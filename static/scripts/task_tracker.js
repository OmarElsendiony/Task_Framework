var github_username_mapping = new Object();
var tasks_info = null;
var username_email_mapping = {};

////////// TEAM STRUCTURE CONSTANTS ////////////
var domains = new Set();
var pods = new Set();
var calibrators = new Set();
var trainers = new Set();
var pod_trainers = new Map();
var calibrator_pods = new Map();
////////////////////////////////////////////////
var podFiltered = false;
var lastPodFilter = null;
////////// TEAM STRUCTURE CONSTANTS ////////////

// Function to get day name from date
function getDayName(dateString) {
    const date = new Date(dateString);
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return days[date.getDay()];
}

// Function to populate dropdown options
function populateDropdowns() {
    populateWeekDropdown();
    populatePodDropdown();
    populateTrainerDropdown();
    populateComplexityDropdown();
    populateDomainsDropDown();
    populateCalibratorDropdown();
    populateInterfaceDropdown();
}

function populateCalibratorDropdown(){
    const calibratorSelect = document.getElementById('calibratorFilter');
    const calibratorsList = Array.from(calibrators);
    calibratorSelect.innerHTML = '<option value="all">All Calibrators</option>';
    calibratorsList.forEach(calibrator => {
        if (calibrator && calibrator.trim()) {
            const option = document.createElement('option');
            option.value = calibrator;
            option.textContent = calibrator;
            calibratorSelect.appendChild(option);
        }
    });
}

function populateInterfaceDropdown() {
    const interfaceSelect = document.getElementById('interfaceFilter');
    interfaceSelect.innerHTML = '<option value="all">All Interfaces</option>';

    for (let i = 0; i < 5; i++){
        const option = document.createElement('option');
        option.value = i + 1;
        option.textContent = i + 1;
        interfaceSelect.appendChild(option);
    };
}

function populateDomainsDropDown() {
    const domainSelect = document.getElementById('domainFilter');
    const domainsList = Array.from(domains);
    
    domainSelect.innerHTML = '<option value="all">All Domains</option>';
    domainsList.forEach(domain => {
        if (domain && domain.trim()) {
            const option = document.createElement('option');
            option.value = domain;
            option.textContent = domain;
            domainSelect.appendChild(option);
        }
    });
}

function populateWeekDropdown() {
    const weekSelect = document.getElementById('weekFilter');
    const weeks = new Set();
    
    if (tasks_info) {
        tasks_info.forEach(task => {
            if (task['Week num']) {
                weeks.add(task['Week num']);
            }
        });
    }

    weekSelect.innerHTML = '<option value="all">All Weeks</option>';
    Array.from(weeks).sort().forEach(week => {
        const option = document.createElement('option');
        option.value = week;
        option.textContent = week.replace('_', ' ').toUpperCase();
        weekSelect.appendChild(option);
    });
}

function populatePodDropdown() {
    const podSelect = document.getElementById('podFilter');
    const podsList = Array.from(pods);
    
    podSelect.innerHTML = '<option value="all">All Pods</option>';
    podsList.forEach(pod => {
        if (pod && pod.trim()) {
            const option = document.createElement('option');
            option.value = pod;
            option.textContent = pod;
            podSelect.appendChild(option);
        }
    });
}

function populateTrainerDropdown() {
    const trainerSelect = document.getElementById('trainerFilter');
    
    const trainersList = Array.from(trainers);
    trainerSelect.innerHTML = '<option value="all">All Trainers</option>';
    trainersList.forEach(trainer => {
        if (trainer && trainer.trim()) {
            const option = document.createElement('option');
            option.value = trainer;
            option.textContent = trainer;
            trainerSelect.appendChild(option);
        }
    });
}

function populateComplexityDropdown() {
    const complexitySelect = document.getElementById('complexityFilter');
    const complexities = new Set();
    
    if (tasks_info) {
        tasks_info.forEach(task => {
            if (task['Complexity']) {
                complexities.add(task['Complexity'].trim().toLowerCase());
                task['Complexity'] = task['Complexity'].trim().toLowerCase();
            }
        });
    }
    console.log(complexities)
    complexitySelect.innerHTML = '<option value="all">All Complexities</option>';
    Array.from(complexities).sort().forEach(complexity => {
        const option = document.createElement('option');
        option.value = complexity;
        option.textContent = complexity.charAt(0).toUpperCase() + complexity.slice(1);
        complexitySelect.appendChild(option);
    });
}

function podFilterPreprocessing(podFilter) {
    const trainerSelect = document.getElementById('trainerFilter');
    if (podFilter != 'all'){
        // if (lastPodFilter !== podFilter) {
            trainerSelect.innerHTML = '';
            trainerSelect.innerHTML = '<option value="all">All Trainers</option>';
            const podTrainers = pod_trainers.get(podFilter) || new Set();
            podTrainers.forEach(trainer => {
                if (trainer && trainer.trim()) {
                    const option = document.createElement('option');
                    option.value = trainer;
                    option.textContent = trainer;
                    trainerSelect.appendChild(option);
                }
            });
        // }
    } else {
        populateTrainerDropdown();
    }
}

function calibratorFilterPreprocessing(calibratorFilter) {
    const podSelect = document.getElementById('podFilter');
    const trainerSelect = document.getElementById('trainerFilter');
    trainerSelect.innerHTML = '<option value="all">All Trainers</option>';

    if (calibratorFilter != 'all') {
        podSelect.innerHTML = '';
        podSelect.innerHTML = '<option value="all">All Pods</option>';
        const calibratorPods = calibrator_pods.get(calibratorFilter) || new Set();
        // console.log('Calibrator Pods:', calibratorPods);
        calibratorPods.forEach(pod => {
            if (pod && pod.trim()) {
                const option = document.createElement('option');
                option.value = pod;
                option.textContent = pod;
                podSelect.appendChild(option);
                const podTrainers = pod_trainers.get(pod) || new Set();
                podTrainers.forEach(trainer => {
                if (trainer && trainer.trim()) {
                        const option = document.createElement('option');
                        option.value = trainer;
                        option.textContent = trainer;
                        trainerSelect.appendChild(option);
                    }
                });
            }
        });
    } else {
        populatePodDropdown();
        populateTrainerDropdown();
    }
}

// Function to generate table data based on filters
function generateTableData(element) {
    if (!tasks_info || tasks_info.length === 0) {
        return null;
    }
    filterChanged = null;
    if (element !== null && element !== undefined) {
        filterChanged = element.id
    }
    const domainFilter = document.getElementById('domainFilter').value;
    // if (filterChanged !== null && filterChanged === 'domainFilter') {
    //     updateDomainAnalytics(domainFilter);
    // }
    const interfaceFilter = document.getElementById('interfaceFilter').value;
    
    // Get filter values
    const calibratorFilter = document.getElementById('calibratorFilter').value;
    // if (filterChanged !== null && filterChanged === 'calibratorFilter') {
    //     calibratorFilterPreprocessing(calibratorFilter);
    // }
    const podFilter = document.getElementById('podFilter').value;
    // if (filterChanged !== null && filterChanged === 'podFilter') {
    //     podFilterPreprocessing(podFilter);
    // }

    

    const weekFilter = document.getElementById('weekFilter').value;
    const trainerFilter = document.getElementById('trainerFilter').value;
    const complexityFilter = document.getElementById('complexityFilter').value;

    // Filter tasks based on selected filters
    let filteredTasks = tasks_info.filter(task => {
        /* if (github_username_mapping[task['GitHub username'].toLowerCase()] === undefined){
            console.log('Trainer Filter Match:', task['GitHub username'], '->', github_username_mapping[task['GitHub username'].toLowerCase()]);
        } */
        // console.log('Filtering Task:', task['GitHub username'], '->', github_username_mapping[task['GitHub username'].toLowerCase()]);
        // console.log('trainer filter:', trainerFilter);
        // return true;
        return (weekFilter === 'all' || task['Week num'] === weekFilter) &&
            (podFilter === 'all' || task['Lead'] === podFilter) &&
            (trainerFilter === 'all' || github_username_mapping[task['GitHub username'].toLowerCase()] !== undefined && github_username_mapping[task['GitHub username'].toLowerCase()].toLowerCase() === trainerFilter.toLowerCase()) &&
            (complexityFilter === 'all' || task['Complexity'] === complexityFilter) &&
            (domainFilter === 'all' || task['Domain'] === domainFilter) &&
            (calibratorFilter === 'all' || task['Calibrator'] === calibratorFilter) &&
            (interfaceFilter === 'all' || task['Interface'] === interfaceFilter);
    });

    // Group by week, date, and user
    const groupedData = {};
    const groupedStatsData = {};
    
    filteredTasks.forEach(task => {
        const week = task['Week num'] || 'Unknown Week';
        if ('Unknown Week' === week) {
            return;
        }
        const createdDate = new Date(task['Created Date (completed)']);
        const dateKey = createdDate.toISOString().split('T')[0]; // YYYY-MM-DD format
        const dayName = getDayName(task['Created Date (completed)']);
        const username = task['GitHub username'].toLowerCase() || 'Unknown User';
        const actual_name = github_username_mapping[username] || username;
        const complexity = task['Complexity'] || 'unknown';


        /////// GROUPING TRAINERS STATS DATA FOR RENDER TABLE //////////
        if (!groupedStatsData[actual_name]) {
            groupedStatsData[actual_name] = {
                merged: 0,
                resubmitted: 0,
                discarded: 0,
                pending_review: 0,
                ready_to_merge: 0,
                needs_changes: 0,
                expert_review_pending_tasks: 0,
                expert_reject_tasks: 0,
                expert_approved_tasks: 0
            };
        }
        if (task['Pull Request Status'] === 'Merged') {
            groupedStatsData[actual_name].merged++;
        } else if (task['Pull Request Status'] === 'discarded') {
            groupedStatsData[actual_name].discarded++;
        } else if (task['Pull Request Status'] === 'resubmitted') {
            groupedStatsData[actual_name].resubmitted++;
        } else if (task['Pull Request Status'] === 'pending review') {
            groupedStatsData[actual_name].pending_review++;
        } else if (task['Pull Request Status'] === 'ready to merge') {
            groupedStatsData[actual_name].ready_to_merge++;
        } else if (task['Pull Request Status'] === 'needs changes') {
            groupedStatsData[actual_name].needs_changes++;
        } else if (task['Pull Request Status'] === 'expert review pending') {
            groupedStatsData[actual_name].expert_review_pending_tasks++;
        } else if (task['Pull Request Status'] === 'expert reject') {
            groupedStatsData[actual_name].expert_reject_tasks++;
        } else if (task['Pull Request Status'] === 'expert approved') {
            groupedStatsData[actual_name].expert_approved_tasks++;
        }


        /////// GROUPING STATS DATA FOR RENDER TABLE //////////
        if (!groupedData[week]) {
            groupedData[week] = {};
        }
        if (!groupedData[week][dayName]) {
            groupedData[week][dayName] = {
                dayName: dayName,
                users: {}
            };
        }
        if (!groupedData[week][dayName].users[actual_name]) {
            groupedData[week][dayName].users[actual_name] = {
                expert: 0,
                hard: 0,
                medium: 0,
                total: 0
            };
        }

        groupedData[week][dayName].users[actual_name][complexity]++;
        groupedData[week][dayName].users[actual_name].total++;
    });

    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

            // Ensure all days exist for each week in the correct order
    for (const week in groupedData) {
        // Create a new ordered object for this week
        const orderedWeekData = {};
        
        // Add days in the correct order (Monday to Sunday)
        days.forEach(dayName => {
            if (groupedData[week][dayName]) {
                orderedWeekData[dayName] = groupedData[week][dayName];
            } else {
                orderedWeekData[dayName] = {
                    dayName: dayName,
                    users: {}
                };
            }
        });
        
        // Replace the week data with the ordered version
        groupedData[week] = orderedWeekData;
    }

    // Sort weeks
    const sortedWeeks = Object.keys(groupedData).sort((a, b) => {
        const weekA = a.replace('_', ' ').toUpperCase();
        const weekB = b.replace('_', ' ').toUpperCase();
        return weekA.localeCompare(weekB);
    });

    // Create final sorted structure
    const sortedGroupedData = {};
    sortedWeeks.forEach(week => {
        sortedGroupedData[week] = groupedData[week];
    });

    // console.log('Grouped Stats Data:', groupedStatsData);
    trainerStats = [];
    for (const trainer in groupedStatsData) {
        const stats = groupedStatsData[trainer];
        const totalTasks = stats.merged + stats.resubmitted + stats.discarded + 
                   stats.pending_review + stats.ready_to_merge + stats.needs_changes +
                   stats.expert_review_pending_tasks + stats.expert_reject_tasks + stats.expert_approved_tasks;
        const mergedPercent = totalTasks > 0 ? (stats.merged / totalTasks * 100).toFixed(1) : 0;
        const resubmittedPercent = totalTasks > 0 ? (stats.resubmitted / totalTasks * 100).toFixed(1) : 0;
        const discardedPercent = totalTasks > 0 ? (stats.discarded / totalTasks * 100).toFixed(1) : 0;
        const pending_reviewPercent = totalTasks > 0 ? (stats.pending_review / totalTasks * 100).toFixed(1) : 0;
        const ready_to_mergePercent = totalTasks > 0 ? (stats.ready_to_merge / totalTasks * 100).toFixed(1) : 0;
        const needs_changesPercent = totalTasks > 0 ? (stats.needs_changes / totalTasks * 100).toFixed(1) : 0;
        const expert_review_pendingPercent = totalTasks > 0 ? (stats.expert_review_pending_tasks / totalTasks * 100).toFixed(1) : 0;
        const expert_rejectPercent = totalTasks > 0 ? (stats.expert_reject_tasks / totalTasks * 100).toFixed(1) : 0;
        const expert_approvedPercent = totalTasks > 0 ? (stats.expert_approved_tasks / totalTasks * 100).toFixed(1) : 0;

        trainerStats.push({
            trainer: trainer,
            merged: stats.merged,
            mergedPercent: parseFloat(mergedPercent),
            resubmitted: stats.resubmitted,
            resubmittedPercent: parseFloat(resubmittedPercent),
            discarded: stats.discarded,
            discardedPercent: parseFloat(discardedPercent),
            pending_review: stats.pending_review,
            pending_reviewPercent: parseFloat(pending_reviewPercent),
            ready_to_merge: stats.ready_to_merge,
            ready_to_mergePercent: parseFloat(ready_to_mergePercent),
            needs_changes: stats.needs_changes,
            needs_changesPercent: parseFloat(needs_changesPercent),
            expert_review_pending: stats.expert_review_pending_tasks,   
            expert_review_pendingPercent: parseFloat(expert_review_pendingPercent),
            expert_reject: stats.expert_reject_tasks,
            expert_rejectPercent: parseFloat(expert_rejectPercent),
            expert_approved: stats.expert_approved_tasks,
            expert_approvedPercent: parseFloat(expert_approvedPercent)
        });
    }
    return groupedData;
}


function renderTrainerStatsTable() {
    const tableContainer = document.getElementById('trainerStatsDisplay');
    
    if (!trainerStats || trainerStats.length === 0) {
        tableContainer.innerHTML = '<div class="no-data">No trainer statistics available</div>';
        return;
    }

    // Calculate totals
    const totals = {
        merged: trainerStats.reduce((sum, trainer) => sum + trainer.merged, 0),
        resubmitted: trainerStats.reduce((sum, trainer) => sum + trainer.resubmitted, 0),
        discarded: trainerStats.reduce((sum, trainer) => sum + trainer.discarded, 0),
        pending_review: trainerStats.reduce((sum, trainer) => sum + (trainer.pending_review || 0), 0),
        ready_to_merge: trainerStats.reduce((sum, trainer) => sum + (trainer.ready_to_merge || 0), 0),
        needs_changes: trainerStats.reduce((sum, trainer) => sum + (trainer.needs_changes || 0), 0),
        expert_review_pending: trainerStats.reduce((sum, trainer) => sum + (trainer.expert_review_pending || 0), 0),
        expert_reject: trainerStats.reduce((sum, trainer) => sum + (trainer.expert_reject || 0), 0),
        expert_approved: trainerStats.reduce((sum, trainer) => sum + (trainer.expert_approved || 0), 0),
    };

    const totalTasks = totals.merged + totals.resubmitted + totals.discarded + totals.pending_review + totals.ready_to_merge + totals.needs_changes + totals.expert_review_pending + totals.expert_reject + totals.expert_approved;
    // console.log('Total Tasks:', totalTasks);
    let tableHTML = `
        <div class="table-wrapper">
            <table class="trainer-stats-table">
                <thead>
                    <tr>
                        <th>Trainer</th>
                        <th class="merged-stat">Merged</th>
                        <th class="percentage-stat">Merged %</th>
                        <th class="resubmitted-stat">Resubmitted</th>
                        <th class="percentage-stat">Resubmitted %</th>
                        <th class="discarded-stat">Discarded</th>
                        <th class="percentage-stat">Discarded %</th>
                        <th class="pending-review-stat">Pending Review</th>
                        <th class="percentage-stat">Pending Review %</th>
                        <th class="ready-to-merge-stat">Ready to Merge</th>
                        <th class="percentage-stat">Ready to Merge %</th>
                        <th class="needs-changes-stat">Needs Changes</th>
                        <th class="percentage-stat">Needs Changes %</th>
                        <th class="expert-review-pending-stat">Expert Review Pending</th>
                        <th class="percentage-stat">Expert Review Pending %</th>
                        <th class="expert-reject-stat">Expert Reject</th>
                        <th class="percentage-stat">Expert Reject %</th>
                        <th class="expert-approved-stat">Expert Approved</th>
                        <th class="percentage-stat">Expert Approved %</th>
                    </tr>
                </thead>
                <tbody>`;

    // Add data rows
    trainerStats.forEach(trainer => {
        tableHTML += `
            <tr>
                <td class="trainer-name">${trainer.trainer}</td>
                <td class="merged-stat">${trainer.merged}</td>
                <td class="percentage-stat">${trainer.mergedPercent.toFixed(1)}%</td>
                <td class="resubmitted-stat">${trainer.resubmitted}</td>
                <td class="percentage-stat">${trainer.resubmittedPercent.toFixed(1)}%</td>
                <td class="discarded-stat">${trainer.discarded}</td>
                <td class="percentage-stat">${trainer.discardedPercent.toFixed(1)}%</td>
                <td class="pending-review-stat">${trainer.pending_review}</td>
                <td class="percentage-stat">${trainer.pending_reviewPercent.toFixed(1)}%</td>
                <td class="ready-to-merge-stat">${trainer.ready_to_merge}</td>
                <td class="percentage-stat">${trainer.ready_to_mergePercent.toFixed(1)}%</td>
                <td class="needs-changes-stat">${trainer.needs_changes}</td>
                <td class="percentage-stat">${trainer.needs_changesPercent.toFixed(1)}%</td>
                <td class="expert-review-pending-stat">${trainer.expert_review_pending || 0}</td>
                <td class="percentage-stat">${(trainer.expert_review_pendingPercent || 0).toFixed(1)}%</td>
                <td class="expert-reject-stat">${trainer.expert_reject || 0}</td>
                <td class="percentage-stat">${(trainer.expert_rejectPercent || 0).toFixed(1)}%</td>
                <td class="expert-approved-stat">${trainer.expert_approved || 0}</td>
                <td class="percentage-stat">${(trainer.expert_approvedPercent || 0).toFixed(1)}%</td>
            </tr>`;
    });

    // Add total row
    const totalMergedPercent = totalTasks > 0 ? (totals.merged / totalTasks * 100).toFixed(1) : 0;
    const totalResubmittedPercent = totalTasks > 0 ? (totals.resubmitted / totalTasks * 100).toFixed(1) : 0;
    const totalDiscardedPercent = totalTasks > 0 ? (totals.discarded / totalTasks * 100).toFixed(1) : 0;
    const totalPendingReviewPercent = totalTasks > 0 ? (totals.pending_review / totalTasks * 100).toFixed(1) : 0;
    const totalReadyToMergePercent = totalTasks > 0 ? (totals.ready_to_merge / totalTasks * 100).toFixed(1) : 0;
    const totalNeedsChangesPercent = totalTasks > 0 ? (totals.needs_changes / totalTasks * 100).toFixed(1) : 0;
    const totalExpertReviewPendingPercent = totalTasks > 0 ? (totals.expert_review_pending / totalTasks * 100).toFixed(1) : 0;
    const totalExpertRejectPercent = totalTasks > 0 ? (totals.expert_reject / totalTasks * 100).toFixed(1) : 0;
    const totalExpertApprovedPercent = totalTasks > 0 ? (totals.expert_approved / totalTasks * 100).toFixed(1) : 0;

    tableHTML += `
            <tr class="total-row">
                <td class="trainer-name">Total</td>
                <td class="merged-stat">${totals.merged}</td>
                <td class="percentage-stat">${totalMergedPercent}%</td>
                <td class="resubmitted-stat">${totals.resubmitted}</td>
                <td class="percentage-stat">${totalResubmittedPercent}%</td>
                <td class="discarded-stat">${totals.discarded}</td>
                <td class="percentage-stat">${totalDiscardedPercent}%</td>
                <td class="pending-review-stat">${totals.pending_review}</td>
                <td class="percentage-stat">${totalPendingReviewPercent}%</td>
                <td class="ready-to-merge-stat">${totals.ready_to_merge}</td>
                <td class="percentage-stat">${totalReadyToMergePercent}%</td>
                <td class="needs-changes-stat">${totals.needs_changes}</td>
                <td class="percentage-stat">${totalNeedsChangesPercent}%</td>
                <td class="expert-review-pending-stat">${totals.expert_review_pending}</td>
                <td class="percentage-stat">${totalExpertReviewPendingPercent}%</td>
                <td class="expert-reject-stat">${totals.expert_reject}</td>
                <td class="percentage-stat">${totalExpertRejectPercent}%</td>
                <td class="expert-approved-stat">${totals.expert_approved}</td>
                <td class="percentage-stat">${totalExpertApprovedPercent}%</td>
            </tr>
                </tbody>
            </table>
        </div>`;

    tableContainer.innerHTML = tableHTML;
}

// Function to render the table
function renderTable(element) {
    /* if (element !== null && element !== undefined) {
        console.log(element.value)
        console.log(element.id)
    } */
    const tableData = generateTableData(element);
    const tableContainer = document.getElementById('tasksDisplay');
    
    if (!tableData || Object.keys(tableData).length === 0) {
        tableContainer.innerHTML = '<div class="no-data">No data available for the selected filters</div>';
        return;
    }

    // Define days in correct order (Monday to Sunday)
    const daysOrder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

    // Get all unique users across all filtered data
    const allUsers = new Set();
    Object.values(tableData).forEach(weekData => {
        Object.values(weekData).forEach(dateData => {
            Object.keys(dateData.users).forEach(user => allUsers.add(user));
        });
    });

    const users = Array.from(allUsers).sort();

    let tableHTML = `
        <div class="table-wrapper">
            <table class="task-table">
                <thead>
                    <tr>
                        <th>Week</th>
                        <th>Date</th>`;

    // Add user columns
    users.forEach(user => {
        tableHTML += `
            <th colspan="4">${user}</th>`;
    });

    tableHTML += `</tr><tr>
                        <th></th>
                        <th></th>`;

    // Add complexity headers for each user
    users.forEach(user => {
        tableHTML += `
            <th class="complexity-expert">Expert</th>
            <th class="complexity-hard">Hard</th>
            <th class="complexity-medium">Medium</th>
            <th class="total-cell">Total</th>`;
    });

    tableHTML += `</tr></thead><tbody>`;

    // Add data rows
    Object.keys(tableData).sort().forEach(week => {
        const weekData = tableData[week];
        let weekTotals = {};
        users.forEach(user => {
            weekTotals[user] = { expert: 0, hard: 0, medium: 0, total: 0 };
        });

        // Show all days (Monday to Sunday) for each week
        daysOrder.forEach(dayName => {
            // Get data for this day, or create empty structure if it doesn't exist
            const dateData = weekData[dayName] || {
                dayName: dayName,
                users: {}
            };
            
            tableHTML += `
                <tr>
                    <td class="week-cell">${week.replace('_', ' ').toUpperCase()}</td>
                    <td class="date-cell">${dateData.dayName}</td>`;

            users.forEach(user => {
                const userData = dateData.users[user] || { expert: 0, hard: 0, medium: 0, total: 0 };
                weekTotals[user].expert += userData.expert;
                weekTotals[user].hard += userData.hard;
                weekTotals[user].medium += userData.medium;
                weekTotals[user].total += userData.total;

                tableHTML += `
                    <td class="complexity-expert">${userData.expert}</td>
                    <td class="complexity-hard">${userData.hard}</td>
                    <td class="complexity-medium">${userData.medium}</td>
                    <td class="total-cell">${userData.total}</td>`;
            });

            tableHTML += `</tr>`;
        });

        // Add week total row
        tableHTML += `
            <tr class="week-total-row" style="border-top: 2px solid rgba(102, 126, 234, 0.8); background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2)); font-weight: bold;">
                <td class="week-cell" style="background: rgba(102, 126, 234, 0.3); color: #667eea; font-weight: bold;">${week.replace('_', ' ').toUpperCase()}</td>
                <td class="total-cell" style="background: rgba(102, 126, 234, 0.25); color: #667eea; font-weight: bold; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">Total</td>`;

        users.forEach(user => {
            tableHTML += `
                <td class="complexity-expert" style="background: rgba(255, 107, 107, 0.2); color: #ff6b6b; font-weight: bold; border: 1px solid rgba(255, 107, 107, 0.3);">${weekTotals[user].expert}</td>
                <td class="complexity-hard" style="background: rgba(255, 167, 38, 0.2); color: #ffa726; font-weight: bold; border: 1px solid rgba(255, 167, 38, 0.3);">${weekTotals[user].hard}</td>
                <td class="complexity-medium" style="background: rgba(102, 187, 106, 0.2); color: #66bb6a; font-weight: bold; border: 1px solid rgba(102, 187, 106, 0.3);">${weekTotals[user].medium}</td>
                <td class="total-cell" style="background: rgba(102, 126, 234, 0.3); color: #667eea; font-weight: bold; border: 2px solid rgba(102, 126, 234, 0.5); text-shadow: 0 1px 2px rgba(0,0,0,0.3);">${weekTotals[user].total}</td>`;
        });

        tableHTML += `</tr>`;

        // Add distribution percentage row
        tableHTML += `
            <tr class="week-distribution-row" style="border-top: 1px solid rgba(118, 75, 162, 0.6); background: linear-gradient(135deg, rgba(118, 75, 162, 0.15), rgba(102, 126, 234, 0.15)); ">
                <td class="week-cell" style="background: rgba(118, 75, 162, 0.25); color: #764ba2; font-weight: bold; ">${week.replace('_', ' ').toUpperCase()}</td>
                <td class="total-cell" style="background: rgba(118, 75, 162, 0.2); color: #764ba2; font-weight: bold; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">Distribution</td>`;

        users.forEach(user => {
            const total = weekTotals[user].total;
            let expertPercent = '0.0%';
            let hardPercent = '0.0%';
            let mediumPercent = '0.0%';

            if (total > 0) {
                expertPercent = ((weekTotals[user].expert / total) * 100).toFixed(1) + '%';
                hardPercent = ((weekTotals[user].hard / total) * 100).toFixed(1) + '%';
                mediumPercent = ((weekTotals[user].medium / total) * 100).toFixed(1) + '%';
            }

            tableHTML += `
                <td class="complexity-expert" style="background: rgba(255, 107, 107, 0.15); color: #ff8a80; font-weight: 600; font-style: italic; border: 1px solid rgba(255, 107, 107, 0.2); text-shadow: 0 1px 1px rgba(0,0,0,0.2);">${expertPercent}</td>
                <td class="complexity-hard" style="background: rgba(255, 167, 38, 0.15); color: #ffb74d; font-weight: 600; font-style: italic; border: 1px solid rgba(255, 167, 38, 0.2); text-shadow: 0 1px 1px rgba(0,0,0,0.2);">${hardPercent}</td>
                <td class="complexity-medium" style="background: rgba(102, 187, 106, 0.15); color: #81c784; font-weight: 600; font-style: italic; border: 1px solid rgba(102, 187, 106, 0.2); text-shadow: 0 1px 1px rgba(0,0,0,0.2);">${mediumPercent}</td>
                <td class="total-cell" style="background: rgba(118, 75, 162, 0.25); color: #764ba2; font-weight: bold; font-style: italic; border: 2px solid rgba(118, 75, 162, 0.4); text-shadow: 0 1px 2px rgba(0,0,0,0.3);">100.0%</td>`;
        });

        tableHTML += `</tr>`;
    });

    tableHTML += `</tbody></table></div>`;
    tableContainer.innerHTML = tableHTML;
}

// Function to reload tracker data
function reloadTrackerData() {
    const reloadBtn = document.getElementById('reloadBtn');
    const originalText = reloadBtn.innerHTML;
    const spinner = '<span class="loading-spinner"></span>';
    
    reloadBtn.innerHTML = spinner + ' Reloading...';
    reloadBtn.disabled = true;

    // Simulate API call to reload tracker data
    fetch('/tracker', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        // console.log('Tracker data reloaded:', data);
        reloadBtn.innerHTML = 'Reloaded &#10003;';
        tasks_info = data.tasks_info || [];
        username_email_mapping = data.username_email_mapping || {};
        
        for (const user of username_email_mapping) {
            if (user["Github Username"]) {
                github_username_mapping[user['Github Username'].toLowerCase()] = user['Actual name'].toLowerCase().trim();
            }
        }
        // console.log('GitHub Username to Name Mapping:', github_username_mapping);

        var show_trainer_pod = new Map(); // show trainer pod
        var show_pod_calibrator = new Map(); // show pod calibrator
        for (const team_structure of data.team_structure) {
            pods.add(team_structure['Pod Lead']);
            calibrators.add(team_structure['Calibrator']);
            if (calibrator_pods.get(team_structure['Calibrator']) !== undefined) {
                calibrator_pods.get(team_structure['Calibrator']).add(team_structure['Pod Lead']);
            } else {
                calibrator_pods.set(team_structure['Calibrator'], new Set([team_structure['Pod Lead']]));
            }
            // calibrator_pods.set(team_structure['Calibrator'], team_structure['Pod Lead']);
            show_pod_calibrator.set(team_structure['Pod Lead'], team_structure['Calibrator']);
            trainers_of_pod = new Set();
            const partialKey = 'Trainer';
            for (const key in team_structure) {
                if (key.startsWith(partialKey)) {
                    trainers.add(team_structure[key].toLowerCase().trim());
                    show_trainer_pod.set(team_structure[key].toLowerCase().trim(), team_structure['Pod Lead']);
                    trainers_of_pod.add(team_structure[key].toLowerCase().trim());
                }
            }
            pod_trainers.set(team_structure['Pod Lead'], trainers_of_pod);
        }
        // console.log('Pods:', pod_trainers);
        // console.log('Pods:', show_trainer_pod);


        for (const task of tasks_info) {
            domains.add(task['Domain']);
            if (!task['Lead'] || task['Lead'] === "Unknown Pod") {
                task['Lead'] = show_trainer_pod.get(github_username_mapping[task['GitHub username'].toLowerCase()]) || "Unknown Pod";
                task['Calibrator'] = show_pod_calibrator.get(task['Lead']) || "Unknown Calibrator";
            }
        }
        
        console.log('Tasks Info:', tasks_info);

        // current_domain = tasks_info[0]['Domain'] // current domain is the last submitted domain as of now
        current_domain = 'finance' // current domain is the last submitted domain as of now

        updateDomainAnalytics(current_domain)
        // Populate dropdowns and render table
        populateDropdowns();
        renderTable();
        renderTrainerStatsTable();
        
        setTimeout(() => {
            reloadBtn.innerHTML = originalText;
            reloadBtn.disabled = false;
        }, 2000);
    })
    .catch(error => {
        console.error('Error reloading tracker data:', error);
        reloadBtn.innerHTML = '❌ Error';
        setTimeout(() => {
            reloadBtn.innerHTML = originalText;
            reloadBtn.disabled = false;
        }, 2000);
    });
}

function updateDomainAnalytics(current_domain) {
    document.getElementById('currentDomain').textContent = current_domain;
    tasks_occurred = new Set();
    tasks_completed = 0;
    merged_tasks = 0;
    discarded_tasks = 0;
    ready_to_merge_tasks = 0;
    pending_review_tasks = 0;
    needs_changes_tasks = 0;
    resubmitted_tasks = 0;
    expert_review_pending_tasks = 0;
    expert_reject_tasks = 0;
    expert_approved_tasks = 0;
    for (const task of tasks_info) {
        if (task['Domain'] == current_domain && !tasks_occurred.has(task['Task'])) {
            tasks_completed += 1;
            if (task['Pull Request Status'] === 'Merged') {
                merged_tasks += 1;
            }
            if (task['Pull Request Status'] === 'ready to merge') {
                ready_to_merge_tasks += 1;
            }
            if (task['Pull Request Status'] === 'discarded') {
                discarded_tasks += 1;
            }
            if (task['Pull Request Status'] === 'pending review') {
                pending_review_tasks += 1;
            }
            if (task['Pull Request Status'] === 'needs changes') {
                needs_changes_tasks += 1;
            }
            if (task['Pull Request Status'] === 'resubmitted') {
                resubmitted_tasks += 1;
            }
            if (task['Pull Request Status'] === 'expert review pending') {
                expert_review_pending_tasks += 1;
            }
            if (task['Pull Request Status'] === 'expert reject') {
                expert_reject_tasks += 1;
            }
            if (task['Pull Request Status'] === 'expert approved') {
                expert_approved_tasks += 1;
            }
            tasks_occurred.add(task['Task']);
        }
    }

    const TASKS_TO_BE_COMPLETED = 200; 
    analytics = {
        totalTasks: tasks_completed,
        activePods: pods.size,
        pendingReviewTasks: pending_review_tasks,
        totalMergedTasks: merged_tasks,
        totalNeedsChangesTasks: needs_changes_tasks,
        totalResubmittedTasks: resubmitted_tasks,
        totalDiscardedTasks: discarded_tasks,
        readyToMergeTasks: ready_to_merge_tasks,
        completionRate: (merged_tasks / TASKS_TO_BE_COMPLETED * 100).toFixed(2)
    };

    updateAnalytics(analytics);
}
// Function to update analytics display
function updateAnalytics(analytics) {
    if (analytics.totalTasks !== undefined) {
        document.getElementById('totalTasks').textContent = analytics.totalTasks;
    }
    if (analytics.activePods !== undefined) {
        document.getElementById('activePods').textContent = analytics.activePods;
    }
    if (analytics.totalResubmittedTasks !== undefined) {
        document.getElementById('totalResubmittedTasks').textContent = analytics.totalResubmittedTasks;
    }
    if (analytics.totalNeedsChangesTasks !== undefined) {
        document.getElementById('totalNeedsChangesTasks').textContent = analytics.totalNeedsChangesTasks;
    }
    if (analytics.pendingReviewTasks !== undefined) {
        document.getElementById('pendingReviewTasks').textContent = analytics.pendingReviewTasks;
    }
    if (analytics.totalMergedTasks !== undefined) {
        document.getElementById('totalMergedTasks').textContent = analytics.totalMergedTasks;
    }
    if (analytics.totalDiscardedTasks !== undefined) {
        document.getElementById('totalDiscardedTasks').textContent = analytics.totalDiscardedTasks;
    }
    if (analytics.readyToMergeTasks !== undefined) {
        document.getElementById('readyToMergeTasks').textContent = analytics.readyToMergeTasks;
    }
    if (analytics.completionRate !== undefined) {
        document.getElementById('completionRate').textContent = analytics.completionRate + '%';
    }
}

// Function to apply filters
function applyFilters(element) {
    if (element.id === 'calibratorFilter') {
        calibratorFilterPreprocessing(element.value);
    }
    if (element.id === 'podFilter') {
        podFilterPreprocessing(element.value);
    }
    if (element.id === 'domainFilter') {
        // Also, add logic to handle the 'all' case here
        updateDomainAnalytics(element.value);
    }
    renderTable(element);
    renderTrainerStatsTable();
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners to filters
    document.querySelectorAll('.filter-select, .filter-input').forEach(element => {
        element.addEventListener('change', (e) => applyFilters(e.target));
    });

    // Show initial loading message
    document.getElementById('tasksDisplay').innerHTML = '<div class="no-data">Click "Reload Data" to load task information</div>';

    // Initial data load
    reloadTrackerData();
});
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("reloadBtn").addEventListener("click", function() {
    reloadTrackerData();
  });
});
