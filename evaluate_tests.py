import subprocess
import json
import os
import logging
import yaml
import sys
from flake8.api import legacy as flake8
from utils.llm_utils import assess_semantic_correctness
import re

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load evaluation configuration
logger.debug("Loading evaluation configuration from config_evaluation.yml...")
with open('config_evaluation.yml', 'r') as f:
    config = yaml.safe_load(f)
logger.info("Configuration loaded successfully.")


def calculate_code_coverage():
    logger.info("Calculating Code Coverage Score (CCS)...")
    try:
        # Run coverage erase to clear any previous data
        subprocess.run(['coverage', 'erase'], check=True)

        # Run tests with coverage
        subprocess.run(['coverage', 'run', '--source=src', '-m', 'pytest', 'tests/', '--disable-warnings'], check=True)

        # Generate coverage report
        result = subprocess.run(['coverage', 'report'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # Parse the coverage percentage from the output
        coverage_output = result.stdout
        coverage_line = [line for line in coverage_output.split('\n') if 'TOTAL' in line]
        if coverage_line:
            coverage_percentage = float(coverage_line[0].split()[-1].replace('%', ''))
            logger.info(f"Code Coverage Score (CCS): {coverage_percentage:.2f}%")
            return coverage_percentage
        else:
            logger.error("Coverage percentage not found in output.")
            return 0.0
    except subprocess.CalledProcessError as e:
        logger.error(f"Coverage calculation failed: {e.stderr}")
        return 0.0
    except Exception as e:
        logger.error(f"An error occurred while calculating code coverage: {e}")
        return 0.0


def perform_mutation_testing():
    logger.info("Performing Mutation Testing for Test Correctness Score (TCS)...")
    try:
        # Generate fresh coverage data
        logger.debug("Generating fresh coverage data...")
        subprocess.run(['coverage', 'erase'], check=True)
        subprocess.run(['coverage', 'run', '--source=src', '-m', 'pytest', 'tests/'], check=True)

        # Run mutmut tests with --no-progress to suppress spinner output
        command = [
            'mutmut', 'run',
            '--paths-to-mutate=src/',
            '--runner=python -m pytest tests/',
            '--use-coverage',
            '--no-progress'  # Suppress spinner output
        ]
        logger.debug(f"Running command: {' '.join(command)}")
        result_run = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        logger.debug(f"Mutmut run return code: {result_run.returncode}")
        logger.debug(f"Mutmut run stdout:\n{result_run.stdout}")
        logger.debug(f"Mutmut run stderr:\n{result_run.stderr}")

        # Get mutation results without 'summary' argument
        result = subprocess.run(
            ['mutmut', 'results'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        logger.debug(f"Mutmut results return code: {result.returncode}")
        logger.debug(f"Mutmut results stdout:\n{result.stdout}")
        logger.debug(f"Mutmut results stderr:\n{result.stderr}")

        if result.stdout.strip() == '':
            logger.error("Mutmut did not return any results.")
            # Check if .mutmut-cache file exists
            if os.path.exists('.mutmut-cache'):
                logger.debug(".mutmut-cache file exists.")
            else:
                logger.debug(".mutmut-cache file does not exist.")
            return 0.0

        # Parse the results output
        # Initialize counters
        killed = 0
        survived = 0

        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.startswith('Survived'):
                survived += 1
            elif line.startswith('Killed'):
                killed += 1
            # Handle other statuses if necessary

        total = killed + survived
        if total == 0:
            logger.error("No mutants were found.")
            return 0.0

        TCS = (killed / total) * 100.0
        logger.info(f"Test Correctness Score (TCS): {TCS:.2f}%")
        logger.info(f"Mutant summary: {killed} killed, {survived} survived")

        return TCS

    except subprocess.CalledProcessError as e:
        logger.error(f"Mutation testing failed with return code {e.returncode}")
        logger.error(f"Command output:\n{e.output}")
        logger.error(f"Command stderr:\n{e.stderr}")
        logger.error(f"Exception: {e}")
        return 0.0
    except Exception as e:
        logger.error(f"An error occurred during mutation testing: {e}")
        return 0.0




def evaluate_edge_case_handling():
    logger.info("Evaluating Edge Case Handling Score (ECHS)...")
    try:
        with open('edge_cases/jira_edge_cases.json') as f:
            edge_cases = json.load(f)
        covered = 0
        total_edge_cases = len(edge_cases)
        logger.debug(f"Total edge cases to evaluate: {total_edge_cases}")

        for case in edge_cases:
            description = case['description']
            logger.debug(f"Assessing edge case: {description}")
            is_covered = assess_semantic_correctness('tests/', description)
            if is_covered:
                covered += 1

        ECHS = (covered / total_edge_cases) * 100 if total_edge_cases > 0 else 0.0
        logger.info(f"Edge Case Handling Score (ECHS): {ECHS:.2f}%")
        return ECHS
    except FileNotFoundError as e:
        logger.error(f"Edge case file not found: {e}")
        return 0.0
    except Exception as e:
        logger.error(f"An error occurred during edge case evaluation: {e}")
        return 0.0


def evaluate_test_quality():
    logger.info("Evaluating Test Quality Score (TQS)...")
    try:
        style_guide = flake8.get_style_guide(ignore=config['flake8']['ignore'])
        report = style_guide.check_files(['tests/'])
        total_issues_detected = report.total_errors
        max_allowable_issues = config['tqs']['max_allowable_issues']
        TQS = max(0.0, 100.0 - ((total_issues_detected / max_allowable_issues) * 100.0))
        logger.info(f"Test Quality Score (TQS): {TQS:.2f}%")
        return TQS
    except Exception as e:
        logger.error(f"An error occurred during test quality evaluation: {e}")
        return 0.0


def evaluate_exception_handling():
    logger.info("Evaluating Exception Handling Score (EHS)...")
    try:
        total_exceptions_in_code = config['ehs']['total_exceptions_in_code']
        exceptions_properly_tested = 0

        for exception_class in config['ehs']['exception_classes']:
            description = f"Tests that '{exception_class}' is properly raised and handled."
            is_tested = assess_semantic_correctness('tests/', description)
            if is_tested:
                exceptions_properly_tested += 1

        EHS = (exceptions_properly_tested / total_exceptions_in_code) * 100.0 if total_exceptions_in_code > 0 else 0.0
        logger.info(f"Exception Handling Score (EHS): {EHS:.2f}%")
        return EHS
    except Exception as e:
        logger.error(f"An error occurred during exception handling evaluation: {e}")
        return 0.0


def evaluate_duplication():
    logger.info("Evaluating Duplication and Redundancy Score (DRS)...")
    try:
        result = subprocess.run(
            ['flake8', '--select=R', 'tests/'],
            capture_output=True,
            text=True,
            check=False
        )
        duplicate_code_blocks = len(result.stdout.strip().split('\n')) if result.stdout else 0
        total_code_blocks = len([file for file in os.listdir('tests/') if file.endswith('.py')])
        DRS = 100.0 - ((duplicate_code_blocks / total_code_blocks) * 100.0) if total_code_blocks > 0 else 100.0
        logger.info(f"Duplication and Redundancy Score (DRS): {DRS:.2f}%")
        return DRS
    except Exception as e:
        logger.error(f"An error occurred during duplication evaluation: {e}")
        return 0.0


def evaluate_execution_success_rate():
    logger.info("Evaluating Execution Success Rate (ESR)...")
    try:
        # Run pytest with JSON report
        result = subprocess.run(
            ['pytest', 'tests/', '--disable-warnings', '--json-report', '--json-report-file=.report.json'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Parse the JSON report
        with open('.report.json', 'r') as f:
            report = json.load(f)

        total_tests = report['summary']['total']
        passed_tests = report['summary'].get('passed', 0)

        ESR = (passed_tests / total_tests) * 100.0 if total_tests > 0 else 0.0
        logger.info(f"Execution Success Rate (ESR): {ESR:.2f}%")
        return ESR
    except Exception as e:
        logger.error(f"An error occurred during execution success rate evaluation: {e}")
        return 0.0


def generate_report(UFEM, component_scores):
    logger.info("Generating evaluation report...")
    report = {
        'UFEM Score': UFEM,
        'Component Scores': component_scores
    }
    try:
        with open('evaluation_report.json', 'w') as f:
            json.dump(report, f, indent=4)
        logger.info("Report saved to evaluation_report.json")
    except Exception as e:
        logger.error(f"An error occurred while saving the report: {e}")


def compute_ufem():
    logger.info("Starting UFEM evaluation...")

    try:
        CCS = calculate_code_coverage()
        TCS = perform_mutation_testing()
        ECHS = evaluate_edge_case_handling()
        TQS = evaluate_test_quality()
        EHS = evaluate_exception_handling()
        DRS = evaluate_duplication()
        ESR = evaluate_execution_success_rate()

        # Calculate UFEM using weights from the configuration
        UFEM = (
            (CCS * config['weights']['CCS']) +
            (TCS * config['weights']['TCS']) +
            (ECHS * config['weights']['ECHS']) +
            (TQS * config['weights']['TQS']) +
            (EHS * config['weights']['EHS']) +
            (DRS * config['weights']['DRS']) +
            (ESR * config['weights']['ESR'])
        ) / 100.0  # Normalize the score

        component_scores = {
            'CCS': CCS,
            'TCS': TCS,
            'ECHS': ECHS,
            'TQS': TQS,
            'EHS': EHS,
            'DRS': DRS,
            'ESR': ESR
        }

        logger.info(f"\nFinal UFEM Score: {UFEM:.2f}%")
        for key, value in component_scores.items():
            logger.info(f"{key}: {value:.2f}%")

        generate_report(UFEM, component_scores)

    except Exception as e:
        logger.error(f"An error occurred during UFEM evaluation: {e}")
        sys.exit(1)


if __name__ == '__main__':
    compute_ufem()
