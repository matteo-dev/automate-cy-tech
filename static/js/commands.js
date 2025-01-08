// Commands.js - Handles Draw++ commands parsing and execution

// Global States
let cursorPosition = { x: 0, y: 0 }; // Default cursor position
let currentColor = "#000000"; // Default color

// Import dependencies
import { updateCanvas, drawShapeOnCanvas } from './canvas.js';
import { loadDrawingList } from './fetchHandlers.js';

// Parses individual Draw++ command
function parseCommand(command) {
    const parts = command.trim().split(" ");
    const cmdName = parts[0];

    switch (cmdName) {
        case "cursor":
            return { action: "cursor", x: parseInt(parts[1], 10), y: parseInt(parts[2], 10) };
        case "set_color":
            return { action: "set_color", color: parts[1] };
        case "circle":
        case "square":
            return {
                action: "draw_shape",
                shape: cmdName,
                x: cursorPosition.x,
                y: cursorPosition.y,
                size: parseInt(parts[1], 10),
                color: currentColor
            };
        case "rectangle":
            return {
                action: "draw_shape",
                shape: "rectangle",
                x: cursorPosition.x,
                y: cursorPosition.y,
                width: parseInt(parts[1], 10),
                height: parseInt(parts[2], 10),
                color: currentColor
            };
        case "line":
            return {
                action: "draw_shape",
                shape: "line",
                x: cursorPosition.x,
                y: cursorPosition.y,
                length: parseInt(parts[1], 10),
                color: currentColor
            };
        case "move_cursor":
            return { action: "move_cursor", dx: parseInt(parts[1], 10), dy: parseInt(parts[2], 10) };
        case "rotate_cursor":
            return { action: "rotate_cursor", angle: parseInt(parts[1], 10) };
        default:
            console.error(`Unknown command: ${cmdName}`);
            return null;
    }
}

// Validates a single command for correctness
function validateCommand(command, lineNumber) {
    const parts = command.trim().split(" ");
    const cmdName = parts[0];

    const validCommands = {
        "cursor": { args: 2, type: "int" },
        "set_color": { args: 1, type: "color" },
        "circle": { args: 1, type: "int" },
        "square": { args: 1, type: "int" },
        "rectangle": { args: 2, type: "int" },
        "line": { args: 1, type: "int" },
        "move_cursor": { args: 2, type: "int" },
        "rotate_cursor": { args: 1, type: "int" },
    };

    if (!validCommands[cmdName]) {
        return `line ${lineNumber}: Unknown command '${cmdName}'.`;
    }

    const cmdRules = validCommands[cmdName];
    const args = parts.slice(1);

    if (args.length !== cmdRules.args) {
        return `line ${lineNumber}: '${cmdName}' expects ${cmdRules.args} arguments, but got ${args.length}.`;
    }

    if (cmdRules.type === "int") {
        for (let arg of args) {
            if (isNaN(parseInt(arg, 10))) {
                return `line ${lineNumber}: Argument '${arg}' must be an integer.`;
            }
        }
    } else if (cmdRules.type === "color") {
        const color = args[0];
        if (!/^#[0-9A-Fa-f]{6}$/.test(color)) {
            return `line ${lineNumber}: Invalid color code '${color}'. Use format '#RRGGBB'.`;
        }
    }

    return null; // Valid command
}


//Function to save a page
function savePage() {
    // Extract HTML content
    const pageContent = document.documentElement.outerHTML;

    // Send HTML content to flask
    fetch('/save_page', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ html: pageContent }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        alert(`Page sauvegardée avec succès ! Fichier : ${data.path}`);
    })
    .catch(error => {
        console.error('Erreur lors de la sauvegarde de la page :', error);
        alert('Une erreur est survenue lors de la sauvegarde de la page.');
    });
}
document.getElementById('save-file').addEventListener('click', savePage);

// Validates all commands and returns an array of error messages
function validateCommands(commands) {
    const errors = [];
    commands.forEach((command, index) => {
        const error = validateCommand(command, index + 1);
        if (error) errors.push(error);
    });
    return errors;
}

// Processes valid commands into actionable objects
function processCommands(commands) {
    const processedCommands = [];

    commands.forEach(command => {
        const parsedCommand = parseCommand(command);
        if (parsedCommand) {
            // Update cursor position or current color dynamically
            if (parsedCommand.action === "cursor") {
                cursorPosition = { x: parsedCommand.x, y: parsedCommand.y };
            } else if (parsedCommand.action === "set_color") {
                currentColor = parsedCommand.color;
            } else if (parsedCommand.action === "move_cursor") {
                cursorPosition.x += parsedCommand.dx;
                cursorPosition.y += parsedCommand.dy;
            }

            // Add processed command to the list
            processedCommands.push(parsedCommand);
        }
    });

    return processedCommands;
}

// Highlights errors in the Draw++ code editor
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

    return highlighted;
}

export { parseCommand, validateCommands, processCommands, renderHighlightedCode };
