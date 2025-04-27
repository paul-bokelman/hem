from globals import constants
from db.utils import Macro
import os

class Prompts:
    _prompt_cache = {}

    @staticmethod
    def _get_prompt(prompt_name: str):
        """Get a prompt from the prompts directory, using cache if available."""
        if prompt_name in Prompts._prompt_cache:
            return Prompts._prompt_cache[prompt_name]

        if not os.path.exists(constants.prompts_dir):
            raise FileNotFoundError(f"Prompts directory not found: {constants.prompts_dir}")
        
        prompt_path = os.path.join(constants.prompts_dir, f"{prompt_name}.prompt.txt")
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        with open(prompt_path, "r") as file:
            prompt_content = file.read()
            Prompts._prompt_cache[prompt_name] = prompt_content
            return prompt_content

    @staticmethod
    def get_system_prompt(macros: list[Macro] | None) -> str:
        """Get the system prompt with the narrative and temperaments."""
        formatted_macros = ""

        # format macros
        if macros and len(macros) > 0:
            for macro in macros:
                formatted_macro = f"[{macro.name}]\nPrompt: {macro.prompt}\nRequired Tools: {', '.join(macro.required_actions)}\nAllow Other Tools: {macro.allow_other_actions}"
                formatted_macros += f"\n{formatted_macro}\n"

        return Prompts._get_prompt("system").replace("{{USER_MACROS}}", formatted_macros)
    
    @staticmethod
    def get_prompt(name: str, *args) -> str:
        """Get a prompt by name and replace placeholders with arguments."""
        prompt = Prompts._get_prompt(name)
        for i, arg in enumerate(args):
            prompt = prompt.replace(f"{{arg{i}}}", str(arg))
        return prompt
        