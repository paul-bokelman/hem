from typing import cast
import os
import claude_tools
from termcolor import colored
import anthropic
import constants
from lib import utils
from lib.converter import transcribe


class Assistant(utils.Mode):
    """Compilation Mode: Speak and let athronpic compile your thoughts into actions."""
    #as of now param input = mp3
    def __init__(self, input: input) -> None:
        self.input = input
        self.client = anthropic.Anthropic()
        user_message = transcribe(input)

        if constants.compilation_template is not None:
            # parse compilation template
            with open("templates/" + constants.compilation_template, "r") as file:
                compilation_template = file.read()
                self.system_prompt = f""""TODO"""
        else:
            self.system_prompt = "TODO"

        # This is what is sent to Anthropic
        message = self.client.messages.create(
            model=constants.compilation_model,
            max_tokens=constants.compilation_max_tokens,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": user_message},
            ],
            tool_choice="auto"
        )

        first = message.content[0]
        if first["type"] == "tool_use":
            tool_name   = first["name"]
            tool_input  = first["input"]
            tool_use_id = first["id"]
    
            tool_result = claude_tools.run_tool(tool_name, tool_input)

            second_message =self.client.messages.create(
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
            final_block = second_message.content[0]
        else:
            # no tool was needed—just use the original
            final_block = first

        # 4) Now extract the plain‐text
        if final_block["type"] == "text":
            final_text = final_block["text"]
        else:
            raise RuntimeError(f"Expected text but got {final_block['type']}")

        return final_block