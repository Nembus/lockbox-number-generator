import typer
from pathlib import Path
import random
import json

app = typer.Typer()
STORAGE_FILE = Path("generated_numbers.json")

def load_generated_numbers():
    if STORAGE_FILE.exists():
        return set(json.loads(STORAGE_FILE.read_text()))
    return set()

def save_generated_numbers(numbers):
    STORAGE_FILE.write_text(json.dumps(list(numbers)))

def generate_unique_number():
    # Get all available digits
    digits = list(range(10))
    # Generate 4 unique digits
    selected_digits = random.sample(digits, 4)
    # Convert to number
    return int(''.join(map(str, selected_digits)))

def generate_number():
    generated = load_generated_numbers()

    # Generate new unique number
    while True:
        new_number = generate_unique_number()
        if new_number not in generated:
            break

    generated.add(new_number)
    save_generated_numbers(generated)
    typer.echo(f"Generated number: {new_number}")

app.command()(generate_number)

if __name__ == "__main__":
    app()