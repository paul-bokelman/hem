from typing import cast
from lib.input import Input
import os
import claude_tools
from templates import response
from termcolor import colored
import anthropic
import constants
from lib import utils
import lib.converter as converter


class Assistant(utils.Mode):
    """Compilation Mode: Speak and let athronpic compile your thoughts into actions."""
    def __init__(self, input: Input) -> None:
        self.input = input

        # create output directory if it doesn't exist
        #TODO check if we need this or go direct to MP3
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

        try:
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
        
                tool_result = claude_tools(tool_name, tool_input)

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
        #TODO ADD text to MP3
        except:
            print(colored("\nAn error occurred. Please try again.\n", "red"))
            pass