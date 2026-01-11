import re


class ResponseParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_solver_response(response_text):
        solution_match = re.search(r'\[SOLUTION\](.*?)\[/SOLUTION\]', response_text, re.DOTALL)
        answer_match = re.search(r'\[ANSWER\](.*?)\[/ANSWER\]', response_text, re.DOTALL)

        return {
            'solution': solution_match.group(1).strip() if solution_match else None,
            'answer': answer_match.group(1).strip() if answer_match else None,
            'full': response_text
        }

    @staticmethod
    def parse_checker_response(response_text):
        analysis_match = re.search(r'\[ANALYSIS\](.*?)\[/ANALYSIS\]', response_text, re.DOTALL)
        issues_match = re.search(r'\[ISSUES\](.*?)\[/ISSUES\]', response_text, re.DOTALL)
        verdict_match = re.search(r'\[VERDICT\](.*?)\[/VERDICT\]', response_text, re.DOTALL)

        return {
            'analysis': analysis_match.group(1).strip() if analysis_match else None,
            'issues': issues_match.group(1).strip() if issues_match else None,
            'verdict': verdict_match.group(1).strip() if verdict_match else None,
            'full': response_text
        }

    @staticmethod
    def parse_fixer_response(response_text):
        summary_match = re.search(r'\[FEEDBACK_SUMMARY\](.*?)\[/FEEDBACK_SUMMARY\]', response_text, re.DOTALL)
        solution_match = re.search(r'\[CORRECTED_SOLUTION\](.*?)\[/CORRECTED_SOLUTION\]', response_text, re.DOTALL)
        answer_match = re.search(r'\[CORRECTED_ANSWER\](.*?)\[/CORRECTED_ANSWER\]', response_text, re.DOTALL)

        return {
            'feedback': summary_match.group(1).strip() if summary_match else None,
            'solution': solution_match.group(1).strip() if solution_match else None,
            'answer': answer_match.group(1).strip() if answer_match else None,
            'full': response_text
        }



def test_parse_solver():
    solver_response = """[SOLUTION]
Here is the solution to the problem:
Let x = 5
Then y = x + 3 = 8
[/SOLUTION]
[ANSWER]
y = 8
[/ANSWER]"""

    result = ResponseParser.parse_solver_response(solver_response)
    assert result['solution'] == "Here is the solution to the problem:\nLet x = 5\nThen y = x + 3 = 8"
    assert result['answer'] == "y = 8"

def test_parse_checker():
    checker_response = """[ANALYSIS]
1. Step 1 is correct
2. Step 2 has an error
[/ANALYSIS]
[ISSUES]
- Error in step 2
[/ISSUES]
[VERDICT]
PARTIALLY_CORRECT
[/VERDICT]"""

    result = ResponseParser.parse_checker_response(checker_response)
    assert result['analysis'] == "1. Step 1 is correct\n2. Step 2 has an error"
    assert result['issues'] == "- Error in step 2"
    assert result['verdict'] == "PARTIALLY_CORRECT"

def test_parse_fixer():
    fixer_response = """[FEEDBACK_SUMMARY]
The main issues were in step 2 and 3.
[/FEEDBACK_SUMMARY]
[CORRECTED_SOLUTION]
Here is the corrected solution:
Step 1: Correct
Step 2: Fixed
Step 3: Also fixed
[/CORRECTED_SOLUTION]
[CORRECTED_ANSWER]
42
[/CORRECTED_ANSWER]"""

    result = ResponseParser.parse_fixer_response(fixer_response)
    assert result['feedback_summary'] == "The main issues were in step 2 and 3."
    assert "Here is the corrected solution:" in result['corrected_solution']
    assert result['corrected_answer'] == "42"
