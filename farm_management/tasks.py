from flask import Blueprint, render_template, request, redirect, url_for

tasks_bp = Blueprint('tasks', __name__, url_prefix='/farm')

@tasks_bp.route('/tasks')
def list_tasks():
    # TODO: Implement database logic to fetch all tasks.
    all_tasks = []
    return render_template('tasks/index.html', tasks=all_tasks)

@tasks_bp.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    # TODO: Fetch all lands and workers for the dropdown menus in the form.
    all_lands = []
    all_workers = []
    if request.method == 'POST':
        # TODO: Implement database logic to add a new task.
        pass
        return redirect(url_for('tasks.list_tasks'))
    return render_template('tasks/form.html', form_action='add', task=None, lands=all_lands, workers=all_workers)

@tasks_bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
def edit_task(id):
    # TODO: Fetch the specific task by its id.
    task_to_edit = None
    # TODO: Fetch all lands and workers for the dropdown menus.
    all_lands = []
    all_workers = []
    if request.method == 'POST':
        # TODO: Implement database logic to update the task.
        pass
        return redirect(url_for('tasks.list_tasks'))
    return render_template('tasks/form.html', form_action='edit', task=task_to_edit, lands=all_lands, workers=all_workers)

@tasks_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    # TODO: Implement database logic to delete the task.
    pass
    return redirect(url_for('tasks.list_tasks'))
