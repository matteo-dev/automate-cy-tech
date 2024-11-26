// Get references to elements
const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
const clearBtn = document.getElementById('clearBtn');
const colorPicker = document.getElementById('colorPicker'); // Shape color picker
const canvasColorPicker = document.getElementById('canvasColorPicker'); // Canvas background color picker
const addShapeBtn = document.getElementById('addShapeBtn');
const shapeSelect = document.getElementById('shapeSelect');
const cursorXInput = document.getElementById('cursorX');
const cursorYInput = document.getElementById('cursorY');
const sizeInput = document.getElementById('size');

// Default values for drawing properties
let cursorPosition = { x: 0, y: 0 };
let currentColor = "#000000";
ctx.fillStyle = currentColor;
ctx.strokeStyle = currentColor;

// Function to execute drawing commands on the canvas
function executeCommands(commands) {
    commands.forEach(command => {
        switch (command.action) {
            case "cursor":
                cursorPosition.x = command.x;
                cursorPosition.y = command.y;
                break;
            case "set_color":
                currentColor = command.color;
                ctx.strokeStyle = currentColor;
                ctx.fillStyle = currentColor;
                break;
            case "move":
                cursorPosition.x += command.distance;
                break;
            case "draw_shape":
                drawShape(command.shape, command.size);
                break;
            // Additional commands can be added here
        }
    });
}

// Function to draw specific shapes on the canvas
function drawShape(shape, size) {
    ctx.beginPath();
    switch (shape) {
        case "circle":
            ctx.arc(cursorPosition.x, cursorPosition.y, size, 0, Math.PI * 2);
            ctx.fill();
            break;
        case "square":
            ctx.fillRect(cursorPosition.x - size / 2, cursorPosition.y - size / 2, size, size);
            break;
        case "rectangle":
            ctx.fillRect(cursorPosition.x - size, cursorPosition.y - size / 2, size * 2, size);
            break;
        case "line":
            ctx.moveTo(cursorPosition.x, cursorPosition.y);
            ctx.lineTo(cursorPosition.x + size, cursorPosition.y);
            ctx.stroke();
            break;
    }
    ctx.closePath();
}

document.addEventListener('DOMContentLoaded', () => {
    const saveBtn = document.getElementById('saveBtn');
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const titleElement = document.getElementById('title');
            if (!titleElement) {
                console.error("Title input field not found.");
                return;
            }

            const title = titleElement.value || "Untitled";
            const commands = JSON.stringify(getCommands()); // Replace with actual function to get current commands

            // Perform fetch to save the drawing
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
                loadDrawingList(); // Reload the drawing list
            })
            .catch(err => {
                console.error("Error saving drawing:", err);
                alert("An error occurred while saving the drawing. Please try again.");
            });
        });
    } else {
        console.error("Save button not found in the DOM.");
    }
});

// Load Drawing List
function loadDrawingList() {
    fetch('/drawings')
        .then(response => response.json())
        .then(drawings => {
            const drawingList = document.getElementById('drawingList');
            drawingList.innerHTML = ''; // Clear current list
            drawings.forEach(drawing => {
                const li = document.createElement('li');
                li.textContent = `${drawing.title} (${drawing.date_created})`;
                li.addEventListener('click', () => loadDrawing(drawing.id));
                drawingList.appendChild(li);
            });
        });
}

// Load Specific Drawing
function loadDrawing(drawingId) {
    fetch(`/drawing/${drawingId}`)
        .then(response => response.json())
        .then(data => {
            if (data.commands) {
                executeCommands(JSON.parse(data.commands)); // Use existing executeCommands function
            } else {
                alert("Error loading drawing");
            }
        });
}

// Load the drawing list on page load
window.onload = loadDrawingList;

addShapeBtn.addEventListener('click', () => {
    alert("Coucou mec t'as clique sur le bouton")
});

// Clear the canvas on button click
clearBtn.addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvas.style.backgroundColor = "#ffffff"; // Reset canvas background color
});

// Change canvas color based on user selection
canvasColorPicker.addEventListener('input', (e) => {
    canvas.style.backgroundColor = e.target.value;
});

// Collapsible Sidebar Logic
const toggleSidebarBtn = document.createElement('button');
toggleSidebarBtn.id = 'toggleSidebar';
toggleSidebarBtn.textContent = '☰';
toggleSidebarBtn.style.position = 'fixed';
toggleSidebarBtn.style.top = '10px';
toggleSidebarBtn.style.left = '10px';
toggleSidebarBtn.style.zIndex = '1001';
toggleSidebarBtn.style.backgroundColor = '#ff7f50';
toggleSidebarBtn.style.color = 'white';
toggleSidebarBtn.style.border = 'none';
toggleSidebarBtn.style.borderRadius = '5px';
toggleSidebarBtn.style.padding = '10px';
toggleSidebarBtn.style.cursor = 'pointer';
document.body.appendChild(toggleSidebarBtn);

const sidebar = document.getElementById('sidebar');
toggleSidebarBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    if (sidebar.classList.contains('collapsed')) {
        sidebar.style.width = '60px';
        Array.from(sidebar.querySelectorAll('a, h2, ul, p')).forEach(el => el.style.display = 'none');
    } else {
        sidebar.style.width = '300px';
        Array.from(sidebar.querySelectorAll('a, h2, ul, p')).forEach(el => el.style.display = 'block');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    // Get references to the button and inputs
    const addShapeBtn = document.getElementById('addShapeBtn');
    const shapeSelect = document.getElementById('shapeSelect');
    const cursorXInput = document.getElementById('cursorX');
    const cursorYInput = document.getElementById('cursorY');
    const sizeInput = document.getElementById('size');
    const colorPicker = document.getElementById('colorPicker');
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');

    if (addShapeBtn) {
        addShapeBtn.addEventListener('click', () => {
            // Collect user input
            const shape = shapeSelect.value;
            const x = parseInt(cursorXInput.value, 10);
            const y = parseInt(cursorYInput.value, 10);
            const size = parseInt(sizeInput.value, 10);
            const color = colorPicker.value;

            // Validate inputs
            if (isNaN(x) || isNaN(y) || isNaN(size) || size <= 0) {
                alert("Please provide valid values for X, Y, and size (greater than 0).");
                return;
            }

            // Send data to the backend
            fetch('/add_shape', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ shape, x, y, size, color }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        // Draw the shape on the canvas
                        drawShapeOnCanvas(ctx, shape, x, y, size, color);
                        console.log('Shape added successfully:', data);
                    } else {
                        alert(`Error adding shape: ${data.error}`);
                    }
                })
                .catch((err) => {
                    console.error('Request failed:', err);
                    alert('An error occurred while adding the shape.');
                });
        });
    } else {
        console.error("Add Shape button not found in the DOM.");
    }

    // Helper function to draw shapes on the canvas
    function drawShapeOnCanvas(ctx, shape, x, y, size, color) {
        ctx.fillStyle = color;
        ctx.beginPath();

        switch (shape) {
            case 'circle':
                ctx.arc(x, y, size, 0, Math.PI * 2);
                ctx.fill();
                break;
            case 'rectangle':
                ctx.fillRect(x - size / 2, y - size / 2, size * 2, size);
                break;
            case 'square':
                ctx.fillRect(x - size / 2, y - size / 2, size, size);
                break;
            case 'line':
                ctx.moveTo(x, y);
                ctx.lineTo(x + size, y);
                ctx.strokeStyle = color;
                ctx.stroke();
                break;
            default:
                alert("Unknown shape type selected.");
        }

        ctx.closePath();
    }
});
