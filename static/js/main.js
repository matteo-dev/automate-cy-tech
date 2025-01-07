// Main.js - Orchestrates application logic and initializes modules

import { clearCanvas, drawShapeOnCanvas, updateCanvas, updateCanvasBackgroundColor, takeCanvasScreenshot } from './canvas.js';
import { parseCommand, validateCommands, processCommands, renderHighlightedCode } from './commands.js';
import { saveDrawing, loadDrawingList, loadDrawing, applyDrawCode, addShape } from './fetchHandlers.js';
import { toggleSidebar, initializeSidebar } from './sidebar.js';

// Default state for cursor and color
let cursorPosition = { x: 0, y: 0 };
let currentColor = "#000000";

// Event listeners for canvas controls
function initializeCanvasControls() {
    const clearBtn = document.getElementById('clearBtn');
    const colorPicker = document.getElementById('colorPicker');
    const canvasColorPicker = document.getElementById('canvasColorPicker');
    const addShapeBtn = document.getElementById('addShapeBtn');
    const takeScreenshotBtn = document.getElementById('takeasaveBtn');

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            clearCanvas();
        });
    }

    if (colorPicker) {
        colorPicker.addEventListener('input', (event) => {
            currentColor = event.target.value;
        });
    }

    if (canvasColorPicker) {
        canvasColorPicker.addEventListener('input', (event) => {
            updateCanvasBackgroundColor(event.target.value);
        });
    }

    if (addShapeBtn) {
        addShapeBtn.addEventListener('click', () => {
            const shapeSelect = document.getElementById('shapeSelect');
            const cursorXInput = document.getElementById('cursorX');
            const cursorYInput = document.getElementById('cursorY');
            const sizeInput = document.getElementById('size');

            const shapeData = {
                shape: shapeSelect.value,
                x: parseInt(cursorXInput.value, 10),
                y: parseInt(cursorYInput.value, 10),
                size: parseInt(sizeInput.value, 10),
                color: currentColor
            };

            addShape(shapeData);
        });
    }

    if (takeScreenshotBtn) {
        takeScreenshotBtn.addEventListener('click', () => {
            takeCanvasScreenshot();
        });
    }
}

// Event listener for the Draw++ code editor
function initializeCodeEditor() {
    const applyCodeBtn = document.getElementById('applyCodeBtn');
    const codeInput = document.getElementById('codeEditor');
    const highlightedCode = document.getElementById('highlightedCode');

    if (applyCodeBtn && codeInput) {
        applyCodeBtn.addEventListener('click', () => {
            const drawCode = codeInput.value;

            const errors = validateCommands(drawCode.split('\n'));
            if (errors.length > 0) {
                alert(`Validation Errors:\n${errors.join('\n')}`);
                return;
            }

            applyDrawCode(drawCode);
        });

        codeInput.addEventListener('input', () => {
            const code = codeInput.value;
            const errors = validateCommands(code.split('\n'));

            if (highlightedCode) {
                highlightedCode.innerHTML = renderHighlightedCode(code, errors);
            }
        });
    }
}

// Tab Switching Logic
function initializeTabSwitching() {
    const tabEditor = document.getElementById('tab-editor');
    const tabCanvas = document.getElementById('tab-canvas');
    const editorContent = document.getElementById('editor-content');
    const canvasContent = document.getElementById('canvas-content');

    if (tabEditor && tabCanvas && editorContent && canvasContent) {
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
    } else {
        console.error("Tab elements not found. Check your HTML structure.");
    }
}

// Initialize the application
function initializeApp() {
    initializeSidebar();
    initializeCanvasControls();
    initializeCodeEditor();
    initializeTabSwitching();
    loadDrawingList();
}

// Start the app when DOM is ready
document.addEventListener('DOMContentLoaded', initializeApp);
