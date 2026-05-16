import re
import logging

logger = logging.getLogger(__name__)

def solve_security_stamp(text: str) -> str:
    """
    Parses strings like 'Compute 14 + 6', 'What is 20 - 5', or '12 + 3 =' 
    and returns the evaluated result as a string.
    """
    try:
        numbers = [int(n) for n in re.findall(r'\d+', text)]

        if len(numbers) < 2:
            raise ValueError(f"Could not find enough integers to parse in text: '{text}'")

        if "+" in text or "sum" in text.lower() or "add" in text.lower():
            result = numbers[0] + numbers[1]
        elif "-" in text or "subtract" in text.lower() or "minus" in text.lower():
            result = numbers[0] - numbers[1]
        else:
            raise ValueError(f"Unknown mathematical operator in text: '{text}'")

        return str(result)

    except Exception as e:
        print(f"Error parsing: {e}")
        return ""

if __name__ == "__main__":
    print("--- Running Local OCR/Text Math Tests ---")
    test_cases = [
        "Compute 17 + 3",
        "What is 45 - 5",
        "12 + 8 =",
    ]

    for case in test_cases:
        res = solve_security_stamp(case)
        print(f"Input: {case:15} | Parsed Output: {res}")