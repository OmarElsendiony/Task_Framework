
const APIs = new Map();
let actionCounter = 0;

async function handleGo() {
    const environment = document.getElementById('environment').value.trim();
    const interface = document.getElementById('interface').value;
    
    if (!environment) {
        showWrongMessage('Please enter an environment name');
        return;
    }
    
    if (!interface) {
        showWrongMessage('Please select an interface');
        return;
    }
    
    console.log('Environment:', environment);
    console.log('Interface:', interface);
    
    try {
        const response = await fetch('/choose_env_interface', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                environment: environment,
                interface: interface
            })
        });

        if (!response.ok) {
            showWrongMessage('Failed to select Environment and Interface.');
            console.error('Error details:', await response.json());
            return;
        }

        const data = await response.json();
        if (data.status === 'success') {
            showCorrectMessage('Environment and Interface selected successfully!');
            console.log('Response:', data);
            
            // Clear existing APIs
            APIs.clear();
            
            // Populate APIs from response
            for (const func of data.functions_info) {
                APIs.set(func.name, {
                    description: func.description,
                    parameters: func.parameters,
                    required: func.required
                });
            }
            console.log('APIs:', APIs);
        } else {
            showWrongMessage('Failed to select Environment and Interface.');
        }
    } catch (error) {
        console.error('Error:', error);
        showWrongMessage('An error occurred while connecting to the server.');
    
    }
}

async function runAllActions() {
    const actionElements = document.querySelectorAll('.api-action');
    const runAllBtn = document.getElementById('run-all-btn');
    
    if (actionElements.length === 0) {
        showWrongMessage('No actions to execute.');
        return;
    }
    
    // Check if all actions have selected APIs
    let hasInvalidActions = false;
    actionElements.forEach((actionEl, index) => {
        const selectedRadio = actionEl.querySelector('input[type="radio"]:checked');
        if (!selectedRadio) {
            showWrongMessage(`Action ${index + 1} doesn't have an API selected.`);
            hasInvalidActions = true;
        }
    });
    
    if (hasInvalidActions) {
        return;
    }
    
    // Disable the run all button
    runAllBtn.textContent = '⏳ Running All Actions...';
    runAllBtn.disabled = true;
    
    let successCount = 0;
    let errorCount = 0;
    
    try {
        for (let i = 0; i < actionElements.length; i++) {
            const actionEl = actionElements[i];
            const actionId = actionEl.id;
            
            showCorrectMessage(`Executing Action ${i + 1} of ${actionElements.length}...`);
            
            try {
                await executeAPI(actionId);
                successCount++;
            } catch (error) {
                console.error(`Error executing action ${i + 1}:`, error);
                errorCount++;
            }
            
            // Wait 1 seconds before next action (except for the last one)
            if (i < actionElements.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        }
        
        // Show final summary
        if (errorCount === 0) {
            showCorrectMessage(`All ${successCount} actions executed successfully!`);
        } else {
            showWrongMessage(`Execution completed: ${successCount} successful, ${errorCount} failed.`);
        }
        
    } catch (error) {
        console.error('Error in runAllActions:', error);
        showWrongMessage('An error occurred while running actions.');
    } finally {
        // Re-enable the button
        runAllBtn.textContent = '🚀 Run All Actions';
        runAllBtn.disabled = false;
    }
}

function addAction() {
    if (APIs.size === 0) {
        showWrongMessage('Please select an environment and interface first by clicking GO.');
        return [ null, null ];
    }

    actionCounter++;
    const actionId = `action_${actionCounter}`;
    
    const actionContainer = document.getElementById('api-actions-container');
    
    const actionDiv = document.createElement('div');
    actionDiv.className = 'api-action';
    actionDiv.id = actionId;
    
    actionDiv.innerHTML = `
        <div class="api-action-header">
            <div class="api-action-title">Action</div>
            <button class="remove-action-button" onclick="removeAction('${actionId}')">×</button>
        </div>
                                        
        <div class="form-group">
            <label class="form-label">Select API</label>
            <div class="radio-button-container" id="${actionId}_radio_container">
                ${Array.from(APIs.keys()).map(apiKey => `
                    <input type="radio" 
                        id="${actionId}_${apiKey}" 
                        name="${actionId}_api" 
                        value="${apiKey}" 
                        class="radio-input"
                        onchange="selectAPI('${actionId}', this.value)">
                    <label for="${actionId}_${apiKey}" class="radio-button">${apiKey}</label>
                `).join('')}
            </div>
        </div>

        
        <div id="${actionId}_description" class="api-description" style="display: none;"></div>
        <div id="${actionId}_parameters" class="parameters-container"></div>
        <div id="${actionId}_execute" style="display: none;">
            <button class="execute-button" onclick="executeAPI('${actionId}')">
                🚀 Execute API
            </button>
        </div>
        <div id="${actionId}_response" class="api-response"></div>
    `;
    document.getElementsByClassName('add-action-container')[0].remove();
    const addAction = document.createElement('div');
    addAction.className = 'add-action-container';
    addAction.style = "height: 100px; display: flex; justify-content: center; align-items: center; flex-direction: column;"
    addAction.innerHTML = `
        <button class="add-action-button" onclick="addAction()">
            +
        </button>
        <span class="add-action-text">Add Action</span>
    `;
    
    actionContainer.appendChild(actionDiv);
    actionContainer.appendChild(addAction);
    
    // Scroll to the new action
    actionDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return [actionId, actionDiv];
}

function removeAction(actionId) {
    const actionDiv = document.getElementById(actionId);
    actionCounter--;
    if (actionDiv) {
        actionDiv.remove();
    }
}

function selectAPI(actionId, apiKey) {
    const descriptionDiv = document.getElementById(`${actionId}_description`);
    const parametersDiv = document.getElementById(`${actionId}_parameters`);
    const executeDiv = document.getElementById(`${actionId}_execute`);
    const responseDiv = document.getElementById(`${actionId}_response`);
    
    // Clear previous content
    parametersDiv.innerHTML = '';
    responseDiv.innerHTML = '';
    responseDiv.className = 'api-response';
    
    if (!apiKey) {
        descriptionDiv.style.display = 'none';
        executeDiv.style.display = 'none';
        return;
    }
    
    const apiInfo = APIs.get(apiKey);
    if (!apiInfo) return;
    
    
    // Show description
    descriptionDiv.innerHTML = apiInfo.description;
    descriptionDiv.style.display = 'block';
    
    // Create parameter inputs
    if (apiInfo.parameters) {
        Object.entries(apiInfo.parameters).forEach(([paramName, paramInfo]) => {
            const isRequired = apiInfo.required && apiInfo.required.includes(paramName);
            
            const paramDiv = document.createElement('div');
            paramDiv.className = 'parameter-group';
            
            paramDiv.innerHTML = `
                <label class="parameter-label ${isRequired ? 'required' : ''}">${paramName}</label>
                <input 
                    type="text" 
                    class="parameter-input ${isRequired ? 'required' : ''}"
                    placeholder="${paramInfo.description || `Enter ${paramName}`}"
                    data-param="${paramName}"
                    ${isRequired ? 'required' : ''}
                >
            `;
            
            parametersDiv.appendChild(paramDiv);
        });
    }
    
    // Show execute button
    executeDiv.style.display = 'block';
}

async function executeAPI(actionId) {
    const environment = document.getElementById('environment').value.trim();
    const actionDiv = document.getElementById(actionId);
    const selectedRadio = actionDiv.querySelector('input[type="radio"]:checked');
    const selectedAPI = selectedRadio ? selectedRadio.value : null;
                
    if (!selectedAPI) {
        showWrongMessage('Please select an API first.');
        return;
    }
    
    // Collect parameters
    const parameters = {};
    const paramInputs = actionDiv.querySelectorAll('.parameter-input');
    let hasError = false;
    
    paramInputs.forEach(input => {
        const paramName = input.dataset.param;
        const value = input.value.trim();
        
        if (input.classList.contains('required') && !value) {
            input.style.borderColor = '#ff4757';
            hasError = true;
        } else {
            input.style.borderColor = '#e1e5e9';
            parameters[paramName] = value;
        }
    });
    
    if (hasError) {
        showWrongMessage('Please fill in all required fields.');
        return;
    }
    
    // Show loading state
    const executeButton = actionDiv.querySelector('.execute-button');
    const originalText = executeButton.textContent;
    executeButton.textContent = '⏳ Executing...';
    executeButton.disabled = true;
    
    const responseDiv = document.getElementById(`${actionId}_response`);
    responseDiv.innerHTML = '<div class="response-header">Executing API...</div>';
    responseDiv.className = 'api-response show';
    
    try {
        const response = await fetch('/execute_api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                api_name: selectedAPI,
                parameters: parameters,
                environment: environment
            })
        });
        
        const result = await response.json();
        
        function fixNewlines(obj) {
            if (typeof obj === 'string') {
                return obj.replace(/\\n/g, '\n');
            }
            if (Array.isArray(obj)) {
                return obj.map(fixNewlines);
            }
            if (obj && typeof obj === 'object') {
                const fixed = {};
                for (let key in obj) {
                    fixed[key] = fixNewlines(obj[key]);
                }
                return fixed;
            }
            return obj;
        }
        if (response.ok) {
            responseDiv.className = 'api-response show success';
            responseDiv.innerHTML = `
                <div class="response-header">✅ Success</div>
                <div class="response-content"><pre></pre></div>
            `;
            // Set the JSON content as text to preserve literals
            
            // Process the data to convert literal \n to actual newlines

            const fixedResult = fixNewlines(result);
            responseDiv.querySelector('pre').textContent = JSON.stringify(fixedResult, null, 2);
            showCorrectMessage('API executed successfully!');
        } else {
            responseDiv.className = 'api-response show error';
            responseDiv.innerHTML = `
                <div class="response-header">❌ Error</div>
                <div class="response-content">${JSON.stringify(result, null, 2)}</div>
            `;
            showWrongMessage('API execution failed. Check the response for details.');
        }
    } catch (error) {
        responseDiv.className = 'api-response show error';
        responseDiv.innerHTML = `
            <div class="response-header">❌ Network Error</div>
            <div class="response-content">Failed to connect to the server: ${error.message}</div>
        `;
        showWrongMessage('Network error occurred while executing the API.');
    } finally {
        executeButton.textContent = originalText;
        executeButton.disabled = false;
    }
}

function showCorrectMessage(text) {
    const message = document.createElement('div');
    message.textContent = text;
    message.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4caf50;
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
            document.body.removeChild(message);
        }, 300);
    }, 3000);
}

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
            document.body.removeChild(message);
        }, 300);
    }, 3000);
}

function saveFilteredHTML() {
    // Clone the entire document
    const clonedDoc = document.cloneNode(true);

    // Sync input, textarea, and select values manually to clonedDoc
    const originalElements = document.querySelectorAll('input, textarea, select');
    const clonedElements = clonedDoc.querySelectorAll('input, textarea, select');

    originalElements.forEach((originalEl, index) => {
        const clonedEl = clonedElements[index];
        if (!clonedEl) return;

        switch (originalEl.tagName) {
            case 'TEXTAREA':
                clonedEl.innerHTML = originalEl.value;
                break;
            case 'SELECT':
                Array.from(clonedEl.options).forEach(option => {
                    option.removeAttribute('selected');
                    if (option.value === originalEl.value) {
                        option.setAttribute('selected', 'selected');
                    }
                });
                break;
            case 'INPUT':
                if (originalEl.type === 'checkbox' || originalEl.type === 'radio') {
                    if (originalEl.checked) {
                        clonedEl.setAttribute('checked', '');
                    } else {
                        clonedEl.removeAttribute('checked');
                    }
                } else {
                    clonedEl.setAttribute('value', originalEl.value);
                }
                break;
        }
    });

    // Remove unwanted elements
    const logo = clonedDoc.getElementById('image-logo');
    if (logo) logo.remove();

    // const elementsToExclude = clonedDoc.querySelectorAll('.save-button');
    // elementsToExclude.forEach(el => el.remove());

    const formTitle = clonedDoc.querySelector('main.content-area .form-title');
    if (formTitle) formTitle.remove();

    const formTextarea = clonedDoc.querySelector('main.content-area .form-textarea');
    if (formTextarea) formTextarea.remove();

    const queryBtn = clonedDoc.querySelector('main.content-area .query-btn');
    if (queryBtn) queryBtn.remove();

    // Save as an HTML file
    const htmlContent = '<!DOCTYPE html>\n' + clonedDoc.documentElement.outerHTML;
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'filtered_page.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    URL.revokeObjectURL(url);
    showCorrectMessage('Page saved successfully!');
}
/////////////////////////////////////////////
env = null;
model_provider = null;
model = null;
num_trials = null;
temperature = null;
interface_num = null;
edgesBefore = null; // so as not to conflict with graph edges
user_id = null;
instruction = null;
actionsBefore = null;
////////////////////////////////////////////
// taskBefore_text = null;


function importActions() {
    const input = document.getElementById('fileInput');
    input.value = '';
    input.click();
    input.onchange = () => {
        const file = input.files[0];
        const reader = new FileReader();
        reader.onload = e => {
            
            try {
                // taskBefore = e.target.result
                // console.log('File content:', taskBefore);
                const obj = JSON.parse(e.target.result);
                env = obj["env"]
                model_provider = obj["model_provider"]
                model = obj["model"]
                num_trials = obj["num_trials"]
                temperature = obj["temperature"]
                interface_num = obj["interface_num"]
                if (obj["task"]) {
                    user_id = obj["task"]["user_id"]
                    instruction = obj["task"]["instruction"]
                    actionsBefore = obj["task"]["actions"]
                    edgesBefore = obj["task"]["edges"]
                } else{
                    user_id = obj["task"]
                    instruction = obj["task"]
                    actionsBefore = obj["actions"]
                    edgesBefore = obj["edges"]
                }

                console.log('Imported actions:', obj);
                // const added = new Set();
                let imported_actions = obj.actions;
                let actions_interface = obj.interface_num;
                if (!obj.actions || !Array.isArray(obj.actions)) {
                    imported_actions = obj.task.actions;
                    // actions_interface = obj.task.interface_num;
                }

                var interface_selected = document.getElementsByClassName("form-select")[0];
                var interface_selected_text = interface_selected.options[interface_selected.selectedIndex].text;
                interface_selected_text = interface_selected_text.split(' ')[1];
                console.log(interface_selected_text, actions_interface);
                if (actions_interface && parseInt(actions_interface) !== parseInt(interface_selected_text)) {
                    showWrongMessage(`The imported actions are for the interface: ${actions_interface} whereas the environment is using interface: ${interface_selected_text}. Please select the correct interface first.`);
                    return;
                }

                imported_actions.forEach(action => {
                    // if (added.has(action.name)) return;
                    // added.add(action.name);
                    [actionID, actionDiv] = addAction();
                    if (actionID === null || actionDiv === null) return;
                    const radioButton = actionDiv.querySelector(`input[type="radio"][value="${action.name}"]`);
                    if (radioButton) {
                        radioButton.checked = true;
                    }
                    selectAPI(actionID, action.name);
                    actionDiv.querySelectorAll('.parameter-input').forEach(input => {
                        const paramName = input.dataset.param;
                        let value = action.arguments[paramName];
                        if (value !== undefined) {
                            // Check if value is a non-null object (but not an array or Date)
                            if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                                try {
                                    value = JSON.stringify(value);
                                } catch (e) {
                                    console.warn(`Failed to stringify value for ${paramName}`, e);
                                }
                            }
                            input.value = value;
                        }
                    });
                    // console.log('Action ID:', actionID);
                });
            } catch (error) {
                console.error('Error importing actions:', error);
                showWrongMessage('Failed to import actions. Please check the file format.');
            }
        };
        reader.readAsText(file);
    };
}

function getTaskActions(){
    const actions = [];
    const actionElements = document.querySelectorAll('.api-action');
    
    actionElements.forEach(actionEl => {
        const selectedRadio = actionEl.querySelector('input[type="radio"]:checked');
        const selectedAPI = selectedRadio ? selectedRadio.value : null;
        
        if (!selectedAPI) return;
        
        const parameters = new Map();
        const paramInputs = actionEl.querySelectorAll('.parameter-input');
        
        paramInputs.forEach(input => {
            const paramName = input.dataset.param;
            const paramVal = input.value.trim();
            console.log(paramName, paramVal);
            if (paramVal !== '') {
                // console.log(Number.isNaN(Number(paramVal)))
                if (!Number.isNaN(Number(paramVal)) && !paramName.includes('phone') && !paramName.includes('mobile')) {
                    // console.log('parsing number')
                    if (paramName.includes('_id') || paramName.includes('_by') || paramName.includes('_to')) {
                        parameters.set(paramName, paramVal); // Keep as string for IDs
                    }
                    else {
                        parameters.set(paramName, Number(paramVal));
                    }
                } else if (paramVal === 'true' || paramVal === 'false') {
                    // console.log('mgegege')
                    parameters.set(paramName, (paramVal === 'true'));
                } else if (paramVal.startsWith('{') || paramVal.startsWith('[')) {
                    // console.log('parsing json')
                    try {
                        parameters.set(paramName, JSON.parse(paramVal));
                    } catch (e) {
                        parameters.set(paramName, paramVal); // Fallback to string if parsing fails
                    }
                } else {
                    parameters.set(paramName, paramVal);
                }
            }
            /* const value = input.value.trim();
            if (value !== '') {
                parameters[paramName] = value;
            } */
        });
        // console.log(actionEl.querySelector('.response-content'))
        output = actionEl.querySelector('.response-content');
        if (output) {
            output = JSON.parse(output.textContent.trim());
            if (output.hasOwnProperty('output')) {
                output = output.output;
            } else {
                output = ''
            }
        } else {
            output = '';
        }

        
        actions.push({
            name: selectedAPI,
            arguments: Object.fromEntries(parameters),
            output: output
        });
    });
    return actions;
}

function exportActions() {
    actions = getTaskActions();
    
    const exportData = { actions: actions };
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'actions.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

