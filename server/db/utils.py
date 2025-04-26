import dataclasses
from typing import List, Optional
from db.models import User

@dataclasses.dataclass
class Macro:
    id: str
    name: str
    prompt: str
    allow_other_actions: bool
    required_actions: List[str]

def get_user_macros(user_id: str) -> Optional[List[Macro]]:
    """Get a user's macros by their ID."""
    try:
        u = User.get(User.id == user_id)
    except Exception:
        return None
    
    macros: list[Macro] = []
    for m in u.macros:
        macros.append(Macro(
            id=str(m.id),
            name=m.name,
            prompt=m.prompt,
            allow_other_actions=m.allow_other_actions,
            required_actions=[ma.action.name for ma in m.required_actions]
        ))

    return macros