import subprocess
import json
import os
import logging
from coverage import Coverage
from flake8.api import legacy as flake8
from utils.llm_utils import assess_semantic_correctness
import yaml
import sys

# Setup logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG to get more detailed logs
logger = logging.getLogger(__name__)

# Load evaluation configuration
logger.debug("Loading evaluation configuration from config_evaluation.yml...")
with open('config_evaluation.yml', 'r') as f:
    config = yaml.safe_load(f)
logger.info("Configuration loaded successfully.")

def calculate_code_coverage():
    logger.info("Calculating Code Coverage Score (CCS)...")
    try:
        cov = Coverage(source=['src'])
        cov.start()
        logger.debug("Running pytest with coverage collection...")
        subprocess.run(['pytest', 'tests/', '--disable-warnings'], check=True)
        cov.stop()
        cov.save()
        coverage_percentage = cov.report()
        logger.info(f"Code Coverage Score (CCS): {coverage_percentage:.2f}%")
        return coverage_percentage
    except subprocess.CalledProcessError as e:
        logger.error(f"Pytest failed: {e}")
        return 0
    except Exception as e:
        logger.error(f"An error occurred while calculating code coverage: {e}")
        return 0

def perform_mutation_testing():
    logger.info("Performing Mutation Testing for Test Correctness Score (TCS)...")
    try:
        subprocess.run(['mutmut', 'run', '--paths-to-mutate=src/'], check=True)
        result = subprocess.run(['mutmut', 'results', '--json'], capture_output=True, text=True, check=True)
        mutmut_results = json.loads(result.stdout)
        killed = mutmut_results.get('killed_mutants', 0)
        survived = mutmut_results.get('surviving_mutants', 0)
        total = killed + survived
        TCS = (killed / total) * 100 if total > 0 else 0
        logger.info(f"Test Correctness Score (TCS): {TCS:.2f}%")
        return TCS
    except subprocess.CalledProcessError as e:
        logger.error(f"Mutation testing failed: {e}")
        return 0
    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError in mutation testing: {e}")
        return 0
    except Exception as e:
        logger.error(f"An error occurred during mutation testing: {e}")
        return 0

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

        ECHS = (covered / total_edge_cases) * 100 if total_edge_cases > 0 else 0
        logger.info(f"Edge Case Handling Score (ECHS): {ECHS:.2f}%")
        return ECHS
    except FileNotFoundError as e:
        logger.error(f"Edge case file not found: {e}")
        return 0
    except Exception as e:
        logger.error(f"An error occurred during edge case evaluation: {e}")
        return 0

def evaluate_test_quality():
    logger.info("Evaluating Test Quality Score (TQS)...")
    try:
        style_guide = flake8.get_style_guide(ignore=config['flake8']['ignore'])
        report = style_guide.check_files(['tests/'])
        total_issues_detected = report.total_errors
        max_allowable_issues = config['tqs']['max_allowable_issues']
        TQS = max(0, 100 - ((total_issues_detected / max_allowable_issues) * 100))
        logger.info(f"Test Quality Score (TQS): {TQS:.2f}%")
        return TQS
    except Exception as e:
        logger.error(f"An error occurred during test quality evaluation: {e}")
        return 0

def evaluate_exception_handling():
    logger.info("Evaluating Exception Handling Score (EHS)...")
    try:
        exceptions_properly_tested = assess_semantic_correctness('tests/', "Proper exception handling in tests")
        total_exceptions_in_code = config['ehs']['total_exceptions_in_code']
        EHS = (exceptions_properly_tested / total_exceptions_in_code) * 100 if total_exceptions_in_code > 0 else 0
        logger.info(f"Exception Handling Score (EHS): {EHS:.2f}%")
        return EHS
    except Exception as e:
        logger.error(f"An error occurred during exception handling evaluation: {e}")
        return 0

def evaluate_duplication():
    logger.info("Evaluating Duplication and Redundancy Score (DRS)...")
    try:
        result = subprocess.run(['flake8', '--select=R', 'tests/'], capture_output=True, text=True, check=True)
        duplicate_code_blocks = len(result.stdout.strip().split('\n')) if result.stdout else 0
        total_code_blocks = len(os.listdir('tests/'))
        DRS = 100 - ((duplicate_code_blocks / total_code_blocks) * 100) if total_code_blocks > 0 else 100
        logger.info(f"Duplication and Redundancy Score (DRS): {DRS:.2f}%")
        return DRS
    except Exception as e:
        logger.error(f"An error occurred during duplication evaluation: {e}")
        return 0

def evaluate_execution_success_rate():
    logger.info("Evaluating Execution Success Rate (ESR)...")
    try:
        result = subprocess.run(['pytest', 'tests/', '--disable-warnings'], capture_output=True, text=True)
        ESR = 100 if result.returncode == 0 else 0
        logger.info(f"Execution Success Rate (ESR): {ESR:.2f}%")
        return ESR
    except Exception as e:
        logger.error(f"An error occurred during execution success rate evaluation: {e}")
        return 0

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

        UFEM = (
            (CCS * config['weights']['CCS']) +
            (TCS * config['weights']['TCS']) +
            (ECHS * config['weights']['ECHS']) +
            (TQS * config['weights']['TQS']) +
            (EHS * config['weights']['EHS']) +
            (DRS * config['weights']['DRS']) +
            (ESR * config['weights']['ESR'])
        )

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
