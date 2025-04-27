from typing import cast
from anthropic.types import MessageParam
import anthropic
from globals import constants
from lib.actions import Actions
from lib.prompts import Prompts
from db.utils import get_user_macros

actions = Actions() # initialize the Actions class (singleton)
prompts = Prompts() 

class Processor:
    """Compilation Mode: Speak and let anthropic compile your thoughts into actions."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Processor, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True
        self.client = anthropic.Anthropic()

    @staticmethod
    def _remove_enclosed_tag_data(text: str, tag: str) -> str:
        """Remove all data enclosed in the specified tag from the text."""
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        while start_tag in text and end_tag in text:
            start_index = text.index(start_tag)
            end_index = text.index(end_tag) + len(end_tag)
            text = text[:start_index] + text[end_index:]
        return text

    def handle_message(self, user_id: str, user_prompt: str) -> tuple[str, list[str]]:
        """Handles an incoming message from a specific user and returns a text response and a list of actions performed."""
        messages: list[MessageParam] = [
            {"role": "user", "content": user_prompt}
        ]

        actions_performed: list[str] = []

        # load macros and generate system prompt
        macros = get_user_macros(user_id)
        system_prompt = prompts.get_system_prompt(macros)

        while True:
            response = self.client.messages.create(
                model=constants.model,
                max_tokens=constants.max_tokens,
                system=system_prompt,
                messages=messages,
                tools=actions.action_schemas,
            )

            text_block = next((item for item in response.content if item.type == "text"), None)
            tool_block = next((item for item in response.content if item.type == "tool_use"), None)

            # requested tool use -> use tool and append result to messages
            if tool_block:
                actions_performed.append(tool_block.name)
                try:
                    action_result = actions.execute(tool_block.name, cast(dict, tool_block.input))
                except Exception as e:
                    action_result = {"error": str(e)}

                previous_message = {"role": "assistant", "content": []}

                # text block is preset -> append to previous message
                if text_block:
                    previous_message["content"].append({"type": "text", "text": text_block.text})

                # append tool use to previous message
                previous_message["content"].append({
                    "type": "tool_use",
                    "id": tool_block.id,
                    "name": tool_block.name,
                    "input": tool_block.input
                })

                messages.append(cast(MessageParam, previous_message))

                action_result_message = cast(MessageParam, {"role": "user", "content": [{ "type": "tool_result", "tool_use_id": tool_block.id, "content": action_result }]})

                messages.append(action_result_message)
                
            # no tool use -> return llm final response
            else:
                return (Processor._remove_enclosed_tag_data(text_block.text, "input_analysis") if text_block else "", actions_performed)