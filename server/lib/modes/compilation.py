from typing import cast
from lib.input import Input
import os
from termcolor import colored
import anthropic
import constants
from lib import utils

class Compilation(utils.Mode):
    """Compilation Mode: Speak and have your thoughts compiled into notes."""
    def __init__(self, input: Input) -> None:
        self.input = input

        # create output directory if it doesn't exist
        if not os.path.exists(constants.compilation_output_path):
            os.makedirs(constants.compilation_output_path)

        self.client = anthropic.Anthropic()

        if constants.compilation_template is not None:
            # parse compilation template
            with open("templates/" + constants.compilation_template, "r") as file:
                compilation_template = file.read()
                self.system_prompt = f"""Your job is to compile the user's thoughts into notes. You will be given a template to follow and you must adhere to the following rules:\n1. Items surrounded by '{{{{}}}}' must be filled in by you. Their content should be inferred from their content in relation to the user's message.\n2. Items that end with '...' can and should be replicated as many times as necessary.\n3. Items that end with '!' are optional and should be included if they are relevant to the user's message.\n4. Items that are enclosed in + signs (+like this+) is a prompt for you. Your response should replace it's content in the output.\n\nTEMPLATE:\n\n{compilation_template}"""
        else:
            self.system_prompt = "Your job is to compile the user's thoughts into notes. You should produce a coherent and concise summary of the user's message in a well structured format. Your response should be in markdown format unless explicitly stated otherwise."

    def run(self) -> None:
        print(colored("Compilation Mode", "cyan", attrs=["bold", "underline"]), end=" ")
        print(colored("— Continually ask questions to deepen your understanding of a topic.", "dark_grey"))

        if constants.preferred_input is not None:
            print(f"  * Preferred input: {colored(constants.preferred_input, 'yellow')}")
        else:
            print("  * Preferred input: indifferent")

        if constants.compilation_template is not None:
            print(f"  * Using template: {colored(constants.compilation_template, 'yellow')}")

        if constants.preferred_input != "text":
            max_audio_length = constants.compilation_max_audio_length if constants.compilation_max_audio_length is not None else constants.default_max_audio_length
            print(f"  * Maximum audio length: {colored(utils.convertMilliseconds(max_audio_length), 'yellow')}")
        
        print("  * Press Ctrl+C to exit.\n")

        input_choice = None

        try: 
            while True:
                # prompt user for output path of the notes file
                output_path = None
                while output_path is None or os.path.exists(constants.compilation_output_path + "/" + output_path):
                    if output_path is not None:
                        print(colored("File already exists. Please try again.\n", "red"))
                    output_path = input(f"Save to: /{constants.compilation_output_path}/")

                response, input_type = self.input.get_input(input_choice, constants.compilation_max_audio_length)

                # assign first choice of desired input type to rest of the conversation
                if input_choice is None:
                    input_choice = input_type

                print(colored("\nCompiling notes...", "dark_grey"))
                    
                message = self.client.messages.create(
                    model=constants.compilation_model,
                    max_tokens=constants.compilation_max_tokens,
                    system=self.system_prompt,
                    messages=[
                        {"role": "user", "content": response},
                    ]
                )

                content = cast(anthropic.types.TextBlock, message.content[0])

                with open(constants.compilation_output_path + "/" + output_path, "x") as f:
                    f.write(content.text)

                print(colored(f"\nNotes saved to /{constants.compilation_output_path}/{output_path}.\n", "green"))
        except KeyboardInterrupt:
            pass
        except:
            print(colored("\nAn error occurred. Please try again.\n", "red"))
            pass