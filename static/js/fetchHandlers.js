// FetchHandlers.js - Handles backend communication for Draw++

// Import dependencies
import { updateCanvas, drawShapeOnCanvas } from './canvas.js';
import { processCommands } from './commands.js';

// Save a drawing to the backend
function saveDrawing(title, commands) {
    fetch('/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, commands })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            loadDrawingList(); // Refresh the list of saved drawings
        })
        .catch(err => {
            console.error("Error saving drawing:", err);
            alert("An error occurred while saving the drawing. Please try again.");
        });
}

// Load all saved drawings
function loadDrawingList() {
    fetch('/drawings')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(drawings => {
            const drawingList = document.getElementById('drawingList');
            if (drawingList) {
                drawingList.innerHTML = ''; // Clear current list
                drawings.forEach(drawing => {
                    const li = document.createElement('li');
                    li.textContent = `${drawing.title} (${drawing.date_created})`;
                    li.addEventListener('click', () => loadDrawing(drawing.id));
                    drawingList.appendChild(li);
                });
            } else {
                console.error("Drawing list element not found in the DOM.");
            }
        })
        .catch(err => console.error("Error loading drawing list:", err));
}

// Load a specific drawing by ID
function loadDrawing(drawingId) {
    fetch(`/drawing/${drawingId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.commands) {
                const commands = JSON.parse(data.commands);
                updateCanvas(commands); // Update the canvas with the fetched commands
            } else {
                alert("Error loading drawing. Commands not found.");
            }
        })
        .catch(err => console.error("Error loading drawing:", err));
}

// Apply Draw++ code from the editor
function applyDrawCode(drawCode) {
    console.log("Sending Draw++ Code to Backend:", drawCode);

    fetch('/apply-draw-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ draw_code: drawCode })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.error);
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            updateCanvas(data.commands);
            alert("Draw++ code applied successfully!");
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error("Error applying Draw++ code:", error.message);
        alert(`Error: ${error.message}`);
    });
}


// Add a shape via the backend
function addShape(shapeData) {
    fetch('/add_shape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(shapeData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert(data.message);
                drawShapeOnCanvas(
                    shapeData.shape,
                    shapeData.x,
                    shapeData.y,
                    shapeData.size,
                    shapeData.color
                );
            } else {
                alert(`Error: ${data.error}`);
            }
        })
        .catch(err => console.error("Error adding shape:", err));
}

export { saveDrawing, loadDrawingList, loadDrawing, applyDrawCode, addShape };
