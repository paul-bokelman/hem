# python -m db.seed
import os
import csv
from peewee import IntegrityError
from db.models import db, Action

CSV_FILE = os.path.join(os.path.dirname(__file__), 'data/actions-seed.csv')

def seed_actions_from_csv(csv_path=CSV_FILE):
    """Read actions-seed.csv and upsert into the Action table."""
    created = 0
    updated = 0
    
    # read and iterate over the CSV file
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with db.atomic():
        for row in rows:
            name = row['name'].strip()
            description = row['description'].strip()

            try:
                action, was_created = Action.get_or_create(
                    name=name,
                    defaults={'description': description}
                )
                if was_created:
                    created += 1
                else:
                    # update description if changed
                    if action.description != description:
                        action.description = description
                        action.save()
                        updated += 1
            except IntegrityError:
                # skip any unexpected unique constraint issues
                continue

    print(f"✅ {created} new actions created, {updated} actions updated.")

if __name__ == "__main__":
    db.connect(reuse_if_open=True)
    db.create_tables([Action], safe=True)
    seed_actions_from_csv()
    db.close()