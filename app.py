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

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/add_shape', methods=['POST'])
def add_shape():
    data = request.get_json()

    # Debug: Log received data
    print("Received data:", data)

    # Extract data
    shape = data.get('shape')
    x = data.get('x')
    y = data.get('y')
    size = data.get('size')
    color = data.get('color')

    # Validate inputs
    if not all([shape, isinstance(x, int), isinstance(y, int), isinstance(size, int), color]):
        return jsonify({'success': False, 'error': 'Invalid input data.'})

    if size <= 0:
        return jsonify({'success': False, 'error': 'Size must be greater than 0.'})

    # Process and respond
    # (Here, you can add code to store the shape data in the database if needed)
    print(f"Shape added: {shape}, Position: ({x}, {y}), Size: {size}, Color: {color}")
    return jsonify({'success': True, 'message': 'Shape added successfully!'})
