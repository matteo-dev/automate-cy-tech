//For managing files, saves and tabs

document.getElementById("open-file").addEventListener("click", () => {
  document.getElementById("file-input").click();
});

document.getElementById("file-input").addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target.result;
      createNewTab(file.name, content);
    };
    reader.readAsText(file);
  }
});

document.getElementById("new-file").addEventListener("click", () => {
    createNewTab("Untitled.drawpp", "");
  });
  
  function activateTab(tabId) {
    document.querySelectorAll(".tab").forEach((tab) => {
      tab.classList.remove("active");
    });
    document.querySelector(`[data-tab-id="${tabId}"]`).classList.add("active");
  
    document.querySelectorAll("#editor-container textarea").forEach((editor) => {
      editor.style.display = "none";
    });
    document.getElementById(tabId).style.display = "block";
  }

  
  document.getElementById("save-file").addEventListener("click", () => {
    const activeTab = document.querySelector(".tab.active");
    if (activeTab) {
      const tabId = activeTab.dataset.tabId;
      const content = document.getElementById(tabId).value;
      const blob = new Blob([content], { type: "text/plain" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = activeTab.innerText;
      link.click();
    } else {
      alert("No active file to save.");
    }
  });

  document.addEventListener("DOMContentLoaded", () => {
    const tabsContainer = document.getElementById("tabs");
    const tabContentContainer = document.getElementById("tab-content-container");
    let tabCounter = 0;
  
    // Create a new file (tab)
    document.getElementById("new-file").addEventListener("click", () => {
      createNewTab();
    });
  });

  function createNewTab(filename = "Untitled.drawpp", content = "") {
    const tabsContainer = document.getElementById("tabs");
    const tabContentContainer = document.getElementById("tab-content-container");

    if (!tabsContainer || !tabContentContainer) {
        console.error("Tabs or Tab Content Container not found in the DOM.");
        return;
    }

    const uniqueId = Date.now(); // Unique ID for this file
    const codeTabId = `tab-code-${uniqueId}`;
    const canvasTabId = `tab-canvas-${uniqueId}`;
    const codeContentId = `content-code-${uniqueId}`;
    const canvasContentId = `content-canvas-${uniqueId}`;

    // Create Code Editor Tab
    const codeTab = document.createElement("div");
    codeTab.classList.add("tab");
    codeTab.dataset.tabId = codeTabId;
    codeTab.innerText = `${filename} (Editor)`;
    codeTab.addEventListener("click", () => switchTab(codeTabId, codeContentId));
    tabsContainer.appendChild(codeTab);

    // Create Canvas Tab
    const canvasTab = document.createElement("div");
    canvasTab.classList.add("tab");
    canvasTab.dataset.tabId = canvasTabId;
    canvasTab.innerText = `${filename} (Canvas)`;
    canvasTab.addEventListener("click", () => switchTab(canvasTabId, canvasContentId));
    tabsContainer.appendChild(canvasTab);

    // Create Code Editor Content
    const codeContent = document.createElement("div");
    codeContent.id = codeContentId;
    codeContent.classList.add("tab-content");

    const editorContainer = document.createElement("div");
    editorContainer.classList.add("editor-container");
    const editorForm = document.createElement("form");
    editorForm.method = "POST";
    editorForm.id = `codeEditorForm-${uniqueId}`;
    const editorTextarea = document.createElement("textarea");
    editorTextarea.name = "draw_code";
    editorTextarea.id = `codeEditor-${uniqueId}`;
    editorTextarea.style.width = "100%";
    editorTextarea.style.height = "300px";
    editorTextarea.value = content;
    editorForm.appendChild(editorTextarea);
    const applyCodeBtn = document.createElement("button");
    applyCodeBtn.type = "button";
    applyCodeBtn.id = `applyCodeBtn-${uniqueId}`;
    applyCodeBtn.innerText = "Apply Code";
    editorForm.appendChild(applyCodeBtn);
    editorContainer.appendChild(editorForm);
    codeContent.appendChild(editorContainer);

    // Create Canvas Content
    const canvasContent = document.createElement("div");
    canvasContent.id = canvasContentId;
    canvasContent.classList.add("tab-content");

    const canvasContainer = document.createElement("div");
    canvasContainer.classList.add("canvas-container");
    const controlsDiv = document.createElement("div");
    controlsDiv.classList.add("drawing-controls");
    controlsDiv.innerHTML = `
        <label for="shapeSelect-${uniqueId}">Choose a shape:</label>
        <select id="shapeSelect-${uniqueId}">
            <option value="circle">Circle</option>
            <option value="rectangle">Rectangle</option>
            <option value="square">Square</option>
            <option value="line">Line</option>
        </select>
    `;

    const propertyInputsDiv = document.createElement("div");
    propertyInputsDiv.id = `propertyInputs-${uniqueId}`;
    propertyInputsDiv.innerHTML = `
        <div id="cursorPosition">
            <label>Set Cursor Position:</label>
            <input type="number" id="cursorX-${uniqueId}" placeholder="X coordinate">
            <input type="number" id="cursorY-${uniqueId}" placeholder="Y coordinate">
        </div>
        <div id="shapeSize">
            <label>Size:</label>
            <input type="number" id="size-${uniqueId}" placeholder="Size (e.g., radius for circles)">
        </div>
        <div id="shapeColor">
            <label>Shape Color:</label>
            <input type="color" id="colorPicker-${uniqueId}" value="#000000">
        </div>
        <div id="canvasColor">
            <label>Canvas Background Color:</label>
            <input type="color" id="canvasColorPicker-${uniqueId}" value="#ffffff">
        </div>
    `;

    const canvas = document.createElement("canvas");
    canvas.id = `drawingCanvas-${uniqueId}`;
    canvas.width = 600;
    canvas.height = 400;
    canvasContainer.appendChild(controlsDiv);
    canvasContainer.appendChild(propertyInputsDiv);
    canvasContainer.appendChild(canvas);
    const buttonContainer = document.createElement("div");
    buttonContainer.id = `buttonContainer-${uniqueId}`;
    buttonContainer.innerHTML = `
        <button id="addShapeBtn-${uniqueId}" class="control-btn">Add Shape to Canvas</button>
        <button id="clearBtn-${uniqueId}" class="control-btn">Clear Canvas</button>
        <button id="takeasaveBtn-${uniqueId}" class="control-btn">Take a save of Canvas</button>
    `;
    canvasContainer.appendChild(buttonContainer);
    canvasContent.appendChild(canvasContainer);

    // Append Content to Tab Container
    tabContentContainer.appendChild(codeContent);
    tabContentContainer.appendChild(canvasContent);

    // Automatically switch to the Code Editor tab
    switchTab(codeTabId, codeContentId);
}

function switchTab(tabId, tabContentId) {
    // Deactivate all tabs and content
    document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach((content) => (content.style.display = "none"));

    // Activate the selected tab and content
    document.querySelector(`[data-tab-id="${tabId}"]`).classList.add("active");
    document.getElementById(tabContentId).style.display = "block";
}


