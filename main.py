import typer
from pathlib import Path
import random
import json
from typing import Optional

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
def main(generate: Optional[bool] = typer.Option(False, "--generate", "-g")):
    if generate:
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