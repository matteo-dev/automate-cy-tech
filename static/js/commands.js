// Commands.js - Handles Draw++ commands parsing and execution
 
// Global States
let cursorPosition = { x: 0, y: 0 }; // Default cursor position
let currentColor = "#000000"; // Default color

// Import dependencies
import { updateCanvas, drawShapeOnCanvas } from './canvas.js';
import { loadDrawingList } from './fetchHandlers.js';

// Validates all commands and returns an array of error messages
function validateCommands(commands) {
    const errors = [];
    const context = {}; // Initialize shared context object

    commands.forEach((command, index) => {
        const error = validateCommand(command, index + 1, context); // Pass context to each command
        if (error) errors.push(error);
    });

    return errors; // Return all validation errors
}


// Validates a single command for correctness
function validateCommand(command, lineNumber, context = {}) {
    const parts = command.trim().split(" ");
    const cmdName = parts[0];

    const validCommands = {
        "cursor": { args: "dynamic", type: "int" },
        "set_color": { args: 1, type: "color" },
        "circle": { args: 1, type: "int" },
        "square": { args: 1, type: "int" },
        "rectangle": { args: 2, type: "int" },
        "line": { args: 1, type: "int" },
        "move_cursor": { args: 2, type: "int" },
        "rotate_cursor": { args: 1, type: "int" },
        "for": { args: 3, type: "loop" }, // Custom handling for loops
        "while": { args: 3, type: "condition" }, // Custom handling for conditions
        "" : { args: 0, type: "separator"},
        "{": { args: 0, type: "block_start" },
        "}": { args: 0, type: "block_end" },
        "from": { args: 1, type: "range_start" },
        "to": { args: 1, type: "range_end" },
        ",": { args: 0, type: "separator" }
    };

    // Check if command is valid
    if (!validCommands[cmdName]) {
        return `line ${lineNumber}: Unknown command '${cmdName}'.`;
    }

    const cmdRules = validCommands[cmdName];
    const args = parts.slice(1);

    // Handle 'for' command to add loop variable to context
    if (cmdName === "for") {
        if (parts.length < 6 || parts[2] !== "from" || parts[4] !== "to") {
            throw new Error(`Invalid 'for' loop syntax on line ${lineNumber}`);
        }
        // Validate range values
        const start = parseInt(parts[3], 10);
        const end = parseInt(parts[5], 10);
        if (isNaN(start) || isNaN(end)) {
            throw new Error(`Invalid range in 'for' loop on line ${lineNumber}`);
        }
        return; // Command is valid
    }  

    if (cmdName === "while") {
        const condition = parts.slice(1).join(" "); // Extract the condition
        if (!condition.includes("cursor[") || !condition.includes("]")) {
            return `line ${lineNumber}: Invalid 'while' condition. Expected condition with 'cursor["key"]'.`;
        }
        // Optional: Add more checks for the condition format
        return null; // Command is valid
    }
    

    if (cmdName === "{" || cmdName === "}") {
        return; // Block delimiters are valid
    }    

    // Check argument count
    if (cmdRules.args === "dynamic") {
        if (args.length < 2) {
            return `line ${lineNumber}: '${cmdName}' expects at least 2 arguments, but got ${args.length}.`;
        }
    } else if (args.length < cmdRules.args) {
        return `line ${lineNumber}: '${cmdName}' expects ${cmdRules.args} arguments, but got ${args.length}.`;
    }

    // Validate argument types
    if (cmdRules.type === "int") {
        for (let arg of args) {
            if (isNaN(parseInt(arg, 10)) && !(arg in context)) {
                return `line ${lineNumber}: Argument '${arg}' must be an integer or a valid variable defined in the context.`;
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


// Processes valid commands into actionable objects
function processCommands(parsedCommand, context = {}) {
    switch (parsedCommand.action) {
        case "cursor":
            cursorPosition.x = parsedCommand.x;
            cursorPosition.y = parsedCommand.y;
            break;
        case "set_color":
            currentColor = parsedCommand.color;
            break;
        case "draw_shape":
            drawShapeOnCanvas(parsedCommand.shape, parsedCommand.x, parsedCommand.y, parsedCommand.size, parsedCommand.color);
            break;
        case "loop":
            for (let i = parsedCommand.start; i <= parsedCommand.end; i++) {
                context[parsedCommand.variable] = i; // Add loop variable to context
                const nestedCommands = parsedCommand.body.split(";"); // Split nested commands
                for (const nestedCommand of nestedCommands) {
                        processCommands(parseCommand(nestedCommand), context);
                    }
            }
            break;
            
        case "while":
            // Dynamically evaluate the condition
            const conditionFunction = new Function("cursor", "context", `return ${parsedCommand.condition}`);
            
            while (conditionFunction(cursorPosition, context)) {
                    const nestedCommands = parsedCommand.body.split(";"); // Split body into commands
                    nestedCommands.forEach(nestedCommand => {
                        const parsedNestedCommand = parseCommand(nestedCommand.trim());
                        processCommands(parsedNestedCommand, context); // Recursively process each command
                    });
                }

             break;
            

        case "block_start":
            console.log("Block start detected");
            break;
        case "block_end":
            console.log("Block end detected");
            break;


        default:
            throw new Error(`Unknown action: ${parsedCommand.action}`);
    }
}

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
        case "for":
                const loopVar = parts[1]; // Loop variable (e.g., 'x')
                const fromIndex = parts.indexOf("from");
                const toIndex = parts.indexOf("to");
            
                if (fromIndex === -1 || toIndex === -1 || toIndex <= fromIndex) {
                    throw new Error(`Invalid 'for' command syntax. Usage: 'for <var> from <start> to <end> { ... }'`);
                }
            
                const start = parseInt(parts[fromIndex + 1], 10);
                const end = parseInt(parts[toIndex + 1], 10);
            
                if (isNaN(start) || isNaN(end)) {
                    throw new Error(`Invalid 'for' command range. 'from' and 'to' must be integers.`);
                }
            
                return {
                    action: "loop",
                    variable: loopVar,
                    start: start,
                    end: end,
                    body: parts.slice(toIndex + 2).join(" ") // Commands after 'to <end>'
                };
            
        case "while":   
            // Extract condition and commands
            const conditionIndex = command.indexOf("{");
            if (conditionIndex === -1) {
                throw new Error("Invalid 'while' syntax. Missing '{'.");
            }
            const condition = command.slice(6, conditionIndex).trim(); // Extracts condition
            const bodyCommands = command.slice(conditionIndex + 1, command.lastIndexOf("}")).trim(); // Extracts body
            return {
                action: "while",
                condition: condition, // e.g., cursor["x"] < 300
                body: bodyCommands    // e.g., move_cursor 50 0; circle 30
            };
        case "{":
            // Handle block initialization
            return { action: "block_start" };
        case "}":
            // Handle block closure
            return { action: "block_end" };
        default:
            throw new Error(`Unknown command: ${cmdName}`);
    }
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

function sendCommandToBackend(command) {
    fetch('/process-command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(command)
    }).then(response => response.json())
      .then(result => {
          if (result.error) {
              console.error("Error:", result.error);
          } else {
              updateCanvas(result); // Update canvas with backend response
          }
      });
}

export { parseCommand, validateCommands, processCommands, renderHighlightedCode, sendCommandToBackend };
