# tests_evaluation/test_evaluate_tests.py
import unittest
from unittest.mock import patch, MagicMock
from evaluate_tests import (
    calculate_code_coverage,
    perform_mutation_testing,
    evaluate_edge_case_handling,
    evaluate_test_quality,
    evaluate_exception_handling,
    evaluate_duplication,
    evaluate_execution_success_rate,
)

class TestEvaluateTests(unittest.TestCase):
    @patch('evaluate_tests.Coverage')
    def test_calculate_code_coverage(self, mock_coverage):
        mock_cov = MagicMock()
        mock_cov.report.return_value = 85.0
        mock_coverage.return_value = mock_cov
        result = calculate_code_coverage()
        self.assertEqual(result, 85.0)

    @patch('evaluate_tests.subprocess')
    def test_perform_mutation_testing(self, mock_subprocess):
        mock_result = MagicMock()
        mock_result.stdout = '{"killed_mutants": 10, "surviving_mutants": 5}'
        mock_subprocess.run.return_value = mock_result
        result = perform_mutation_testing()
        self.assertEqual(result, 66.66666666666666)

    @patch('evaluate_tests.assess_semantic_correctness')
    def test_evaluate_edge_case_handling(self, mock_assess):
        mock_assess.return_value = True
        result = evaluate_edge_case_handling()
        self.assertEqual(result, 100.0)

    @patch('evaluate_tests.flake8.get_style_guide')
    def test_evaluate_test_quality(self, mock_style_guide):
        mock_report = MagicMock()
        mock_report.total_errors = 5
        mock_style_guide.return_value.check_files.return_value = mock_report
        result = evaluate_test_quality()
        self.assertEqual(result, 95.0)

if __name__ == '__main__':
    unittest.main()
