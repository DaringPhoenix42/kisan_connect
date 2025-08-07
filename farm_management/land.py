from flask import Blueprint, render_template, request, redirect, url_for

land_bp = Blueprint('land', __name__, url_prefix='/farm')

@land_bp.route('/land')
def list_fields():
    # TODO: Implement database logic to fetch all fields.
    all_lands = []
    return render_template('land/index.html', lands=all_lands)

@land_bp.route('/land/add', methods=['GET', 'POST'])
def add_field():
    if request.method == 'POST':
        # TODO: Implement database logic to add a new field.
        pass
        return redirect(url_for('land.list_fields'))
    return render_template('land/form.html', form_action='add', land=None)

@land_bp.route('/land/<int:id>/edit', methods=['GET', 'POST'])
def edit_field(id):
    # TODO: Fetch the specific field by its id.
    field_to_edit = None 
    if request.method == 'POST':
        # TODO: Implement database logic to update the field.
        pass
        return redirect(url_for('land.list_fields'))
    return render_template('land/form.html', form_action='edit', land=field_to_edit)

@land_bp.route('/land/<int:id>/delete', methods=['POST'])
def delete_field(id):
    # TODO: Implement database logic to delete the field.
    pass
    return redirect(url_for('land.list_fields'))