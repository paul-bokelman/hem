from typing import cast
from lib.input import Input
import os
from termcolor import colored
import anthropic
import constants
from lib import utils
import lib.converter as converter
import tools 



class Assistant(utils.Mode):
    """Compilation Mode: Speak and let athronpic compile your thoughts into actions."""
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
                self.system_prompt = f""""TODO"""
        else:
            self.system_prompt = "TODO"

    def run(self) -> None:
        if constants.preferred_input is not None:
            print(f"  * Preferred input: {colored(constants.preferred_input, 'yellow')}")
        else:
            print("  * Preferred input: indifferent")

        if constants.compilation_template is not None:
            print(f"  * Using template: {colored(constants.compilation_template, 'yellow')}")

        input_choice = None

        try: 
            # prompt user for output path of the notes file
            output_path = None
            while output_path is None or os.path.exists(constants.compilation_output_path + "/" + output_path):
                if output_path is not None:
                    print(colored("File already exists. Please try again.\n", "red"))
                output_path = input(f"Save to: /{constants.compilation_output_path}/")

            response, input_type = self.input.get_input(input_choice, constants.compilation_max_audio_length)

            # This is what is sent to Anthropic
            message = self.client.messages.create(
                model=constants.compilation_model,
                max_tokens=constants.compilation_max_tokens,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": response},
                ],
                tool_choice="auto"
            )

            content = cast(anthropic.types.TextBlock, message.content[0])
            if content["type"] == "tool_use":
                tool_name = content["name"]
                tool_input = content["input"]
                tool_use_id = content["id"]
        
                tool_result = tools_runner(tool_name, tool_input)

                self.client.messages.create(
                    model=constants.compilation_model,
                    max_tokens=constants.compilation_max_tokens,
                    system=self.system_prompt,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_use_id,
                                    "content": tool_result
                                }
                            ]
                        }
                    ]
                )
            else:
                content = cast(anthropic.types.TextBlock, content)

            with open(constants.compilation_output_path + "/" + output_path, "x") as f:
                f.write(content.text)

            print(colored(f"\nNotes saved to /{constants.compilation_output_path}/{output_path}.\n", "green"))
        except KeyboardInterrupt:
            pass
        except:
            print(colored("\nAn error occurred. Please try again.\n", "red"))
            pass