from typing import cast
import os
import claude_tools
from termcolor import colored
import anthropic
import constants
from lib import utils
from lib.converter import transcribe


class Assistant(utils.Mode):
    """Compilation Mode: Speak and let Anthropic compile your thoughts into actions."""
    # As of now, param input = mp3

    def __init__(self, input: input) -> None:
        self.input = input
        self.client = anthropic.Anthropic()
        user_message = transcribe(input)

        if constants.compilation_template is not None:
            # Parse compilation template
            with open("templates/" + constants.compilation_template, "r") as file:
                compilation_template = file.read()
            self.system_prompt = f"""
            You are a home assitant running specialized action tools provided in the current runtime environment.
            Use tools where appropriate to answer user queries efficiently, correctly, and concisely.
            Always favor structure over free-form prose if the query lends itself to it.

            Guidelines:
            - Choose the best tool based on the input parameters.
            - Validate that all required fields for a tool are present before attempting execution.
            - If no appropriate tool exists, respond succinctly in plain English.
            - Be direct. Do not apologize, offer disclaimers, or hedge answers unless absolutely necessary.
            - Where possible, favor automation and output that could easily be parsed or used downstream.
            - Use Farenheit when given other
            - Use regular time when given military time
            """
        else:
            self.system_prompt = """
            You are a Claude agent running specialized action tools in a lightweight runtime environment.
            No compilation template was provided — operate using plain natural language.
            Be direct, concise, and favor giving responses that can be easily used in programming contexts or automations.
            """

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
            tool_name = first["name"]
            tool_input = first["input"]
            tool_use_id = first["id"]

            tool_result = claude_tools.run_tool(tool_name, tool_input)

            second_message = self.client.messages.create(
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
            # No tool was needed—just use the original
            final_block = first

        # Now extract the plain-text
        if final_block["type"] == "text":
            final_text = final_block["text"]
        else:
            raise RuntimeError(f"Expected text but got {final_block['type']}")

        self.final_text = final_text
