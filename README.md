# Task_Framework
Repository that aids utilities that help in the task creation

# How to Use

## Setup

The app files need to be in the same directory as the `envs` directory. We recommend cloning the repo and moving the `envs` directory to the cloned repo root directory. Note that you'll need to do this for every change in the interface/data to be updated. 

Alternative approaches include moving the repo files to the amazon repo (though you'll need to remove them from the staging area). Choose whatever approach fits your workflow best.

## What Can You Do With This Tool?

### 1. Test APIs
**For Trainers and Leads**
- **Trainers**: Ensure that your inputs to API functions are correct and get the output of API functions, especially when they involve calculations or information from multiple tables that might be confusing. This helps double-check your work by simply importing the task (explained in point 2).
- **Leads**: Verify that everything is correct without manually adding actions.

### 2. Import Actions List
Re-import the actions list when you want to redo something. As a lead, you can check that everything is correct without adding actions manually. 

**Why would a trainer need this?** Within a session (after clicking `GO`), APIs may depend on created IDs. If you want to modify something and ensure the flow is correct without re-inserting everything, you can import the actions list.

### 3. Export Actions
Export actions in the same format needed for task submission, including:
- Name
- Arguments  
- Output

**Note**: The output is ignored and left as an empty string when the API cannot be executed (e.g., when using placeholder IDs for created users, leaving it for you to fill in).

### 4. Save and Resume Work
If you need to stop working on a task and continue later, you have two options:

**Option A**: Export and then import your work
**Option B**: Save the state using the save button and continue from there

The save function downloads an HTML file to your system. To resume:
1. Re-open the downloaded HTML file
2. Start a server in the directory where the file was downloaded using:
   ```bash
   python3 -m http.server 8000
   ```
3. Continue operating from where you left off

### 5. Automate Edge Creation
Instead of manually creating edges, use the **Graph Editor Playground**:
- Add nodes with edges between them
- **Important**: Edge names must be in the format `x->y` where:
  - `x` is the output from the "from" node
  - `y` is the input to the "to" node
- Export the graph in the same format as the edges you'll submit

### 6. Populate Graph with Actions
- Populate the graph playground nodes with actions from your action list
- Draw the connections between nodes
- Export the completed graph

### 7. Import and Modify Existing Edges
- Import the edges of an existing task
- Modify them as necessary
- Export the updated version
