async function extract_policy_apis_handling(){
    const response = await fetch('/database_utilities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: 'extract_policy_apis'
        })
    });

    const data = await response.json();
    console.log(data);

    document.getElementById('content').style.display = 'block';
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').innerHTML = `
        <h2 id="content-header">Extract Policy APIs</h2>
        <h3 class="content-subheader">Initial Prompt</h3>
        <textarea id="initial-prompt"></textarea>

        <h3 class="content-subheader">Policy</h3>
        <textarea id="policy"></textarea>

        <h3 class="content-subheader">Example APIs</h3>
        <textarea id="example-apis"></textarea>

        <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
            <button id="extract-apis" onclick="sendContentLLM('extract_policy_apis')" style="margin: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">Extract Policy APIs</button>
        </div>
    `;

    document.getElementById('initial-prompt').value = data.initial_prompt || '';
    document.getElementById('policy').value = data.policy || '';
    document.getElementById('example-apis').value = data.example_apis || '';
}

async function extract_policy_schema_handling(){
    const response = await fetch('/database_utilities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: 'extract_policy_schema'
        })
    });

    const data = await response.json();
    console.log(data);

    document.getElementById('content').style.display = 'block';
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').innerHTML = `
        <h2 id="content-header">Extract Policy Schema</h2>
        <h3 class="content-subheader">Initial Prompt</h3>
        <textarea id="initial-prompt"></textarea>

        <h3 class="content-subheader">Policy</h3>
        <textarea id="policy"></textarea>

        <h3 class="content-subheader">Example Schema</h3>
        <textarea id="example-schema"></textarea>

        <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
            <button id="extract-schema" onclick="sendContentLLM('extract_policy_schema')" style="margin: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">Extract Policy Schema</button>
        </div>
    `;

    document.getElementById('initial-prompt').value = data.initial_prompt || '';
    document.getElementById('policy').value = data.policy || '';
    document.getElementById('example-schema').value = data.example_schema || '';
}

function sendContentLLM(feature){
    if (feature == "policy_creation"){
        const initialPrompt = document.getElementById('initial-prompt').value;
        const dbSchema = document.getElementById('db-schema').value;
        const examplePolicies = document.getElementById('example-policies').value;
        const interfaceApis = document.getElementById('interface-apis').value;

        fetch('/database_utilities_prompt_generation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'generate_policy_prompt',
                initial_prompt: initialPrompt,
                db_schema: dbSchema,
                example_policies: examplePolicies,
                interface_apis: interfaceApis
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // remove if they were present before
            const existingHeader = document.getElementById('output-header');
            const existingTextArea = document.getElementById('generated-policy');
            if (existingHeader) {
                existingHeader.remove();
            }
            if (existingTextArea) {
                existingTextArea.remove();
            }

            outputHeader = document.createElement('h2');
            outputHeader.innerText = 'Generated Policy Prompt';
            outputHeader.id = 'output-header';
            document.getElementById('content').appendChild(outputHeader);

            textAreaNode = document.createElement('textarea');
            textAreaNode.id = 'generated-policy';
            textAreaNode.style.width = '100%';
            textAreaNode.style.height = '200px';
            textAreaNode.value = data.prompt;
            document.getElementById('content').appendChild(textAreaNode);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while generating the policy.');
        });

    } else if (feature == "api_implementation"){
        const initialPrompt = document.getElementById('initial-prompt').value;
        const dbSchema = document.getElementById('db-schema').value;
        const exampleApis = document.getElementById('example-apis').value;
        const interfaceApis = document.getElementById('interface-apis').value;

        fetch('/database_utilities_prompt_generation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'generate_api_prompt',
                initial_prompt: initialPrompt,
                db_schema: dbSchema,
                example_apis: exampleApis,
                interface_apis: interfaceApis
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // remove if they were present before
            const existingHeader = document.getElementById('output-header');
            const existingTextArea = document.getElementById('generated-api');
            if (existingHeader) {
                existingHeader.remove();
            }
            if (existingTextArea) {
                existingTextArea.remove();
            }

            outputHeader = document.createElement('h2');
            outputHeader.innerText = 'Generated API Prompt';
            outputHeader.id = 'output-header';
            document.getElementById('content').appendChild(outputHeader);

            textAreaNode = document.createElement('textarea');
            textAreaNode.id = 'generated-api';
            textAreaNode.style.width = '100%';
            textAreaNode.style.height = '200px';
            textAreaNode.value = data.prompt;
            document.getElementById('content').appendChild(textAreaNode);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while generating the API.');
        });
    } else if (feature == "database_seeding"){
        const initialPrompt = document.getElementById('initial-prompt').value;
        const dbSchema = document.getElementById('db-schema').value;

        fetch('/database_utilities_prompt_generation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'generate_seed_prompt',
                initial_prompt: initialPrompt,
                db_schema: dbSchema
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // remove if they were present before
            const existingHeader = document.getElementById('output-header');
            const existingTextArea = document.getElementById('generated-seed');
            if (existingHeader) {
                existingHeader.remove();
            }
            if (existingTextArea) {
                existingTextArea.remove();
            }

            outputHeader = document.createElement('h2');
            outputHeader.innerText = 'Generated Seed Prompt';
            outputHeader.id = 'output-header';
            document.getElementById('content').appendChild(outputHeader);

            textAreaNode = document.createElement('textarea');
            textAreaNode.id = 'generated-seed';
            textAreaNode.style.width = '100%';
            textAreaNode.style.height = '200px';
            textAreaNode.value = data.prompt;
            document.getElementById('content').appendChild(textAreaNode);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while generating the seed.');
        });
    } else if (feature == "scenario_realism"){
        const initialPrompt = document.getElementById('initial-prompt').value;
        const dbSchema = document.getElementById('db-schema').value;

        fetch('/database_utilities_prompt_generation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'check_scenario_realism',
                initial_prompt: initialPrompt,
                db_schema: dbSchema,
                scenario: document.getElementById('scenario').value
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // remove if they were present before
            const existingHeader = document.getElementById('output-header');
            const existingTextArea = document.getElementById('generated-scenario');
            if (existingHeader) {
                existingHeader.remove();
            }
            if (existingTextArea) {
                existingTextArea.remove();
            }

            outputHeader = document.createElement('h2');
            outputHeader.innerText = 'Generated Scenario Prompt';
            outputHeader.id = 'output-header';
            document.getElementById('content').appendChild(outputHeader);

            textAreaNode = document.createElement('textarea');
            textAreaNode.id = 'generated-scenario';
            textAreaNode.style.width = '100%';
            textAreaNode.style.height = '200px';
            textAreaNode.value = data.realism_check;
            document.getElementById('content').appendChild(textAreaNode);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while generating the scenario.');
        });
    } else if (feature == "extract_policy_apis"){
        const initialPrompt = document.getElementById('initial-prompt').value;
        const policy = document.getElementById('policy').value;
        const exampleApis = document.getElementById('example-apis').value;

        fetch('/database_utilities_prompt_generation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'extract_policy_apis',
                initial_prompt: initialPrompt,
                policy: policy,
                example_apis: exampleApis
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // remove if they were present before
            const existingHeader = document.getElementById('output-header');
            const existingTextArea = document.getElementById('generated-apis');
            if (existingHeader) {
                existingHeader.remove();
            }
            if (existingTextArea) {
                existingTextArea.remove();
            }

            outputHeader = document.createElement('h2');
            outputHeader.innerText = 'Extracted Policy APIs';
            outputHeader.id = 'output-header';
            document.getElementById('content').appendChild(outputHeader);

            textAreaNode = document.createElement('textarea');
            textAreaNode.id = 'generated-prompt';
            textAreaNode.style.width = '100%';
            textAreaNode.style.height = '200px';
            textAreaNode.value = data.prompt;
            document.getElementById('content').appendChild(textAreaNode);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while extracting policy APIs.');
        });
    } else if (feature == "extract_policy_schema"){
        const initialPrompt = document.getElementById('initial-prompt').value;
        const policy = document.getElementById('policy').value;
        const exampleSchema = document.getElementById('example-schema').value;

        fetch('/database_utilities_prompt_generation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'extract_policy_schema',
                initial_prompt: initialPrompt,
                policy: policy,
                example_schema: exampleSchema
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // remove if they were present before
            const existingHeader = document.getElementById('output-header');
            const existingTextArea = document.getElementById('generated-schema');
            if (existingHeader) {
                existingHeader.remove();
            }
            if (existingTextArea) {
                existingTextArea.remove();
            }

            outputHeader = document.createElement('h2');
            outputHeader.innerText = 'Extracted Policy Schema';
            outputHeader.id = 'output-header';
            document.getElementById('content').appendChild(outputHeader);

            textAreaNode = document.createElement('textarea');
            textAreaNode.id = 'generated-prompt';
            textAreaNode.style.width = '100%';
            textAreaNode.style.height = '200px';
            textAreaNode.value = data.prompt;
            document.getElementById('content').appendChild(textAreaNode);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while extracting policy schema.');
        });
    } else if (feature == "tune_policy"){
        const initialPrompt = document.getElementById('initial-prompt').value;
        const policy = document.getElementById('policy').value;
        const examplePolicies = document.getElementById('example-policies').value;

        fetch('/database_utilities_prompt_generation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'tune_policy',
                initial_prompt: initialPrompt,
                policy: policy,
                example_policies: examplePolicies
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // remove if they were present before
            const existingHeader = document.getElementById('output-header');
            const existingTextArea = document.getElementById('generated-tuned-policy');
            if (existingHeader) {
                existingHeader.remove();
            }
            if (existingTextArea) {
                existingTextArea.remove();
            }

            outputHeader = document.createElement('h2');
            outputHeader.innerText = 'Tuned Policy';
            outputHeader.id = 'output-header';
            document.getElementById('content').appendChild(outputHeader);

            textAreaNode = document.createElement('textarea');
            textAreaNode.id = 'generated-tuned-policy';
            textAreaNode.style.width = '100%';
            textAreaNode.style.height = '200px';
            textAreaNode.value = data.prompt;
            document.getElementById('content').appendChild(textAreaNode);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while tuning the policy.');
        });
    } else if (feature == "policy_validator"){
        const initialPrompt = document.getElementById('initial-prompt').value;
        const policy = document.getElementById('policy').value;
        const examplePolicies = document.getElementById('example-policies').value;

        fetch('/database_utilities_prompt_generation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'validate_policy',
                initial_prompt: initialPrompt,
                policy: policy,
                example_policies: examplePolicies
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // remove if they were present before
            const existingHeader = document.getElementById('output-header');
            const existingTextArea = document.getElementById('generated-validation');
            if (existingHeader) {
                existingHeader.remove();
            }
            if (existingTextArea) {
                existingTextArea.remove();
            }

            outputHeader = document.createElement('h2');
            outputHeader.innerText = 'Policy Validation Results';
            outputHeader.id = 'output-header';
            document.getElementById('content').appendChild(outputHeader);

            textAreaNode = document.createElement('textarea');
            textAreaNode.id = 'generated-validation';
            textAreaNode.style.width = '100%';
            textAreaNode.style.height = '200px';
            textAreaNode.value = data.prompt;
            document.getElementById('content').appendChild(textAreaNode);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while validating the policy.');
        });
    } else {
        alert("This feature is not implemented yet.");
    }
}

async function policy_creation_handling(){
    const response = await fetch('/database_utilities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: 'policy_creation'
        })
    });

    const data = await response.json();
    console.log(data);

    document.getElementById('content').style.display = 'block';
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').innerHTML = `
        <h2 id="content-header">Policy Creation</h2>
        <h3 class="content-subheader">Initial Prompt</h3>
        <textarea id="initial-prompt"></textarea>

        <h3 class="content-subheader">Database schema</h3>
        <textarea id="db-schema"></textarea>

        <h3 class="content-subheader">Example policies</h3>
        <textarea id="example-policies"></textarea>

        <h3 class="content-subheader">Interface APIs</h3>
        <textarea id="interface-apis"></textarea>
        <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
            <button id="generate-policy" onclick="sendContentLLM('policy_creation')" style="margin: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">Generate Policy Prompt</button>
        </div>
    `;

    document.getElementById('initial-prompt').value = data.initial_prompt;
    // document.getElementById('db-schema').value = data.db_schema;
    document.getElementById('example-policies').value = data.example_policies;
}

async function database_seeding_handling(){
    const response = await fetch('/database_utilities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: 'database_seeding'
        })
    });

    const data = await response.json();
    console.log(data);

    document.getElementById('content').style.display = 'block';
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').innerHTML = `
        <h2 id="content-header">Database Seeding</h2>
        <h3 class="content-subheader">Initial Prompt</h3>
        <textarea id="initial-prompt"></textarea>

        <h3 class="content-subheader">Database schema</h3>
        <textarea id="db-schema"></textarea>

        <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
            <button id="generate-seed" onclick="sendContentLLM('database_seeding')" style="margin: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">Generate Seed Prompt</button>
        </div>
    `;

    document.getElementById('initial-prompt').value = data.initial_prompt;
    // document.getElementById('db-schema').value = data.db_schema;
    // document.getElementById('example-data').value = data.example_data;
}

async function scenario_realism_handling(){
    const response = await fetch('/database_utilities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: 'scenario_realism'
        })
    });

    const data = await response.json();
    console.log(data);

    document.getElementById('content').style.display = 'block';
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').innerHTML = `
        <h2 id="content-header">Scenario Realism</h2>
        <h3 class="content-subheader">Initial Prompt</h3>
        <textarea id="initial-prompt"></textarea>

        <h3 class="content-subheader">Database schema</h3>
        <textarea id="db-schema"></textarea>

        <h3 class="content-subheader">Scenario</h3>
        <textarea id="scenario"></textarea>

        <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
            <button id="generate-scenario" onclick="sendContentLLM('scenario_realism')" style="margin: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">Generate Scenario Prompt</button>
        </div>
    `;

    document.getElementById('initial-prompt').value = data.initial_prompt;
    // document.getElementById('db-schema').value = data.db_schema;
}

async function api_implementation_handling(){

    const response = await fetch('/database_utilities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: 'api_implementation'
        })
    });

    const data = await response.json();
    console.log(data);

    document.getElementById('content').style.display = 'block';
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').innerHTML = `
        <h2 id="content-header">API Implementation</h2>
        <h3 class="content-subheader">Initial Prompt</h3>
        <textarea id="initial-prompt"></textarea>

        <h3 class="content-subheader">Database schema</h3>
        <textarea id="db-schema"></textarea>

        <h3 class="content-subheader">Example APIs</h3>
        <textarea id="example-apis"></textarea>

        <h3 class="content-subheader">Interface APIs</h3>
        <textarea id="interface-apis"></textarea>

        <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
            <button id="generate-api" onclick="sendContentLLM('api_implementation')" style="margin: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">Generate API Prompt</button>
        </div>
    `;

    document.getElementById('initial-prompt').value = data.initial_prompt;
    // document.getElementById('db-schema').value = data.db_schema;
    document.getElementById('example-apis').value = data.example_apis;

}

        
async function extract_policy_apis_handling(){
    const response = await fetch('/database_utilities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: 'extract_policy_apis'
        })
    });

    const data = await response.json();
    console.log(data);

    document.getElementById('content').style.display = 'block';
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').innerHTML = `
        <h2 id="content-header">Extract Policy APIs</h2>
        <h3 class="content-subheader">Initial Prompt</h3>
        <textarea id="initial-prompt"></textarea>

        <h3 class="content-subheader">Policy</h3>
        <textarea id="policy"></textarea>

        <h3 class="content-subheader">Example APIs</h3>
        <textarea id="example-apis"></textarea>

        <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
            <button id="extract-apis" onclick="sendContentLLM('extract_policy_apis')" style="margin: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">Extract Policy APIs</button>
        </div>
    `;

    document.getElementById('initial-prompt').value = data.initial_prompt || '';
    document.getElementById('policy').value = data.policy || '';
    document.getElementById('example-apis').value = data.example_apis || '';
}

async function tune_policy_handling(){
    const response = await fetch('/database_utilities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: 'tune_policy'
        })
    });

    const data = await response.json();
    console.log(data);

    document.getElementById('content').style.display = 'block';
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').innerHTML = `
        <h2 id="content-header">Tune Policy</h2>
        <h3 class="content-subheader">Initial Prompt</h3>
        <textarea id="initial-prompt"></textarea>

        <h3 class="content-subheader">Policy</h3>
        <textarea id="policy"></textarea>

        <h3 class="content-subheader">Example Policies</h3>
        <textarea id="example-policies"></textarea>

        <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
            <button id="tune-policy" onclick="sendContentLLM('tune_policy')" style="margin: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">Tune Policy</button>
        </div>
    `;

    document.getElementById('initial-prompt').value = data.initial_prompt || '';
    document.getElementById('policy').value = data.policy || '';
    document.getElementById('example-policies').value = data.example_policies || '';
}

async function policy_validator_handling(){
    const response = await fetch('/database_utilities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: 'policy_validator'
        })
    });

    const data = await response.json();
    console.log(data);

    document.getElementById('content').style.display = 'block';
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').innerHTML = `
        <h2 id="content-header">Policy Validator</h2>
        <h3 class="content-subheader">Initial Prompt</h3>
        <textarea id="initial-prompt"></textarea>

        <h3 class="content-subheader">Policy</h3>
        <textarea id="policy"></textarea>

        <h3 class="content-subheader">Example Policies</h3>
        <textarea id="example-policies"></textarea>

        <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
            <button id="validate-policy" onclick="sendContentLLM('policy_validator')" style="margin: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">Validate Policy</button>
        </div>
    `;

    document.getElementById('initial-prompt').value = data.initial_prompt || '';
    document.getElementById('policy').value = data.policy || '';
    document.getElementById('example-policies').value = data.example_policies || '';
}

async function extract_policy_schema_handling(){
    const response = await fetch('/database_utilities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: 'extract_policy_schema'
        })
    });

    const data = await response.json();
    console.log(data);

    document.getElementById('content').style.display = 'block';
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').innerHTML = `
        <h2 id="content-header">Extract Policy Schema</h2>
        <h3 class="content-subheader">Initial Prompt</h3>
        <textarea id="initial-prompt"></textarea>

        <h3 class="content-subheader">Policy</h3>
        <textarea id="policy"></textarea>

        <h3 class="content-subheader">Example Schema</h3>
        <textarea id="example-schema"></textarea>

        <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
            <button id="extract-schema" onclick="sendContentLLM('extract_policy_schema')" style="margin: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">Extract Policy Schema</button>
        </div>
    `;

    document.getElementById('initial-prompt').value = data.initial_prompt || '';
    document.getElementById('policy').value = data.policy || '';
    document.getElementById('example-schema').value = data.example_schema || '';
}


document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers for utility cards
    const cards = document.querySelectorAll('.analytics-card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            const utility = this.dataset.utility;
            if (utility) {
                console.log(`Clicked on ${utility}`);
                // Add navigation logic here
                if (utility === 'policy-creation') {
                    policy_creation_handling();
                } else if (utility === 'api-implementation') {
                    api_implementation_handling();
                } else if (utility === 'database-seeding') {
                    database_seeding_handling();
                } else if (utility === 'scenario-realism') {
                    scenario_realism_handling();
                }
                else if (utility === 'extract-policy-apis') {
                    extract_policy_apis_handling();
                } else if (utility === 'extract-policy-schema') {
                    extract_policy_schema_handling();
                }
                else if (utility === 'tune-policy') {
                    tune_policy_handling();
                } else if (utility === 'policy-validator') {
                    policy_validator_handling();
                }
            } else {
                console.warn('No utility data found for this card.');
            }
        });
    });
});