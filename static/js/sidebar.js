// Sidebar.js - Handles sidebar toggle and dynamic functionality

// Import dependencies
import { updateCanvas, drawShapeOnCanvas } from './canvas.js';
import { processCommands } from './commands.js';
import { loadDrawingList } from './fetchHandlers.js';

// Toggles the visibility of the sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const toggleButton = document.getElementById('toggleSidebar');

    if (sidebar) {
        sidebar.classList.toggle('collapsed');

        if (sidebar.classList.contains('collapsed')) {
            // Adjust styles for collapsed state
            sidebar.style.width = '60px';
            toggleButton.textContent = '☰';
            Array.from(sidebar.querySelectorAll('a, h2, ul, p')).forEach(el => el.style.display = 'none');
        } else {
            // Adjust styles for expanded state
            sidebar.style.width = '300px';
            toggleButton.textContent = '✖';
            Array.from(sidebar.querySelectorAll('a, h2, ul, p')).forEach(el => el.style.display = 'block');
        }
    } else {
        console.error('Sidebar element not found in the DOM.');
    }
}

// Populates the drawing history dynamically
function updateDrawingHistory(drawings) {
    const drawingList = document.getElementById('drawingList');
    if (drawingList) {
        drawingList.innerHTML = ''; // Clear current list

        drawings.forEach(drawing => {
            const li = document.createElement('li');
            li.textContent = `${drawing.title} (${drawing.date_created})`;
            li.classList.add('drawing-item');
            li.addEventListener('click', () => loadDrawing(drawing.id)); // Add click listener to load the drawing
            drawingList.appendChild(li);
        });
    } else {
        console.error('Drawing list element not found in the DOM.');
    }
}

// Initializes the sidebar toggle functionality
function initializeSidebar() {
    // Create a toggle button for the sidebar
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

    // Attach click event listener to the toggle button
    toggleSidebarBtn.addEventListener('click', toggleSidebar);

    // Load drawing history when the sidebar is initialized
    loadDrawingList(); // Assumes this function is defined in fetchHandlers.js
}

// Makes the sidebar responsive for smaller screens
function adjustSidebarForScreenSize() {
    const sidebar = document.getElementById('sidebar');
    const toggleButton = document.getElementById('toggleSidebar');

    if (window.innerWidth < 768) {
        sidebar.classList.add('collapsed');
        sidebar.style.width = '60px';
        toggleButton.textContent = '☰';
        Array.from(sidebar.querySelectorAll('a, h2, ul, p')).forEach(el => el.style.display = 'none');
    } else {
        sidebar.classList.remove('collapsed');
        sidebar.style.width = '300px';
        toggleButton.textContent = '✖';
        Array.from(sidebar.querySelectorAll('a, h2, ul, p')).forEach(el => el.style.display = 'block');
    }
}

// Event listener for window resize to adjust sidebar
window.addEventListener('resize', adjustSidebarForScreenSize);

// Initialize the sidebar functionality when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeSidebar();
    adjustSidebarForScreenSize();
});

export { toggleSidebar, initializeSidebar, updateDrawingHistory };
