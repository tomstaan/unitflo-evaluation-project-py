import openai
import os
import logging
from openai import OpenAI
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    client = OpenAI(api_key=api_key)
    return client


def assess_semantic_correctness(test_directory, description):
    try:
        client = initialize_openai_client()
        # Collect all test files
        test_files_content = ""
        for root, dirs, files in os.walk(test_directory):
            for file in files:
                if file.endswith('.py'):
                    with open(os.path.join(root, file), 'r') as f:
                        test_files_content += f.read() + "\n"
        
        # Construct prompt for OpenAI
        prompt = f"""
        You are an expert software engineer.
        Given the following tests:\n{test_files_content}\n
        Assess whether the tests cover the requirement: "{description}".
        Respond with "Yes" if the tests cover it, or "No" otherwise.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a software testing expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        
        answer = response.choices[0].message.content.strip().lower()
        return "yes" in answer
    except Exception as e:
        logger.error(f"LLM assessment failed: {e}")
        return False
