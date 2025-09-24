
function computeLineDiff(text1, text2) {
    const lines1 = text1.split('\n');
    const lines2 = text2.split('\n');
    
    // Create a more sophisticated diff using LCS (Longest Common Subsequence) approach
    const matrix = [];
    for (let i = 0; i <= lines1.length; i++) {
        matrix[i] = [];
        for (let j = 0; j <= lines2.length; j++) {
            if (i === 0) matrix[i][j] = j;
            else if (j === 0) matrix[i][j] = i;
            else if (lines1[i - 1] === lines2[j - 1]) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j - 1] + 1
                );
            }
        }
    }
    
    // Backtrack to find the diff
    const diff = [];
    let i = lines1.length, j = lines2.length;
    
    while (i > 0 || j > 0) {
        if (i > 0 && j > 0 && lines1[i - 1] === lines2[j - 1]) {
            diff.unshift({ type: 'unchanged', value: lines1[i - 1] });
            i--;
            j--;
        } else if (j > 0 && (i === 0 || matrix[i][j - 1] <= matrix[i - 1][j])) {
            diff.unshift({ type: 'added', value: lines2[j - 1] });
            j--;
        } else if (i > 0) {
            diff.unshift({ type: 'removed', value: lines1[i - 1] });
            i--;
        }
    }
    
    return diff;
}

function computeWordDiff(line1, line2) {
    const words1 = line1.split(/(\s+)/);
    const words2 = line2.split(/(\s+)/);
    
    const diff = [];
    let i = 0, j = 0;
    
    while (i < words1.length || j < words2.length) {
        if (i >= words1.length) {
            diff.push({ type: 'added', value: words2[j] });
            j++;
        } else if (j >= words2.length) {
            diff.push({ type: 'removed', value: words1[i] });
            i++;
        } else if (words1[i] === words2[j]) {
            diff.push({ type: 'unchanged', value: words1[i] });
            i++;
            j++;
        } else {
            // Look ahead for matches
            let foundMatch = false;
            
            // Check if current word from text1 appears later in text2
            for (let k = j + 1; k < Math.min(j + 3, words2.length); k++) {
                if (words1[i] === words2[k]) {
                    for (let l = j; l < k; l++) {
                        diff.push({ type: 'added', value: words2[l] });
                    }
                    diff.push({ type: 'unchanged', value: words1[i] });
                    i++;
                    j = k + 1;
                    foundMatch = true;
                    break;
                }
            }
            
            if (!foundMatch) {
                // Check if current word from text2 appears later in text1
                for (let k = i + 1; k < Math.min(i + 3, words1.length); k++) {
                    if (words2[j] === words1[k]) {
                        for (let l = i; l < k; l++) {
                            diff.push({ type: 'removed', value: words1[l] });
                        }
                        diff.push({ type: 'unchanged', value: words2[j] });
                        i = k + 1;
                        j++;
                        foundMatch = true;
                        break;
                    }
                }
            }
            
            if (!foundMatch) {
                diff.push({ type: 'removed', value: words1[i] });
                diff.push({ type: 'added', value: words2[j] });
                i++;
                j++;
            }
        }
    }
    
    return diff;
}

function formatDiffForPanel(diff, showType) {
    let result = '';
    let stats = { added: 0, removed: 0, unchanged: 0 };
    
    diff.forEach(item => {
        stats[item.type]++;
        
        if (item.type === 'unchanged') {
            result += `<span class="diff-unchanged">${escapeHtml(item.value)}</span>\n`;
        } else if (item.type === 'added' && (showType === 'both' || showType === 'added')) {
            result += `<span class="diff-added">${escapeHtml(item.value)}</span>\n`;
        } else if (item.type === 'removed' && (showType === 'both' || showType === 'removed')) {
            result += `<span class="diff-removed">${escapeHtml(item.value)}</span>\n`;
        } else if (item.type === 'added' && showType === 'removed') {
            // Don't show additions in the "removed" panel
        } else if (item.type === 'removed' && showType === 'added') {
            // Don't show removals in the "added" panel
        } else {
            result += `<span class="diff-unchanged">${escapeHtml(item.value)}</span>\n`;
        }
    });
    
    return { content: result, stats };
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function compareDiff() {
    const text1 = document.getElementById('text1').value;
    const text2 = document.getElementById('text2').value;
    
    if (!text1.trim() && !text2.trim()) {
        document.getElementById('originalDiff').innerHTML = '<div class="empty-state">Please enter text in at least one field</div>';
        document.getElementById('modifiedDiff').innerHTML = '<div class="empty-state">Please enter text in at least one field</div>';
        document.getElementById('stats').style.display = 'none';
        return;
    }
    
    const lineDiff = computeLineDiff(text1, text2);
    
    // Enhanced diff that also does word-level comparison within changed lines
    const enhancedDiff = [];
    lineDiff.forEach(item => {
        if (item.type === 'unchanged') {
            enhancedDiff.push(item);
        } else {
            // For added/removed lines, we keep them as is for line-level diff
            enhancedDiff.push(item);
        }
    });
    
    // Format for both panels
    const originalResult = formatDiffForPanel(enhancedDiff, 'removed');
    const modifiedResult = formatDiffForPanel(enhancedDiff, 'added');
    
    document.getElementById('originalDiff').innerHTML = originalResult.content || '<div class="empty-state">No content to display</div>';
    document.getElementById('modifiedDiff').innerHTML = modifiedResult.content || '<div class="empty-state">No content to display</div>';
    
    // Update stats
    const totalStats = {
        added: enhancedDiff.filter(item => item.type === 'added').length,
        removed: enhancedDiff.filter(item => item.type === 'removed').length,
        unchanged: enhancedDiff.filter(item => item.type === 'unchanged').length
    };
    
    document.getElementById('addedCount').textContent = totalStats.added;
    document.getElementById('removedCount').textContent = totalStats.removed;
    document.getElementById('unchangedCount').textContent = totalStats.unchanged;
    document.getElementById('stats').style.display = 'flex';
}

function clearAll() {
    document.getElementById('text1').value = '';
    document.getElementById('text2').value = '';
    document.getElementById('originalDiff').innerHTML = '<div class="empty-state">Click "Compare Texts" to see differences</div>';
    document.getElementById('modifiedDiff').innerHTML = '<div class="empty-state">Click "Compare Texts" to see differences</div>';
    document.getElementById('stats').style.display = 'none';
}

function swapTexts() {
    const text1 = document.getElementById('text1').value;
    const text2 = document.getElementById('text2').value;
    document.getElementById('text1').value = text2;
    document.getElementById('text2').value = text1;
    if (document.getElementById('stats').style.display === 'flex') {
        compareDiff();
    }
}

// Auto-compare when typing (with debounce)
let compareTimeout;
function autoCompare() {
    clearTimeout(compareTimeout);
    compareTimeout = setTimeout(compareDiff, 500);
}

document.getElementById('text1').addEventListener('input', autoCompare);
document.getElementById('text2').addEventListener('input', autoCompare);

// Initialize with example comparison
/* window.onload = function() {
    compareDiff();
}; */
function mapToObj(map) {
    return Object.fromEntries(map);
}

diffExpanded = false;
function toggleDiff() {
    if (actionsBefore === null) {
        showWrongMessage('Please import a task first to compare it with the current task!');
        return;
    }
    numberOutputs = document.querySelectorAll('.response-content').length
    numberInputs = document.querySelectorAll('.parameters-container').length

    if (numberOutputs != numberInputs) {
        showWrongMessage('Mismatched number of inputs and outputs. Please ensure you have run all actions.');
        return;
    }
    
    const content = document.getElementById('task-diff-content');
    const toggle = document.getElementById('diff-toggle');
    diffExpanded = !diffExpanded;
    if (diffExpanded) {
        taskBeforeReconstructed = new Map(); taskAfterConstructed = new Map();
        taskBeforeReconstructed["env"] = env; taskAfterConstructed["env"] = env;
        taskBeforeReconstructed["model_provider"] = model_provider; taskAfterConstructed["model_provider"] = model_provider;
        taskBeforeReconstructed["model"] = model; taskAfterConstructed["model"] = model;
        taskBeforeReconstructed["num_trials"] = num_trials; taskAfterConstructed["num_trials"] = num_trials;
        taskBeforeReconstructed["temperature"] = temperature; taskAfterConstructed["temperature"] = temperature;
        taskBeforeReconstructed["interface_num"] = interface_num; taskAfterConstructed["interface_num"] = interface_num;
        taskBeforeReconstructed["task"] = new Map(); taskAfterConstructed["task"] = new Map();
        taskBeforeReconstructed["task"].set("user_id", user_id); taskAfterConstructed["task"].set("user_id", user_id);
        taskBeforeReconstructed["task"].set("instruction", instruction); taskAfterConstructed["task"].set("instruction", instruction);
        taskBeforeReconstructed["task"].set("actions", actionsBefore); taskAfterConstructed["task"].set("actions", getTaskActions());
        taskBeforeReconstructed["task"].set("edges", edgesBefore); taskAfterConstructed["task"].set("edges", edgesBefore);

        // console.log(taskBeforeReconstructed)
        document.getElementById("text1").value = JSON.stringify(
        { ...taskBeforeReconstructed, task: mapToObj(taskBeforeReconstructed["task"]) },
        null,
        2
        );
        document.getElementById("text2").value = JSON.stringify(
            { ...taskAfterConstructed, task: mapToObj(taskAfterConstructed["task"]) },
            null,
            2
        );

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
