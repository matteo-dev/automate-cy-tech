// Get references to elements
const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
const clearBtn = document.getElementById('clearBtn');
const colorPicker = document.getElementById('colorPicker');
const canvasColorPicker = document.getElementById('canvasColorPicker');
const addShapeBtn = document.getElementById('addShapeBtn');
const shapeSelect = document.getElementById('shapeSelect');
const cursorXInput = document.getElementById('cursorX');
const cursorYInput = document.getElementById('cursorY');
const sizeInput = document.getElementById('size');
const applyCodeBtn = document.getElementById('applyCodeBtn');
const element = document.getElementById('drawingCanvas'); 

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

// Function to apply Draw++ code from the editor
function applyDrawCode() {
    const drawCode = document.getElementById('codeEditor').value;

    fetch('/apply-draw-code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ draw_code: drawCode }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Commands received from server:", data.commands);
                updateCanvas(data.commands); // Update the canvas with parsed commands
                alert("Draw++ code applied successfully!");
            } else {
                console.error('Error applying Draw++ code:', data.error);
                alert("Error: " + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while applying the Draw++ code.');
        });
}

// Tab Switching Logic
const tabEditor = document.getElementById('tab-editor');
const tabCanvas = document.getElementById('tab-canvas');
const editorContent = document.getElementById('editor-content');
const canvasContent = document.getElementById('canvas-content');

tabEditor.addEventListener('click', () => {
    tabEditor.classList.add('active');
    tabCanvas.classList.remove('active');
    editorContent.classList.add('active');
    canvasContent.classList.remove('active');
});

tabCanvas.addEventListener('click', () => {
    tabCanvas.classList.add('active');
    tabEditor.classList.remove('active');
    canvasContent.classList.add('active');
    editorContent.classList.remove('active');
});

// Attach event listener to the Apply Code button\
if(applyCodeBtn){
    applyCodeBtn.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent form submission and page reload
        applyDrawCode(); // Call the function to apply Draw++ code
    }); 
}

// Apply Code Button Logic
applyCodeBtn.addEventListener('click', () => {
    const code = document.getElementById('codeEditor').value;

    fetch('/apply-draw-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ draw_code: code }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Code applied successfully!');
                updateCanvas(data.commands);
                tabCanvas.click(); // Switch to Canvas tab
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(err => {
            console.error('Error:', err);
            alert('Failed to apply code.');
        });
});

// Update Canvas Function
function updateCanvas(commands) {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

    commands.forEach(command => {
        const { shape, x, y, size, color } = command;
        ctx.fillStyle = color;
        ctx.beginPath();
        if (shape === 'circle') {
            ctx.arc(x, y, size, 0, 2 * Math.PI);
            ctx.fill();
        } else if (shape === 'square') {
            ctx.fillRect(x, y, size, size);
        } else if (shape === 'line') {
            ctx.moveTo(x, y);
            ctx.lineTo(x + size, y); // Example line
            ctx.strokeStyle = color;
            ctx.stroke();
        }
        ctx.closePath();
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const addShapeBtn = document.getElementById('addShapeBtn');
    
    if (addShapeBtn) {
        addShapeBtn.addEventListener('click', () => {
            const shape = shapeSelect.value;
            const x = parseInt(cursorXInput.value, 10);
            const y = parseInt(cursorYInput.value, 10);
            const size = parseInt(sizeInput.value, 10);
            const color = colorPicker.value;

            console.log({ shape, x, y, size, color });

            fetch('/add_shape', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ shape, x, y, size, color }),
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                console.log("Commands received:", data.commands);
                if (data.success) {
                    alert(data.message);
                } else {
                    alert("Error: " + data.error);
                }
            })
            .catch(err => console.error("Request failed:", err));
        });
    } else {
        console.log('Add Shape button not found.');
    }
});

// Button to take a capture like a save 
takeasaveBtn.addEventListener('click', () => {
    html2canvas(element).then(canvas => {
        // Convertir le canvas en image
        const screenshot = canvas.toDataURL('image/png');

        // Créer un lien pour télécharger l'image
        const link = document.createElement('a');
        link.href = screenshot;
        link.download = 'save.png';
        link.click();
    }).catch(err => {
        console.error('Erreur lors de la capture de l\'écran :', err);
    });
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

document.addEventListener('DOMContentLoaded', function () {
    const addShapeBtn = document.getElementById('addShapeBtn');
    const shapeSelect = document.getElementById('shapeSelect');
    const cursorXInput = document.getElementById('cursorX');
    const cursorYInput = document.getElementById('cursorY');
    const sizeInput = document.getElementById('size');
    const colorPicker = document.getElementById('colorPicker');
    
    if (addShapeBtn) {
        addShapeBtn.addEventListener('click', () => {
            const shape = shapeSelect.value;
            const x = parseInt(cursorXInput.value, 10);
            const y = parseInt(cursorYInput.value, 10);
            const size = parseInt(sizeInput.value, 10);
            const color = colorPicker.value;

            // Print shape data to debug
            console.log("Sending data to server:", { shape, x, y, size, color });

            // Send shape data to the server
            fetch('/add_shape', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ shape, x, y, size, color }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);  // Success alert
                    // After success, draw shape on canvas
                    drawShapeOnCanvas(shape, x, y, size, color); 
                } else {
                    alert("Error: " + data.error);  // Error message
                }
            })
            .catch(err => console.error("Request failed:", err));
        });
    }
});

// Function to update the canvas with the new shape
function drawShapeOnCanvas(shape, x, y, size, color) {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = color;
    ctx.strokeStyle = color;
    ctx.beginPath();

    switch (shape) {
        case "circle":
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();
            break;
        case "square":
            ctx.fillRect(x - size / 2, y - size / 2, size, size);
            break;
        case "rectangle":
            ctx.fillRect(x - size, y - size / 2, size * 2, size);
            break;
        case "line":
            ctx.moveTo(x, y);
            ctx.lineTo(x + size, y);
            ctx.stroke();
            break;
        default:
            console.error(`Unknown shape: ${shape}`);
    }

    ctx.closePath();
}

//Function that applies commands received from the server or a saved drawing.
function executeCommands(commands) {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
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
            case "draw_shape":
                drawShapeOnCanvas(command.shape, command.x, command.y, command.size, command.color);
                break;
            default:
                console.error(`Unknown command action: ${command.action}`);
        }
    });
}

document.getElementById("applyCodeButton").addEventListener("click", () => {
    const code = document.getElementById("codeInput").value;

    fetch("/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ commands: code })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);  // Show success message
        } else {
            alert("Errors:\n" + data.errors.join("\n"));  // Show validation errors
        }
    })
    .catch(error => console.error("Error:", error));
});

document.addEventListener("DOMContentLoaded", () => {
    const applyCodeButton = document.getElementById("applyCodeButton");
    if (applyCodeButton) {
        applyCodeButton.addEventListener("click", () => {
            const drawCode = document.getElementById("codeInput").value;
            fetch("/execute", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ commands: drawCode })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                } else {
                    alert("Errors:\n" + data.errors.join("\n"));
                }
            })
            .catch(error => console.error("Error:", error));
        });
    } else {
        console.error("Apply Code button not found in the DOM.");
    }
});

applyCodeButton.addEventListener("click", () => {
    const code = codeInput.value;

    fetch("/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ commands: code })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            // Highlight errors
            const validCommands = renderHighlightedCode(code, data.errors);

            // Only process valid commands
            console.log("Valid commands:", validCommands);
            if (validCommands.length > 0) {
                processValidCommands(validCommands);
            }
        } else {
            console.log("All commands are valid!");
            processValidCommands(code.split("\n"));
        }
    })
    .catch(error => console.error("Error:", error));
});

document.addEventListener("DOMContentLoaded", () => {
    const codeInput = document.getElementById("codeInput");
    const highlightedCode = document.getElementById("highlightedCode");

    codeInput.addEventListener("input", () => {
        const code = codeInput.value;

        // Send code to the backend for validation
        fetch("/execute", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ commands: code })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderHighlightedCode(code, []); // No errors
            } else {
                renderHighlightedCode(code, data.errors); // Pass errors
            }
        })
        .catch(error => console.error("Error:", error));
    });

    function renderHighlightedCode(code, errors) {
        const lines = code.split("\n");
        let highlighted = "";

        lines.forEach((line, index) => {
            const error = errors.find(err => err.includes(`line ${index + 1}`));
            if (error) {
                highlighted += `<span class="error">${line}</span>\n`;
            } else {
                highlighted += `${line}\n`;
            }
        });

        highlightedCode.innerHTML = highlighted;
    }
});


function renderHighlightedCode(code, errors) {
    const lines = code.split("\n");
    let highlighted = "";

    console.log("Errors Received from Backend:", errors); // Debugging

    lines.forEach((line, index) => {
        const error = errors.find(err => err.includes(`line ${index + 1}`));
        if (error) {
            console.log(`Highlighting Error in Line ${index + 1}:`, line); // Debugging
            highlighted += `<span class="error">${line}</span>\n`; // Highlight invalid line
        } else {
            highlighted += `${line}\n`; // Keep valid line normal
        }
    });

    console.log("Highlighted Content:", highlighted); // Debugging

    // Update the highlighted div
    highlightedCode.innerHTML = highlighted;

    // Sync the height of the textarea with the div
    highlightedCode.style.height = `${codeInput.scrollHeight}px`;
}

function processValidCommands(commands) {
    // Send valid commands to the canvas logic
    console.log("Processing valid commands:", commands);
    // Example: Add your canvas drawing logic here
}
