# main.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
import json
from task_runner import find_all_task_files, run_single_task, run_all_tasks, get_available_interfaces

app = Flask(__name__)
app.secret_key = "supersecretkey"

BASE_PATH = "tools_regression_tests"
OUTPUT_PATH = "tools_test_output"

# Ensure folders exist
os.makedirs(BASE_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)


@app.route("/")
def index():
    """List all JSON test files with results if available"""
    selected_interface = session.get('selected_interface', None)
    
    # Get available interfaces
    available_interfaces = get_available_interfaces(BASE_PATH)
    
    # Get task files for selected interface (or all if none selected)
    if selected_interface:
        search_path = os.path.join(BASE_PATH, selected_interface)
    else:
        search_path = BASE_PATH
    
    task_files = find_all_task_files(search_path)
    relative_files = [os.path.relpath(f, BASE_PATH) for f in task_files]
    
    # Check if results exist for each file
    files_with_status = []
    for f in relative_files:
        result_file = os.path.join(OUTPUT_PATH, f"{os.path.basename(f).split('.')[0]}_result.json")
        status = None
        if os.path.exists(result_file):
            with open(result_file, 'r') as rf:
                result_data = json.load(rf)
                # Determine status from actions
                if result_data.get('error'):
                    status = 'failed'
                elif result_data.get('actions'):
                    all_success = all(a.get('success', False) for a in result_data['actions'])
                    status = 'passed' if all_success else 'failed'
        
        # Get interface folder name
        interface_folder = os.path.dirname(f) if os.path.dirname(f) else 'root'
        
        files_with_status.append({
            'path': f,
            'name': os.path.basename(f),
            'interface': interface_folder,
            'status': status
        })
    
    # Get environment path from session
    envs_path = session.get('envs_path', 'envs')
    
    return render_template("index.html", 
                         files=files_with_status, 
                         envs_path=envs_path,
                         available_interfaces=available_interfaces,
                         selected_interface=selected_interface)


@app.route("/select_interface", methods=["POST"])
def select_interface():
    """Select which interface folder to view/test"""
    interface = request.form.get("interface", "")
    if interface == "all":
        session.pop('selected_interface', None)
        flash("Showing all interfaces", "info")
    else:
        session['selected_interface'] = interface
        flash(f"Selected interface: {interface}", "success")
    return redirect(url_for("index"))


@app.route("/settings", methods=["GET", "POST"])
def settings():
    """Configure environment path"""
    if request.method == "POST":
        envs_path = request.form.get("envs_path", "envs").strip()
        session['envs_path'] = envs_path
        flash(f"Environment path set to: {envs_path}", "success")
        return redirect(url_for("index"))
    
    current_path = session.get('envs_path', 'envs')
    return render_template("settings.html", current_path=current_path)


@app.route("/create", methods=["GET", "POST"])
def create():
    """Create a new JSON task"""
    available_interfaces = get_available_interfaces(BASE_PATH)
    
    if request.method == "POST":
        filename = request.form["filename"]
        env = request.form["env"]
        interface_num = request.form["interface_num"]
        interface_folder = request.form.get("interface_folder", "interface_1")
        action = request.form["actions"]
        
        try:
            action_parsed = json.loads(action)
        except json.JSONDecodeError as e:
            flash(f"Invalid JSON format in actions field: {str(e)}", "error")
            return redirect(url_for("create"))

        # Build a basic structure
        task_content = {
            "env": env,
            "interface_num": interface_num,
            "task": {"actions": [action_parsed]}
        }

        # Create interface folder if it doesn't exist
        interface_path = os.path.join(BASE_PATH, interface_folder)
        os.makedirs(interface_path, exist_ok=True)
        
        save_path = os.path.join(interface_path, f"{filename}.json")
        with open(save_path, "w") as f:
            json.dump(task_content, f, indent=2)

        flash(f"Task '{interface_folder}/{filename}.json' created successfully.", "success")
        return redirect(url_for("index"))
    
    return render_template("create.html", available_interfaces=available_interfaces)


@app.route("/view/<path:task_path>")
def view_task(task_path):
    """View JSON file content"""
    abs_path = os.path.join(BASE_PATH, task_path)
    if not os.path.exists(abs_path):
        flash("Task file not found!", "danger")
        return redirect(url_for("index"))
    with open(abs_path, "r") as f:
        content = json.load(f)
    return render_template("view.html", file=task_path, content=json.dumps(content, indent=2))


@app.route("/results/<path:task_path>")
def view_results(task_path):
    """View detailed test results"""
    result_file = os.path.join(OUTPUT_PATH, f"{os.path.basename(task_path).split('.')[0]}_result.json")
    
    if not os.path.exists(result_file):
        flash("No results found for this task. Run it first!", "warning")
        return redirect(url_for("index"))
    
    with open(result_file, 'r') as f:
        result_data = json.load(f)
    
    # Calculate statistics
    total_actions = len(result_data.get('actions', []))
    passed_actions = sum(1 for a in result_data.get('actions', []) if a.get('success', False))
    failed_actions = total_actions - passed_actions
    
    return render_template("results.html", 
                         task_path=task_path,
                         result=result_data,
                         total_actions=total_actions,
                         passed_actions=passed_actions,
                         failed_actions=failed_actions)


@app.route("/delete/<path:task_path>", methods=["POST"])
def delete(task_path):
    """Delete a JSON task"""
    abs_path = os.path.join(BASE_PATH, task_path)
    if os.path.exists(abs_path):
        os.remove(abs_path)
        # Also delete results if they exist
        result_file = os.path.join(OUTPUT_PATH, f"{os.path.basename(task_path).split('.')[0]}_result.json")
        if os.path.exists(result_file):
            os.remove(result_file)
        flash(f"Deleted task: {task_path}", "info")
    return redirect(url_for("index"))


@app.route("/run/<path:task_path>", methods=["POST"])
def run_single(task_path):
    """Run one test"""
    abs_path = os.path.join(BASE_PATH, task_path)
    envs_path = session.get('envs_path', 'envs')
    
    success, result = run_single_task(abs_path, envs_path=envs_path)
    output_path = os.path.join(OUTPUT_PATH, f"{os.path.basename(task_path).split('.')[0]}_result.json")

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    if success:
        flash(f"✅ '{task_path}' executed successfully", "success")
    else:
        error_msg = result.get('error', 'Unknown error')
        flash(f"❌ '{task_path}' failed: {error_msg}", "danger")
    
    return redirect(url_for("view_results", task_path=task_path))


@app.route("/run_all", methods=["POST"])
def run_all():
    """Run all JSON test files"""
    envs_path = session.get('envs_path', 'envs')
    selected_interface = session.get('selected_interface', None)
    
    # Determine which path to run
    if selected_interface:
        search_path = os.path.join(BASE_PATH, selected_interface)
        flash_msg = f"Running all tasks in {selected_interface}..."
    else:
        search_path = BASE_PATH
        flash_msg = "Running all tasks..."
    
    summary = run_all_tasks(search_path, envs_path=envs_path)
    flash(f"{flash_msg} Result: {summary['passed']} passed, {summary['failed']} failed. Pass rate: {summary['pass_rate']}", "info")
    return redirect(url_for("summary"))


@app.route("/summary")
def summary():
    """View summary of all test results"""
    summary_file = os.path.join(OUTPUT_PATH, "summary.json")
    
    if not os.path.exists(summary_file):
        flash("No test summary found. Run tests first!", "warning")
        return redirect(url_for("index"))
    
    with open(summary_file, 'r') as f:
        summary_data = json.load(f)
    
    return render_template("summary.html", summary=summary_data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)