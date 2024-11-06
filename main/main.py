import yaml
import subprocess
import json
import sys
import re
from colorama import Fore, Style, init
import pyfiglet

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Prints a custom banner in ASCII art."""
    banner = pyfiglet.figlet_format("Auto Drozer", font="slant")
    print(Fore.GREEN + banner)

def load_commands(yaml_file, package_name):
    """Loads commands and titles from a YAML file and injects the package name."""
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
        commands = data.get('commands', [])
        
        # Substitute the package name in each command
        formatted_commands = [
            {'title': cmd['title'], 'command': re.sub(r'\{package\}', package_name, cmd['command'])}
            for cmd in commands
        ]
        return formatted_commands

def check_drozer_connection():
    """Checks if drozer console can connect; exits if it fails."""
    try:
        result = subprocess.run(
            ['drozer', 'console', 'connect', '--command', 'exit'],
            capture_output=True,
            text=True,
            check=True
        )
        if "No module named drozer" in result.stderr:
            print(Fore.RED + "[ - ] [ERROR] Drozer console could not be connected. Ensure Drozer is installed and running.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + "[ - ] [ERROR] Failed to connect to Drozer console. Ensure Drozer is installed and running.")
        sys.exit(1)

def run_drozer_command(command):
    """Runs a single Drozer command and captures the output."""
    try:
        print(Fore.YELLOW + "[ + ] [INFO] Running command: " + Fore.CYAN + f"{command}")
        result = subprocess.run(
            ['drozer', 'console', 'connect', '-c', command],
            capture_output=True,
            text=True,
            check=True
        )
        print(Fore.GREEN + "[ ✔ ] [SUCCESS] Command executed successfully.")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[ - ] [ERROR] Error executing command '{command}': {e}", file=sys.stderr)
        return f"Error: {e}"

def run_commands_and_collect_results(commands):
    """Runs a list of Drozer commands and collects their results with titles."""
    results = []
    for cmd in commands:
        print(Fore.CYAN + f"[ + ] [INFO] Executing: {cmd['title']}")
        output = run_drozer_command(cmd['command'])
        results.append({
            'title': cmd['title'],
            'command': cmd['command'],
            'output': output
        })
    return results

def save_results_to_html(results, output_html):
    """Formats Drozer JSON command output to an HTML file with titles."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Drozer Command Results</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            .command { margin-top: 20px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
            .command h2 { font-size: 18px; color: #555; }
            .output pre { background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>Drozer Command Results</h1>
    """

    for result in results:
        html_content += f"""
        <div class="command">
            <h2>{result['title']}</h2>
            <p><strong>Command:</strong> {result['command']}</p>
            <div class="output">
                <pre>{result['output']}</pre>
            </div>
        </div>
        """

    html_content += """
    </body>
    </html>
    """

    with open(output_html, 'w') as file:
        file.write(html_content)
    print(Fore.GREEN + "[ ✔ ] [SUCCESS] HTML file created: " + Fore.CYAN + f"{output_html}")

def main(yaml_file, output_file, package_name):
    # Print the banner at the start
    print_banner()

    # Check if Drozer console is running
    check_drozer_connection()

    # Load Drozer commands and titles from YAML file with package name substitution
    commands = load_commands(yaml_file, package_name)
    if not commands:
        print(Fore.RED + "[ - ] [ERROR] No commands found in YAML file.")
        return

    # Run commands and collect results
    results = run_commands_and_collect_results(commands)

    # Output results to JSON file
    with open(output_file, 'w') as json_file:
        json.dump(results, json_file, indent=4)
    print(Fore.GREEN + "[ ✔ ] [SUCCESS] Results saved to " + Fore.CYAN + f"{output_file}")

    # Save results to HTML file
    html_output_file = output_file.replace('.json', '.html')
    save_results_to_html(results, html_output_file)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(Fore.RED + "[ - ] [ERROR] Usage: python drozer_script.py <commands.yml> <output.json> <package_name>")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    output_file = sys.argv[2]
    package_name = sys.argv[3]
    
    main(yaml_file, output_file, package_name)
