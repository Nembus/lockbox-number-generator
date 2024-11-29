import json
import random
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer()
STORAGE_FILE = Path("generated_numbers.json")

def load_generated_numbers():
    if STORAGE_FILE.exists():
        return set(json.loads(STORAGE_FILE.read_text()))
    return set()

def save_generated_numbers(numbers):
    STORAGE_FILE.write_text(json.dumps(list(numbers)))

def get_last_number():
    numbers = load_generated_numbers()
    return list(numbers)[-1] if numbers else None

def is_valid_number(number: int) -> bool:
    digits = str(number)
    return len(digits) == 4 and len(set(digits)) == 4

def generate_unique_number():
    digits = list(range(10))
    selected_digits = random.sample(digits, 4)
    return int(''.join(map(str, selected_digits)))

def generate_number():
    generated = load_generated_numbers()
    while True:
        new_number = generate_unique_number()
        if new_number not in generated:
            break
    generated.add(new_number)
    save_generated_numbers(generated)
    return new_number

@app.callback(invoke_without_command=True)
def main(
    generate: Optional[bool] = typer.Option(False, "--generate", "-g"),
    blacklist: Optional[int] = typer.Option(None, "--blacklist", "-b")
):
    if blacklist is not None:
        if not is_valid_number(blacklist):
            typer.echo("Error: Blacklist number must be 4 digits with no repeating digits")
            raise typer.Exit(1)
        numbers = load_generated_numbers()
        numbers.add(blacklist)
        save_generated_numbers(numbers)
        typer.echo(f"Added {blacklist} to blacklist")
    elif generate:
        new_number = generate_number()
        typer.echo(f"Generated number: {new_number}")
    else:
        last = get_last_number()
        if last:
            typer.echo(f"Last generated number: {last}")
        else:
            typer.echo("No numbers generated yet")

if __name__ == "__main__":
    app()