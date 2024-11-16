import argparse
import sys

def execute_command(command: str):
    """
    Executes a command by dynamically dispatching to the appropriate agent or tool.
    """
    response = execute_query_dynamically(command)
    print(f"\nResponse:\n{response}\n")


def show_menu():
    """
    Displays the CLI menu and processes user inputs.
    """
    print("\nWelcome to the Multi-Agent Assistant CLI!")
    print("Choose an option:")
    print("1. Analyze logs for critical issues")
    print("2. Resolve dependency conflicts")
    print("3. Run npm install")
    print("4. Stream a real-time query response")
    print("5. Exit")

    try:
        choice = int(input("Enter your choice (1-5): ").strip())
        if choice == 1:
            command = "Analyze logs for critical issues."
            execute_command(command)
        elif choice == 2:
            command = "Resolve dependency conflicts."
            execute_command(command)
        elif choice == 3:
            command = "Run npm install."
            execute_command(command)
        elif choice == 4:
            query = input("Enter your query for real-time response: ").strip()
            stream_response(query)
        elif choice == 5:
            print("Exiting. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select a number between 1 and 5.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def cli_interface():
    """
    Provides an interactive command-line interface with support for arguments or a menu.
    """
    parser = argparse.ArgumentParser(description="Multi-Agent Assistant CLI")
    parser.add_argument("--query", type=str, help="Run a specific query directly without entering the interactive menu.")
    args = parser.parse_args()

    if args.query:
        # Execute a direct query passed via --query
        execute_command(args.query)
    else:
        # Launch the interactive menu
        while True:
            show_menu()

