from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from datetime import datetime
import ctypes  # For C integration

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('drawings.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drawings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            date_created TEXT,
            commands TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Serve the main HTML interface
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to serve the drawing tool page
@app.route('/drawing_tool')
def drawing_tool():
    return render_template('drawing_tool.html')

# Save a drawing to the database
@app.route('/save', methods=['POST'])
def save_drawing():
    data = request.json
    title = data.get("title", "Untitled")
    commands = data.get("commands")
    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('drawings.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO drawings (title, date_created, commands) VALUES (?, ?, ?)', 
                   (title, date_created, commands))
    conn.commit()
    conn.close()

    return jsonify({"message": "Drawing saved successfully!"})

# Retrieve all saved drawings
@app.route('/drawings', methods=['GET'])
def get_drawings():
    conn = sqlite3.connect('drawings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, date_created FROM drawings')
    drawings = cursor.fetchall()
    conn.close()

    drawings_list = [{"id": row[0], "title": row[1], "date_created": row[2]} for row in drawings]
    return jsonify(drawings_list)

# Load a specific drawing by ID
@app.route('/drawing/<int:drawing_id>', methods=['GET'])
def load_drawing(drawing_id):
    conn = sqlite3.connect('drawings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT commands FROM drawings WHERE id = ?', (drawing_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({"commands": row[0]})
    else:
        return jsonify({"error": "Drawing not found"}), 404

# C integration
def call_c_function(shape, x, y, size, color):
    try:
        print(f"Calling C function with: {shape}, {x}, {y}, {size}, {color}")
        lib = ctypes.CDLL('./drawlib.so')
        lib.draw_shape.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
        lib.draw_shape.restype = ctypes.c_int
        result = lib.draw_shape(shape.encode('utf-8'), x, y, size, color.encode('utf-8'))
        print(f"C function result: {result}")
        return result == 0  # Return True if success
    except Exception as e:
        print("Error calling C function:", e)
        return False

# Flask route for adding a shape
@app.route('/add_shape', methods=['POST'])
def add_shape():
    data = request.get_json()

    # Extract data from the received request
    shape = data.get('shape')
    x = data.get('x')
    y = data.get('y')
    size = data.get('size')
    color = data.get('color')

    # Validate the inputs
    # Validate general inputs
    if not shape or not isinstance(x, int) or not isinstance(y, int) or not isinstance(size, int) or not color:
        return jsonify({'success': False, 'error': 'Invalid input data.'}), 400

    if size <= 0:
        return jsonify({'success': False, 'error': 'Size must be greater than 0.'}), 400

    # Add shape-specific checks only if needed
    if shape == "circle":
        radius = size
        if not (radius <= x <= 800 - radius) or not (radius <= y <= 600 - radius):
            return jsonify({'success': False, 'error': 'Circle must fit within the canvas.'}), 400

    elif shape == "rectangle":
        # Extract width and height from the request
        width = data.get('width')
        height = data.get('height')

        # Ensure width and height are provided and are greater than 0
        if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
            return jsonify({'success': False, 'error': 'Rectangle width and height must be greater than 0.'}), 400

        # Optional: Ensure the rectangle fits within the canvas bounds
        canvas_width = 800  # Replace with your actual canvas width
        canvas_height = 600  # Replace with your actual canvas height
        if not (0 <= x <= canvas_width - width) or not (0 <= y <= canvas_height - height):
            return jsonify({'success': False, 'error': 'Rectangle must fit within the canvas.'}), 400

    # Call the C function to process the shape
    success = call_c_function(shape, x, y, size, color)

    if success:
        # Save the Draw++ command in the file
        draw_command = f"{shape} {x} {y} {size} {color}\n"
        with open('static/draw_code.drawpp', 'a') as file:
            file.write(draw_command)
        return jsonify({'success': True, 'message': f'{shape} added successfully!'})
    else:
        return jsonify({'success': False, 'error': 'Failed to add shape.'}), 500

# File path for Draw++ code
CODE_FILE_PATH = "static/draw_code.drawpp"

# Function to initialize the code file if not present
def init_code_file():
    try:
        if not os.path.exists(CODE_FILE_PATH):
            with open(CODE_FILE_PATH, 'w') as file:
                file.write("// Write your Draw++ code here\n")
    except Exception as e:
        print(f"Error initializing code file: {e}")

# Route for code editor
@app.route('/code-editor', methods=['GET', 'POST'])
def code_editor():
    try:
        # Initialize file if not present
        init_code_file()

        # Handle GET request
        if request.method == 'GET':
            with open(CODE_FILE_PATH, 'r') as file:
                current_code = file.read()
            return render_template('code_editor.html', code=current_code)

        # Handle POST request
        if request.method == 'POST':
            updated_code = request.form.get('draw_code', '').strip()

            # Validate the code (basic validation example)
            if not updated_code:
                return jsonify({"success": False, "error": "Code cannot be empty."}), 400

            # Save the updated code to file
            with open(CODE_FILE_PATH, 'w') as file:
                file.write(updated_code)

            return jsonify({"success": True, "message": "Code saved successfully."})

    except Exception as e:
        print(f"Error in /code-editor route: {e}")
        return jsonify({"success": False, "error": "An error occurred while processing your request."}), 500

# Route to apply Draw++ code and update the canvas
@app.route('/apply-draw-code', methods=['POST'])
def apply_draw_code():
    data = request.json
    draw_code = data.get("draw_code")

    if not draw_code:
        return jsonify({'success': False, 'error': 'No Draw++ code provided.'}), 400

    try:
        commands = []  # Parsed commands for the canvas
        cursor_position = {"x": 0, "y": 0}  # Default cursor position
        current_color = "#000000"  # Default color

        for line in draw_code.strip().split('\n'):
            parts = line.strip().split()
            command = parts[0].lower()

            if command == "cursor":
                cursor_position = {"x": int(parts[1]), "y": int(parts[2])}
            elif command == "set_color":
                current_color = parts[1]
            elif command in ["circle", "square", "rectangle", "line"]:
                x = cursor_position["x"]
                y = cursor_position["y"]
                size = int(parts[1])
                color = current_color

                if command == "circle":
                    commands.append({"shape": "circle", "x": x, "y": y, "size": size, "color": color})
                elif command == "square":
                    commands.append({"shape": "square", "x": x, "y": y, "size": size, "color": color})
                elif command == "rectangle":
                    commands.append({"shape": "rectangle", "x": x, "y": y, "size": size, "color": color})
                elif command == "line":
                    commands.append({"shape": "line", "x": x, "y": y, "size": size, "color": color})
            elif command == "move_cursor":
                cursor_position["x"] += int(parts[1])
                cursor_position["y"] += int(parts[2])
            elif command == "rotate_cursor":
                pass  # Future implementation: handle rotation logic

        return jsonify({'success': True, 'commands': commands})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

def validate_command(command: str) -> str:
    """
    Validates a single Draw++ command string.
    Returns an error message if invalid; otherwise, returns None.
    """
    valid_commands = {
        "cursor": {"args": 2, "type": "int", "range": (-10000, 10000)},  # Allow negatives
        "set_color": {"args": 1, "type": "color"},  # Validate hex colors
        "circle": {"args": 1, "type": "int", "range": (1, float("inf"))},  # Positive radius
        "square": {"args": 1, "type": "int", "range": (1, float("inf"))},  # Positive size
        "rectangle": {"args": 2, "type": "int", "range": (1, float("inf"))},  # Positive dimensions
        "line": {"args": 1, "type": "int", "range": (1, float("inf"))},  # Positive length
        "move_cursor": {"args": 2, "type": "int", "range": (-10000, 10000)},  # Allow negatives
    }

    parts = command.split()
    if not parts:
        return "Empty command."

    cmd_name = parts[0]
    if cmd_name not in valid_commands:
        return f"Invalid command '{cmd_name}'. Valid commands are: {list(valid_commands.keys())}."

    args = parts[1:]
    cmd_rules = valid_commands[cmd_name]

    if len(args) != cmd_rules["args"]:
        return f"'{cmd_name}' expects {cmd_rules['args']} arguments, but got {len(args)}."

    for i, arg in enumerate(args):
        if cmd_rules["type"] == "int":
            try:
                value = int(arg)
                if not (cmd_rules["range"][0] <= value <= cmd_rules["range"][1]):
                    return f"Argument '{arg}' in '{cmd_name}' must be in range {cmd_rules['range']}."
            except ValueError:
                return f"Argument '{arg}' in '{cmd_name}' must be an integer."
        elif cmd_rules["type"] == "color":
            if not (arg.startswith("#") and len(arg) == 7 and all(c in "0123456789ABCDEFabcdef" for c in arg[1:])):
                return f"Invalid color code '{arg}' in '{cmd_name}'. Use format '#RRGGBB'."

    return None  # No errors


def validate_commands(commands: list[str]) -> list[str]:
    """
    Validates a list of Draw++ commands.
    Returns a list of error messages, one for each invalid command.
    """
    errors = []
    for i, command in enumerate(commands):
        error = validate_command(command)
        if error:
            errors.append(f"line {i + 1}: {error}")
    return errors


@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    draw_code = data.get("commands", "")
    commands = draw_code.split("\n")

    # Validate commands
    errors = validate_commands(commands)

    print("Received Commands:", commands)  # Debugging
    print("Validation Errors:", errors)   # Debugging

    if errors:  # If there are errors, return them
        return jsonify({"success": False, "errors": errors}), 400

    # If no errors, log success
    return jsonify({"success": True, "message": "Draw++ code applied successfully!"})
