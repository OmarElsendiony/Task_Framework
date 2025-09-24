
// Graph Editor Variables
const nodes = new vis.DataSet([]);
const edges = new vis.DataSet([]);
let network = null;
let graphExpanded = false;

const defaultOptions = {
    manipulation: {
        enabled: true,
        initiallyActive: true,
        addNode: function (data, callback) {
            const label = prompt("Enter node label:", data.id);
            if (label !== null) {
                data.label = label;
                data.id = label;
                callback(data);
            }
        },
        addEdge: function (data, callback) {
            if (data.from === data.to) {
                alert("Self-loops not allowed.");
                return;
            }
            const label = prompt("Enter edge connection (input->output):", "");
            if (label !== null && label !== '') {
                data.label = label;
            }
            callback(data);
        },
        editNode: function (data, callback) {
            const label = prompt("Edit node label:", data.label);
            if (label !== null) {
                data.label = label;
                nodes.update({ id: data.id, label: label });
                callback(data);
            }
        },
        editEdge: function (data, callback) {
            const label = prompt("Edit edge connection (input->output):", data.label);
            if (label !== null) {
                data.label = label;
                callback(data);
            }
        },
        deleteNode: true,
        deleteEdge: true
    },
    nodes: {
        shape: 'circle'
    },
    edges: { arrows: 'to' },
    physics: false,
    layout: { improvedLayout: false }
};

function createNetwork(options = defaultOptions) {
    if (network) network.destroy();
    const container = document.getElementById('network');
    network = new vis.Network(container, { nodes, edges }, options);
}

function toggleGraphEditor() {
    const content = document.getElementById('graph-editor-content');
    const toggle = document.getElementById('graph-toggle');
    
    graphExpanded = !graphExpanded;
    
    if (graphExpanded) {
        content.classList.add('expanded');
        toggle.textContent = '▲';
        // Initialize network when expanded for the first time
        if (!network) {
            createNetwork();
        }
    } else {
        content.classList.remove('expanded');
        toggle.textContent = '▼';
    }
}

function exportGraphJSON() {
    const edgeList = [];
    const edgeMap = new Map();

    edges.get().forEach(edge => {
        const fromLabel = nodes.get(edge.from)?.label || edge.from;
        const toLabel = nodes.get(edge.to)?.label || edge.to;
        const key = `${fromLabel}->${toLabel}`;
        const conn = edge.label?.split(',').map(pair => pair.trim().split('->')) || [];
        if (!edgeMap.has(key)) {
            edgeMap.set(key, []);
        }
        edgeMap.get(key).push(...conn);
    });

    for (let [key, connections] of edgeMap.entries()) {
        const [from, to] = key.split('->');
        const inputs = connections.map(c => c[0]).join(', ');
        const outputs = connections.map(c => c[1]).join(', ');
        edgeList.push({
            from,
            to,
            connection: { input: inputs, output: outputs }
        });
    }

    const exportData = { edges: edgeList };
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'graph.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showCorrectMessage('Graph exported successfully!');
}

function importGraphJSON() {
    const input = document.getElementById('graphFileInput');
    input.value = '';
    input.click();
    input.onchange = () => {
        const file = input.files[0];
        const reader = new FileReader();
        reader.onload = e => {
            try {
                const obj = JSON.parse(e.target.result);
                nodes.clear();
                edges.clear();
                const added = new Set();
                const uniqueNodes = new Set();
                let imported_edges = obj.edges
                if (!obj.edges || !Array.isArray(obj.edges)) {
                    imported_edges = obj.task.edges
                }

                imported_edges.forEach(e => {
                    uniqueNodes.add(e.from);
                    uniqueNodes.add(e.to);
                });

                let angle = 0;
                const radius = 200;
                const step = (2 * Math.PI) / uniqueNodes.size;

                [...uniqueNodes].forEach(node => {
                    const x = radius * Math.cos(angle);
                    const y = radius * Math.sin(angle);
                    angle += step;
                    nodes.add({ id: node, label: node, x, y, fixed: false });
                });

                imported_edges.forEach(e => {
                    const inputFields = e.connection.input.split(',').map(s => s.trim());
                    const outputFields = e.connection.output.split(',').map(s => s.trim());
                    const pairs = inputFields.map((input, i) => `${input}->${outputFields[i]}`);
                    const edgeId = `${e.from}-${e.to}`;
                    
                    if (!added.has(edgeId)) {
                        edges.add({
                            from: e.from,
                            to: e.to,
                            label: pairs.join(', '),
                            arrows: 'to'
                        });
                        added.add(edgeId);
                    }
                });

                if (network) {
                    network.setData({ nodes, edges });
                }
                showCorrectMessage('Graph imported successfully!');
            } catch (error) {
                console.error('Error importing graph:', error);
                showWrongMessage('Error importing graph: ' + error.message);
            }
        };
        reader.readAsText(file);
    };
}

function populateNodesFromActions() {
    // Initialize nodeList as an empty array
    let nodeList = [];
    
    // Get all API action containers
    const actionElements = document.querySelectorAll('.api-action');
    
    // Extract selected API names from radio buttons
    actionElements.forEach(actionEl => {
        const selectedRadio = actionEl.querySelector('input[type="radio"]:checked');
        if (selectedRadio && selectedRadio.value) {
            nodeList.push(selectedRadio.value);
        }
    });
    
    // Check if we have any nodes to work with
    if (nodeList.length === 0) {
        showWrongMessage('No actions with selected APIs found. Please add actions and select APIs first.');
        return;
    }
    
    try {
        // Remove duplicates (optional - in case same API appears multiple times)
        const uniqueNodeNames = [...new Set(nodeList)];
        
        // Clear existing nodes and edges
        nodes.clear();
        edges.clear();
        
        // Calculate positions for nodes in a circle
        const radius = 200;
        const angleStep = (2 * Math.PI) / uniqueNodeNames.length;
        
        uniqueNodeNames.forEach((nodeName, index) => {
            const angle = index * angleStep;
            const x = radius * Math.cos(angle);
            const y = radius * Math.sin(angle);
            
            nodes.add({
                id: nodeName,
                label: nodeName,
                x: x,
                y: y,
                fixed: false,
                color: {
                    background: '#667eea',
                    border: '#764ba2',
                    highlight: {
                        background: '#764ba2',
                        border: '#667eea'
                    }
                },
                font: {
                    color: 'white',
                    size: 14,
                    face: 'Arial'
                }
            });
        });
        
        // Update the network if it exists
        if (network) {
            network.setData({ nodes, edges });
            // Fit the network to show all nodes
            network.fit({
                animation: {
                    duration: 1000,
                    easingFunction: 'easeInOutQuad'
                }
            });
        }
        
        showCorrectMessage(`Successfully populated ${uniqueNodeNames.length} nodes from your actions!`);
        
    } catch (error) {
        console.error('Error creating nodes:', error);
        showWrongMessage('Error creating nodes: ' + error.message);
    }
}