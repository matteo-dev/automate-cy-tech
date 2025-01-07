// Canvas.js - Handles all canvas-related functionality

// Import dependencies
import { processCommands } from './commands.js';
import { loadDrawingList } from './fetchHandlers.js';

// Constants and References
const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');

// Default values for drawing properties
let currentColor = "#000000";
ctx.fillStyle = currentColor;
ctx.strokeStyle = currentColor;

// Clears the canvas and resets the background
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvas.style.backgroundColor = "#ffffff"; // Default canvas background
}

// Draws a shape on the canvas
function drawShapeOnCanvas(shape, x, y, size, color) {
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
            ctx.fillRect(x, y, size.width, size.height);
            break;
        case "line":
            ctx.moveTo(x, y);
            ctx.lineTo(x + size, y); // Example horizontal line
            ctx.stroke();
            break;
        default:
            console.error(`Unknown shape: ${shape}`);
    }

    ctx.closePath();
}

// Updates the canvas with commands parsed from the backend
function updateCanvas(commands) {
    clearCanvas();
    commands.forEach(command => {
        const { shape, x, y, size, color } = command;
        drawShapeOnCanvas(shape, x, y, size, color);
    });
}

// Updates the canvas background color
function updateCanvasBackgroundColor(color) {
    canvas.style.backgroundColor = color;
}

// Takes a screenshot of the canvas and allows the user to save it
function takeCanvasScreenshot() {
    if (!canvas) {
        console.error('Canvas not found for screenshot.');
        return;
    }

    html2canvas(canvas).then((canvasImage) => {
        const link = document.createElement('a');
        link.href = canvasImage.toDataURL('image/png');
        link.download = 'drawing_screenshot.png';
        link.click();
    }).catch((err) => {
        console.error('Error taking screenshot:', err);
        alert('Failed to take a screenshot of the canvas.');
    });
}

// Validates whether a shape can fit within the canvas bounds
function validateShapeBounds(shape, x, y, size) {
    if (shape === "circle" || shape === "square") {
        return x - size >= 0 && x + size <= canvas.width && y - size >= 0 && y + size <= canvas.height;
    } else if (shape === "rectangle") {
        return x >= 0 && x + size.width <= canvas.width && y >= 0 && y + size.height <= canvas.height;
    } else if (shape === "line") {
        return x >= 0 && x + size <= canvas.width && y >= 0 && y <= canvas.height;
    }
    return true;
}

// Export functions for use in other modules
export { 
    clearCanvas, 
    drawShapeOnCanvas, 
    updateCanvas, 
    updateCanvasBackgroundColor, 
    takeCanvasScreenshot, 
    validateShapeBounds 
};
