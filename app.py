from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

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

import ctypes  # For C integration

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
        if result != 0:
            print(f"Error: C function failed with result {result}")
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
    if not shape or not isinstance(x, int) or not isinstance(y, int) or not isinstance(size, int) or not color:
        return jsonify({'success': False, 'error': 'Invalid input data.'}), 400

    if size <= 0:
        return jsonify({'success': False, 'error': 'Size must be greater than 0.'}), 400

    # Call the C function to process the shape
    success = call_c_function(shape, x, y, size, color)

    if success:
        return jsonify({'success': True, 'message': f'{shape} added successfully!'})
    else:
        return jsonify({'success': False, 'error': 'Failed to add shape.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
