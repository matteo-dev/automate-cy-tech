// Open a fresh new page for each "New File" click
document.getElementById("new-file").addEventListener("click", () => {
    // Open a new tab with the URL pointing to the Drawing Tool
    const newWindow = window.open("/drawing_tool", "_blank");

    if (!newWindow) {
        console.error("Failed to open a new window/tab. Ensure pop-ups are not blocked.");
    }
    // Optional: Add unique page titles
    newWindow.onload = () => {
        newWindow.document.title = `New File - Drawing Tool (${Date.now()})`;
    };


});

