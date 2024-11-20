import magic
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich.box import SIMPLE
import os
import csv


console = Console()
def identify_file_type(file_path):
    """Identify the file type using libmagic."""
    try:
        mime = magic.Magic(mime=True)
        description = magic.Magic(mime=False)
        file_type = mime.from_file(file_path)
        detailed_info = description.from_file(file_path)
        return file_type, detailed_info
    except Exception as e:
        console.print(f"[bold red]Error identifying file type: {e}[/]")
        return None, None


def display_results(file_path, file_type, detailed_info):
    """Display file type information in a visually appealing way."""
    table = Table(title="File Identification Results", box=SIMPLE)
    table.add_column("Property", style="bold cyan", justify="center")
    table.add_column("Details", style="bold magenta", justify="left")
    table.add_row("File Path", file_path)
    table.add_row("MIME Type", file_type)
    table.add_row("Detailed Info", detailed_info)

    console.print(Panel.fit(
        table, title="[bold green]Analysis Complete[/]", border_style="green"))


def save_results_to_file(results, output_path):
    """Save analysis results to a file."""
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["File Path", "MIME Type", "Detailed Info"])
            for result in results:
                writer.writerow(result)
        console.print(f"[bold green]Results saved to {output_path}[/]")
    except Exception as e:
        console.print(f"[bold red]Error saving results: {e}[/]")


def analyze_single_file():
    """Analyze a single file."""
    file_path = console.input("[bold yellow]Enter the file path: [/]")

    if not os.path.isfile(file_path):
        console.print("[bold red]Invalid file path. Please try again.[/]")
        return

    console.print("\n[bold blue]Analyzing file...[/]")
    with Progress() as progress:
        task = progress.add_task("[cyan]Processing file...", total=100)
        for _ in range(5):
            progress.update(task, advance=20)
            import time
            time.sleep(0.2)

    file_type, detailed_info = identify_file_type(file_path)
    if file_type:
        display_results(file_path, file_type, detailed_info)


def analyze_directory():
    """Analyze all files in a directory."""
    dir_path = console.input("[bold yellow]Enter the directory path: [/]")

    if not os.path.isdir(dir_path):
        console.print("[bold red]Invalid directory path. Please try again.[/]")
        return

    console.print("\n[bold blue]Analyzing directory...[/]")
    results = []
    with Progress() as progress:
        files = [os.path.join(dir_path, f) for f in os.listdir(
            dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        task = progress.add_task("[cyan]Processing files...", total=len(files))
        for file_path in files:
            file_type, detailed_info = identify_file_type(file_path)
            if file_type:
                results.append((file_path, file_type, detailed_info))
            progress.update(task, advance=1)

    console.print(f"[bold green]{len(results)} files analyzed.[/]")
    for result in results:
        display_results(*result)

    save_option = console.input(
        "[bold green]Save results to a file? (yes/no): [/] ").strip().lower()
    if save_option in ["yes", "y"]:
        output_path = console.input(
            "[bold yellow]Enter the output file path (e.g., results.csv): [/] ")
        save_results_to_file(results, output_path)


def main():
    """Main program loop with an interactive CLI."""
    console.print(
        Panel(
            "[bold yellow]Welcome to File Type Identifier[/]\n"
            "[blue]Analyze files and get detailed insights effortlessly![/]",
            title="File Type Identification Tool",
            border_style="bright_magenta",
        )
    )

    while True:
        console.print("\n[bold cyan]Menu Options:[/]")
        console.print("1. Analyze a single file")
        console.print("2. Analyze all files in a directory")
        console.print("3. Exit\n")

        choice = console.input("[bold green]Enter your choice (1/2/3): [/]")

        if choice == "1":
            analyze_single_file()
        elif choice == "2":
            analyze_directory()
        elif choice == "3":
            console.print("[bold green]Exiting the program. Goodbye![/]")
            break
        else:
            console.print(
                "[bold red]Invalid choice. Please enter 1, 2, or 3.[/]")


if __name__ == "__main__":
    main()



