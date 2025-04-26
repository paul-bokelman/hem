from typing import cast
from lib.input import Input
from termcolor import colored
import anthropic
from lib import utils
import constants

class Inquisitive(utils.Mode):
    """Inquisitive Mode: Ask the user questions to deepen their understanding of a topic."""
    def __init__(self, input: Input) -> None:
        self.input = input
        self.client = anthropic.Anthropic()

        self.system_prompt = f"You are a curious peer, eager to understand the user's topic the user is explaining. You ask deep, relevant questions and seek analogies to bridge gaps in your understanding, despite limited prior knowledge. Ensure you're only asking a maximum of {constants.max_questions} question(s) per message {'and keeping responses very concise' if constants.concise_questions else ''}. If the user's explanation is not completely correct, steer them in the right direction with your questions. Additionally, if the user's explanation is too complex, ask for a simpler explanation. Lastly, don't explain yourself just ask questions."

    def run(self) -> None:
        print(colored("Inquisitive Mode", "cyan", attrs=["bold", "underline"]), end=" ")
        print(colored("— Continually ask questions to deepen your understanding of a topic.", "dark_grey"))

        if constants.preferred_input is not None:
            print(f"  * Preferred input: {colored(constants.preferred_input, 'yellow')}")
        else:
            print("  * Preferred input: indifferent")

        if constants.preferred_input != "text":
            max_audio_length = constants.inquisitive_max_audio_length if constants.inquisitive_max_audio_length is not None else constants.default_max_audio_length
            print(f"  * Maximum audio length: {colored(utils.convertMilliseconds(max_audio_length), 'yellow')}")

        print("  * Press Ctrl+C to exit.\n")

        input_choice = None

        try: 
            while True:
                response, input_type = self.input.get_input(input_choice, constants.inquisitive_max_audio_length)

                # assign first choice of desired input type to rest of the conversation
                if input_choice is None:
                    input_choice = input_type

                message = self.client.messages.create(
                    model=constants.inquisitive_model,
                    max_tokens=constants.inquisitive_max_tokens,
                    system=self.system_prompt,
                    messages=[
                        {"role": "user", "content": response},
                    ],
                )

                content = cast(anthropic.types.TextBlock, message.content[0])
                print(f"\n{colored('Fathom', 'light_magenta')}: {content.text}\n")
        except KeyboardInterrupt:
            pass
        except:
            print(colored("\nAn error occurred. Please try again.\n", "red"))
            pass