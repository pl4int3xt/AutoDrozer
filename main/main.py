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
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEJ+K2+P6T3vBa6J00k78sghYh/g3AqWbVjxU3jHElg1l5PCgD7Yzq9rWc9t5" crossorigin="anonymous">
        <style>
            body { font-family: 'Arial', sans-serif; margin: 20px; background-color: #f8f9fa; }
            h1 { color: #495057; text-align: center; margin-bottom: 40px; }
            .command { margin-top: 20px; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
            .command h2 { font-size: 20px; color: #343a40; }
            .output pre { background: #e9ecef; padding: 15px; border-radius: 5px; font-size: 14px; color: #495057; overflow-x: auto; }
            .command p { font-size: 14px; color: #6c757d; margin-bottom: 10px; }
            .btn-copy { background-color: #007bff; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; }
            .btn-copy:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>

        <h1>Drozer Command Results</h1>

        <div class="container">
    """
    for result in results:
        html_content += f"""
        <div class="command">
            <h2>{result['title']}</h2>
            <p><strong>Command:</strong> <code>{result['command']}</code></p>
            <button class="btn btn-primary btn-sm btn-copy" onclick="copyToClipboard('{result['command']}')">Copy Command</button>
            <div class="output">
                <pre>{result['output']}</pre>
            </div>
        </div>
        <hr>
        """

    html_content += """
        </div>

        <script>
            function copyToClipboard(text) {
                navigator.clipboard.writeText(text).then(function() {
                    alert('Command copied to clipboard!');
                }, function(err) {
                    alert('Error copying text: ' + err);
                });
            }
        </script>
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
