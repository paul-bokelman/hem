from abc import abstractmethod
from lib.input import Input
from termcolor import colored

class Mode:
    """Base Mode class"""

    @abstractmethod
    def __init__(self, input: Input) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

def compose_q(key: str, hint: str) -> str:
    """Compose a question with a key and hint"""
    return key + colored(f" — {hint}", "dark_grey")

def decompose_q(question: str) -> tuple[str, str]:
    """Decompose a question into a key and hint"""
    assert "—" in question, "Question does not contain a hint"
    key, hint = question.replace("\x1b[90m", "").replace("\x1b[0m", "").split("—")
    return key.strip(), hint.strip()

def convertMilliseconds(m: int) -> str:
    seconds = int((m/1000)%60)
    minutes= int((m/(1000*60))%60)
    hours= int((m/(1000*60*60))%24)

    formatted_string = ""

    if hours > 0:
        formatted_string += f"{hours} hours"
    if minutes > 0:
        if formatted_string:
            formatted_string += ", "
        formatted_string += f"{minutes} minutes"
    if seconds > 0:
        if formatted_string:
            formatted_string += ", "
        formatted_string += f"{seconds} seconds"

    return formatted_string