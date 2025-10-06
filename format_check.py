import json
import sys


def check_formatting(filepath: str) -> bool:
    """
    Take a prediction filepath as input and print on the command line whether there
    are any peculiarities about the prediction formatting.

    :param filepath: str path to predictions file (should be jsonl)
    :return: True = Can Parse, False = Cannot Parse
    """
    with open(filepath, "r") as f:
        lines = f.readlines()
    questionable_lines = []
    error_lines = []
    line_ids = []

    # TODO: check the other keys
    for line in lines:
        try:
            json_line = json.loads(line)
            pred = json_line["prediction"]
            pred = int(pred)
            if pred not in [1, 2, 3, 4, 5]:
                questionable_lines.append(line)

        except:
            error_lines.append(line)

    if error_lines:
        print("Error: The following lines are malformatted.")
        print(error_lines)
        print("The above lines are malformatted. Please make sure each line is a valid json.")
        return False

    if questionable_lines:
        print("Warning: The following lines do not have expected values (1-5). Evaluation can still take place but please check your data.")
        print(questionable_lines)
        
    return True


    


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please give the file to check formatting of as an argument")

    check_formatting(sys.argv[1])