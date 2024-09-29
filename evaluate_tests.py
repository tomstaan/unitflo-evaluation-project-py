# evaluate_tests.py
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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load evaluation configuration
with open('config_evaluation.yml', 'r') as f:
    config = yaml.safe_load(f)

def calculate_code_coverage():
    logger.info("Calculating Code Coverage Score (CCS)...")
    cov = Coverage(source=['src'])
    cov.start()
    subprocess.run(['pytest', 'tests/', '--disable-warnings'])
    cov.stop()
    cov.save()
    coverage_percentage = cov.report()
    return coverage_percentage

def perform_mutation_testing():
    logger.info("Performing Mutation Testing for Test Correctness Score (TCS)...")
    subprocess.run(['mutmut', 'run', '--paths-to-mutate=src/'])
    result = subprocess.run(['mutmut', 'results', '--json'], capture_output=True, text=True)
    try:
        mutmut_results = json.loads(result.stdout)
        killed = mutmut_results.get('killed_mutants', 0)
        survived = mutmut_results.get('surviving_mutants', 0)
        total = killed + survived
        TCS = (killed / total) * 100 if total > 0 else 0
        return TCS
    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError: {e}")
        return 0

def evaluate_edge_case_handling():
    logger.info("Evaluating Edge Case Handling Score (ECHS)...")
    with open('edge_cases/jira_edge_cases.json') as f:
        edge_cases = json.load(f)
    covered = 0
    total_edge_cases = len(edge_cases)
    for case in edge_cases:
        description = case['description']
        is_covered = assess_semantic_correctness('tests/', description)
        if is_covered:
            covered += 1
    ECHS = (covered / total_edge_cases) * 100 if total_edge_cases > 0 else 0
    return ECHS

def evaluate_test_quality():
    logger.info("Evaluating Test Quality Score (TQS)...")
    style_guide = flake8.get_style_guide(ignore=config['flake8']['ignore'])
    report = style_guide.check_files(['tests/'])
    total_issues_detected = report.total_errors
    max_allowable_issues = config['tqs']['max_allowable_issues']
    TQS = max(0, 100 - ((total_issues_detected / max_allowable_issues) * 100))
    return TQS

def evaluate_exception_handling():
    logger.info("Evaluating Exception Handling Score (EHS)...")
    exceptions_properly_tested = assess_semantic_correctness('tests/', "Proper exception handling in tests")
    total_exceptions_in_code = config['ehs']['total_exceptions_in_code']
    EHS = (exceptions_properly_tested / total_exceptions_in_code) * 100 if total_exceptions_in_code > 0 else 0
    return EHS

def evaluate_duplication():
    logger.info("Evaluating Duplication and Redundancy Score (DRS)...")
    result = subprocess.run(['flake8', '--select=R', 'tests/'], capture_output=True, text=True)
    duplicate_code_blocks = len(result.stdout.strip().split('\n')) if result.stdout else 0
    total_code_blocks = len(os.listdir('tests/'))
    DRS = 100 - ((duplicate_code_blocks / total_code_blocks) * 100) if total_code_blocks > 0 else 100
    return DRS

def evaluate_execution_success_rate():
    logger.info("Evaluating Execution Success Rate (ESR)...")
    result = subprocess.run(['pytest', 'tests/', '--disable-warnings'], capture_output=True, text=True)
    if result.returncode == 0:
        ESR = 100
    else:
        ESR = 0
    return ESR

def generate_report(UFEM, component_scores):
    logger.info("Generating evaluation report...")
    report = {
        'UFEM Score': UFEM,
        'Component Scores': component_scores
    }
    with open('evaluation_report.json', 'w') as f:
        json.dump(report, f, indent=4)
    logger.info("Report saved to evaluation_report.json")

def compute_ufem():
    logger.info("Starting UFEM evaluation...")
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

if __name__ == '__main__':
    try:
        compute_ufem()
    except Exception as e:
        logger.error(f"An error occurred during UFEM evaluation: {e}")
        sys.exit(1)
