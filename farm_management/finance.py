from flask import Blueprint, render_template, request, redirect, url_for

finance_bp = Blueprint('finance', __name__, url_prefix='/farm')

@finance_bp.route('/finance')
def list_transactions():
    # TODO: Implement database logic to fetch all transactions.
    all_transactions = []
    # TODO: Calculate summary data (total income, total expense, profit).
    summary = {'income': 0, 'expense': 0, 'profit': 0}
    return render_template('finance/index.html', transactions=all_transactions, summary=summary)

@finance_bp.route('/finance/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        # TODO: Implement database logic to add a new transaction.
        pass
        return redirect(url_for('finance.list_transactions'))
    return render_template('finance/form.html', form_action='add', transaction=None)

@finance_bp.route('/finance/<int:id>/edit', methods=['GET', 'POST'])
def edit_transaction(id):
    # TODO: Fetch the specific transaction by its id.
    transaction_to_edit = None
    if request.method == 'POST':
        # TODO: Implement database logic to update the transaction.
        pass
        return redirect(url_for('finance.list_transactions'))
    return render_template('finance/form.html', form_action='edit', transaction=transaction_to_edit)

@finance_bp.route('/finance/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    # TODO: Implement database logic to delete the transaction.
    pass
    return redirect(url_for('finance.list_transactions'))
