// Event listeners setup
document.addEventListener('DOMContentLoaded', function() {
    // Initialize page
    fetch_initial_prompt();
    
    // Setup event listeners
    const callButton = document.getElementById('callButton');
    if (callButton) {
        callButton.addEventListener('click', function() {
            sendContentLLM('basic_validation');
        });
    }
});

// Main validation function
function sendContentLLM(feature) {
    if (feature == "basic_validation") {
        const initialPrompt = document.getElementById('initial-prompt').value;
        const examples = document.getElementById('examples').value;
        const policy = document.getElementById('policy').value;
        const instruction = document.getElementById('instruction').value;
        const selectedModel = document.getElementById('model-select').value;
        const callLLMButton = document.getElementById('callButton');
        
        if (!initialPrompt || !policy || !instruction) {
            showWrongMessage("Please fill in all fields before validating.");
            return;
        }
        
        if (!selectedModel) {
            showWrongMessage("Please select a model before validating.");
            return;
        }
        
        // Disable the button to prevent multiple clicks
        callLLMButton.disabled = true;
        callLLMButton.innerHTML = "Validating...";
        
        fetch('/instruction_validation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'validate_instruction',
                initial_prompt: initialPrompt,
                policy: policy,
                instruction: instruction,
                model: selectedModel,
                examples: examples
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status === 'error') {
                alert(data.message || 'An error occurred while processing your request.');
                return;
            }
            
            // Remove if they were present before
            const existingHeader = document.getElementById('output-header');
            const existingTextArea = document.getElementById('generated-validation');
            if (existingHeader) {
                existingHeader.remove();
            }
            if (existingTextArea) {
                existingTextArea.remove();
            }

            const outputHeader = document.createElement('h2');
            outputHeader.innerText = 'LLM response';
            outputHeader.id = 'output-header';
            document.getElementById('content').appendChild(outputHeader);

            const textAreaNode = document.createElement('textarea');
            textAreaNode.id = 'generated-validation';
            textAreaNode.style.width = '100%';
            textAreaNode.style.height = '200px';
            textAreaNode.value = data.validation_result;
            document.getElementById('content').appendChild(textAreaNode);
            
            callLLMButton.disabled = false;
            callLLMButton.innerText = "Validate Instruction";
        })
        .catch(error => {
            console.error('Error:', error);
            callLLMButton.disabled = false;
            callLLMButton.innerText = "Validate Instruction";
        });
    } else {
        alert("This feature is not implemented yet.");
    }
}

// Fetch initial prompt from server
async function fetch_initial_prompt() {
    try {
        const response = await fetch('/instruction_validation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'fetch_initial_prompt'
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        if (data.initial_prompt) {
            document.getElementById('initial-prompt').value = data.initial_prompt;
            document.getElementById('content').style.display = 'block';
        } else {
            console.warn('No initial prompt found in the response.');
            document.getElementById('content').style.display = 'none';
        }
        
        if (data.examples) {
            document.getElementById('examples').value = data.examples;
        } else {
            console.warn('No examples found in the response.');
        }
    } catch (error) {
        console.error('Error fetching initial prompt:', error);
    }
}

// Show error message
function showWrongMessage(text) {
    const message = document.createElement('div');
    message.textContent = text;
    message.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #f44336;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1000;
        font-family: Arial, sans-serif;
        transition: all 0.3s ease;
    `;
    document.body.appendChild(message);

    setTimeout(() => {
        message.style.opacity = '0';
        message.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            if (document.body.contains(message)) {
                document.body.removeChild(message);
            }
        }, 300);
    }, 3000);
}