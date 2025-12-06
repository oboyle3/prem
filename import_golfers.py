import os
import django
import csv

# --- Load Django environment ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prempickem.settings")
django.setup()


from Fantasy_App.models import GolfersInDatabase

CSV_PATH = "2023_masters_golfers.csv"  # <-- Put your CSV file in project root

def import_golfers():
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            name = row["name"]
            hometown = row["hometown"]
            tour = row["tour"]
            rating = int(row["rating"])

            golfer, created = GolfersInDatabase.objects.get_or_create(
                name=name,
                defaults={
                    "hometown": hometown,
                    "tour": tour,
                    "rating": rating,
                }
            )

            if created:
                print(f"Added: {name}")
            else:
                print(f"Already exists: {name}")

    print("\nImport complete!")

if __name__ == "__main__":
    import_golfers()
