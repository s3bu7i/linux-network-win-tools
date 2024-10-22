import subprocess
from flask import Flask, request, render_template_string, redirect, url_for
import logging

app = Flask(__name__)

# Set up logging to log executed commands and errors
logging.basicConfig(filename='rce.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Simple username/password storage (for demonstration purposes, don't use in production)
USERS = {'admin': 'password123'}

# List of allowed commands (whitelisting)
ALLOWED_COMMANDS = ['ls', 'pwd', 'whoami', 'uptime']

# Basic HTML for the input form (simple UI)
html_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Command Execution</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 50px; }
        form { background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input { margin-bottom: 10px; padding: 10px; width: 300px; }
        button { padding: 10px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <h2>Remote Command Execution Tool (Secure)</h2>
    <form method="POST">
        <label>Command:</label><br>
        <input type="text" name="command" placeholder="Enter command (e.g., ls)" required><br>
        <label>Password:</label><br>
        <input type="password" name="password" placeholder="Enter password" required><br>
        <button type="submit">Execute</button>
    </form>
    <br>
    <div><strong>Output:</strong></div>
    <pre>{{ output }}</pre>
</body>
</html>
"""

# Basic authentication (username/password)


def authenticate(password):
    return USERS.get('admin') == password

# Function to execute the command securely


def execute_command(command):
    # Check if the command is allowed
    if command not in ALLOWED_COMMANDS:
        return "Command not allowed", 400

    try:
        # Execute the command securely without shell=True
        output = subprocess.check_output([command], universal_newlines=True)
        # Log the successful execution
        logging.info(f"Executed command: {command}")
        return output, 200
    except subprocess.CalledProcessError as e:
        # Log any errors
        logging.error(f"Failed to execute command: {
                      command} - Error: {e.output}")
        return f"Command failed with error:\n{e.output}", 500

# Route for the main page with the form


@app.route('/', methods=['GET', 'POST'])
def command_form():
    if request.method == 'POST':
        # Get the command and password from the form
        command = request.form.get('command')
        password = request.form.get('password')

        # Authenticate the user
        if not authenticate(password):
            return "Unauthorized: Invalid password", 403

        # Execute the command securely
        output, _ = execute_command(command)

        # Render the page with the command output
        return render_template_string(html_page, output=output)

    # Render the form without output (initial page)
    return render_template_string(html_page, output="")


if __name__ == '__main__':
    # Running the Flask app in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)
