#!/bin/bash

# Create directories
mkdir -p .github/workflows
mkdir -p src/config
mkdir -p src/data
mkdir -p src/services
mkdir -p tests
mkdir -p tests_evaluation
mkdir -p edge_cases
mkdir -p embeddings
mkdir -p utils

# Create files in the root directory
touch .gitignore
touch .pre-commit-config.yaml
touch CONTRIBUTING.md
touch Dockerfile
touch LICENSE
touch README.md
touch requirements.txt
touch setup.cfg
touch evaluate_tests.py
touch config_evaluation.yml

# Create files under .github/workflows
touch .github/workflows/ci.yml

# Create files under src/
touch src/__init__.py
touch src/api_client.py
touch src/data_processor.py
touch src/exceptions.py
touch src/model.py
touch src/utilities.py
touch src/validations.py

# Create files under src/config
touch src/config/__init__.py
touch src/config/settings.py

# Create files under src/data
touch src/data/__init__.py
touch src/data/data_source.py

# Create files under src/services
touch src/services/__init__.py
touch src/services/service_a.py
touch src/services/service_b.py

# Create files under tests/
touch tests/__init__.py
touch tests/test_api_client.py
touch tests/test_data_processor.py
touch tests/test_model.py
touch tests/test_services.py
touch tests/test_utilities.py
touch tests/test_validations.py

# Create files under tests_evaluation
touch tests_evaluation/__init__.py
touch tests_evaluation/test_evaluate_tests.py

# Create files under edge_cases
touch edge_cases/jira_edge_cases.json

# Create files under embeddings
touch embeddings/code_embeddings.json

# Create files under utils
touch utils/__init__.py
touch utils/llm_utils.py
touch utils/logger.py

echo "Project structure created successfully!"
