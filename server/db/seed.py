# python -m db.seed
from peewee import IntegrityError
from db.models import db, Action
from lib.actions import Actions

def seed_actions_from_registry():
    """Seed the Action table using the action registry from the Actions class."""
    created = 0
    updated = 0

    # Get the action registry from the Actions class
    actions = Actions().action_registry

    with db.atomic():
        for action_name, action_func in actions.items():
            # Extract the description from the action's metadata
            action_metadata = getattr(action_func, "__action__", {})
            description = action_metadata.get("description", "").strip()

            try:
                # Insert or update the action in the database
                action, was_created = Action.get_or_create(
                    name=action_name.replace('_', ' ').title(),
                    defaults={"description": description}
                )
                if was_created:
                    created += 1
                else:
                    # Update the description if it has changed
                    if action.description != description:
                        action.description = description
                        action.save()
                        updated += 1
            except IntegrityError:
                # Skip any unexpected unique constraint issues
                continue

    print(f"✅ {created} new actions created, {updated} actions updated.")

if __name__ == "__main__":
    db.connect(reuse_if_open=True)
    db.create_tables([Action], safe=True)
    seed_actions_from_registry()
    db.close()