# utils/llm_utils.py
import openai
import os
import logging

logger = logging.getLogger(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

def assess_semantic_correctness(test_directory, description):
    try:
        # Read test files
        test_files_content = ""
        for root, dirs, files in os.walk(test_directory):
            for file in files:
                if file.endswith('.py'):
                    with open(os.path.join(root, file), 'r') as f:
                        test_files_content += f.read() + "\n"

        # Construct the prompt
        prompt = f"""
        You are an expert software engineer.
        Given the following tests:

        {test_files_content}

        Assess whether the tests adequately cover the following requirement:

        "{description}"

        Respond with "Yes" if the tests cover the requirement, or "No" otherwise.
        """

        # Call the LLM API (e.g., OpenAI's GPT)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1,
            temperature=0
        )

        answer = response.choices[0].text.strip()
        return answer.lower() == "yes"
    except Exception as e:
        logger.error(f"LLM assessment failed: {e}")
        return False
