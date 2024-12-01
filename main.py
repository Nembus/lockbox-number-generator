import json
import random
from datetime import datetime
from pathlib import Path
from typing import Optional, Set

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
STORAGE_FILE = Path("generated_numbers.json")
console = Console()


# Internal blacklist of easily guessable numbers
INTERNAL_BLACKLIST = {1234, 4321, 2345, 3456, 4567, 5678, 6789, 7890, 8901, 9012}


def is_valid_number(number: int) -> bool:
    try:
        digits = str(number)
        return len(digits) == 4 and len(set(digits)) == 4
    except (ValueError, TypeError):
        return False


def is_available_number(number: int) -> bool:
    return (
        is_valid_number(number)
        and number not in INTERNAL_BLACKLIST
        and number not in load_generated_numbers()
    )


def add_number(number: int) -> bool:
    if not is_available_number(number):
        return False

    data = load_full_data()
    data.append({"number": number, "dateCreated": datetime.now().strftime("%Y-%m-%d")})
    save_generated_numbers(data)
    return True


def load_generated_numbers():
    if STORAGE_FILE.exists():
        data = json.loads(STORAGE_FILE.read_text())
        return {item["number"] for item in data}
    return set()


def load_full_data():
    if STORAGE_FILE.exists():
        return json.loads(STORAGE_FILE.read_text())
    return []


def save_generated_numbers(numbers_data):
    STORAGE_FILE.write_text(json.dumps(numbers_data, indent=2))


def get_last_number():
    data = load_full_data()
    return data[-1]["number"] if data else None


def load_all_blacklisted_numbers() -> Set[int]:
    return INTERNAL_BLACKLIST | load_generated_numbers()


def generate_unique_number():
    digits = list(range(10))
    blacklisted = load_all_blacklisted_numbers()

    while True:
        selected_digits = random.sample(digits, 4)
        # Force 4 digits by converting to string with leading zeros
        number = int(
            f"{selected_digits[0]}{selected_digits[1]}{selected_digits[2]}{selected_digits[3]}"
        )
        if number not in blacklisted and 1000 <= number <= 9999:
            return number


def generate_number():
    data = load_full_data()
    generated = {item["number"] for item in data}

    while True:
        new_number = generate_unique_number()
        if new_number not in generated:
            break

    data.append(
        {"number": new_number, "dateCreated": datetime.now().strftime("%Y-%m-%d")}
    )
    save_generated_numbers(data)
    return new_number


def display_numbers_table():
    data = load_full_data()
    if not data:
        typer.echo("No numbers generated yet")
        return

    table = Table(title="Generated Numbers")
    table.add_column("Number", justify="right")
    table.add_column("Date Created", justify="left")

    for entry in data:
        table.add_row(str(entry["number"]), entry["dateCreated"])

    console.print(table)


@app.callback(invoke_without_command=True)
def main(
    generate: Optional[bool] = typer.Option(False, "--generate", "-g"),
    blacklist: Optional[int] = typer.Option(None, "--blacklist", "-b"),
    show: Optional[bool] = typer.Option(False, "--show", "-s"),
    add: Optional[int] = typer.Option(None, "--add", "-a"),
):
    if add is not None:
        if add_number(add):
            typer.echo(f"Added number: {add}")
        else:
            typer.echo("Error: Number is invalid, blacklisted, or already exists")
            raise typer.Exit(1)
    if show:
        display_numbers_table()
    elif blacklist is not None:
        if not is_valid_number(blacklist):
            typer.echo(
                "Error: Blacklist number must be 4 digits with no repeating digits"
            )
            raise typer.Exit(1)
        data = load_full_data()
        data.append(
            {"number": blacklist, "dateCreated": datetime.now().strftime("%Y-%m-%d")}
        )
        save_generated_numbers(data)
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
