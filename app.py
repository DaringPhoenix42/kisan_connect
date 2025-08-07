from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json
import os
from datetime import datetime, date
import requests
from werkzeug.utils import secure_filename

# Use your config.py and ai_integration.py
from ai_integration import KisanMitraAI
from config import get_api_key

app = Flask(__name__)
app.secret_key = 'kisan_mitra_secret_key_2025'

# --- 1. DATABASE SETUP ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farm_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- 2. DATABASE MODELS ---
class Land(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    area = db.Column(db.Float, nullable=False)
    soil_type = db.Column(db.String(100))
    irrigation_type = db.Column(db.String(100))
    status = db.Column(db.String(50), default='Fallow')

class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), unique=True)
    daily_wage = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.Text)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    field_id = db.Column(db.Integer, db.ForeignKey('land.id'), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=True)
    field = db.relationship('Land', backref=db.backref('tasks', lazy=True))
    worker = db.relationship('Worker', backref=db.backref('tasks', lazy=True))

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    stock = db.Column(db.Float, nullable=False, default=0)
    unit = db.Column(db.String(20))
    alert_threshold = db.Column(db.Float)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'Income' or 'Expense'
    date = db.Column(db.Date, nullable=False, default=date.today)

class Produce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmer_name = db.Column(db.String(150))
    location = db.Column(db.String(100), nullable=False)
    crop_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    expected_price = db.Column(db.Integer, nullable=False) # Price per quintal
    harvest_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    date_listed = db.Column(db.DateTime, default=datetime.utcnow)


# --- 3. BLUEPRINT DEFINITIONS ---
land_bp = Blueprint('land', __name__, url_prefix='/farm')
labor_bp = Blueprint('labor', __name__, url_prefix='/farm')
tasks_bp = Blueprint('tasks', __name__, url_prefix='/farm')
inventory_bp = Blueprint('inventory', __name__, url_prefix='/farm')
finance_bp = Blueprint('finance', __name__, url_prefix='/farm')
mandi_bp = Blueprint('mandi', __name__, url_prefix='/mandi')


# --- Farm Management Routes (FULLY IMPLEMENTED) ---
@land_bp.route('/land')
def list_fields():
    all_lands = Land.query.order_by(Land.name).all()
    return render_template('land/index.html', lands=all_lands)

@land_bp.route('/land/add', methods=['GET', 'POST'])
def add_field():
    if request.method == 'POST':
        try:
            new_field = Land(
                name=request.form.get('name'), area=float(request.form.get('area')),
                soil_type=request.form.get('soil_type'), irrigation_type=request.form.get('irrigation_type'),
                status=request.form.get('status')
            )
            db.session.add(new_field)
            db.session.commit()
            flash('Field added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding field: {e}', 'danger')
        return redirect(url_for('land.list_fields'))
    return render_template('land/form.html', form_action='add', land=None)

@land_bp.route('/land/<int:id>/edit', methods=['GET', 'POST'])
def edit_field(id):
    field_to_edit = Land.query.get_or_404(id)
    if request.method == 'POST':
        try:
            field_to_edit.name = request.form.get('name')
            field_to_edit.area = float(request.form.get('area'))
            field_to_edit.soil_type = request.form.get('soil_type')
            field_to_edit.irrigation_type = request.form.get('irrigation_type')
            field_to_edit.status = request.form.get('status')
            db.session.commit()
            flash('Field updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating field: {e}', 'danger')
        return redirect(url_for('land.list_fields'))
    return render_template('land/form.html', form_action='edit', land=field_to_edit)

@land_bp.route('/land/<int:id>/delete', methods=['POST'])
def delete_field(id):
    field_to_delete = Land.query.get_or_404(id)
    try:
        db.session.delete(field_to_delete)
        db.session.commit()
        flash('Field deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting field: {e}', 'danger')
    return redirect(url_for('land.list_fields'))

@labor_bp.route('/workers')
def list_workers():
    all_workers = Worker.query.order_by(Worker.full_name).all()
    return render_template('labor/index.html', workers=all_workers)

@labor_bp.route('/workers/add', methods=['GET', 'POST'])
def add_worker():
    if request.method == 'POST':
        try:
            new_worker = Worker(
                full_name=request.form.get('full_name'), phone=request.form.get('phone'),
                daily_wage=int(request.form.get('daily_wage')), skills=request.form.get('skills')
            )
            db.session.add(new_worker)
            db.session.commit()
            flash('Worker added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding worker: {e}', 'danger')
        return redirect(url_for('labor.list_workers'))
    return render_template('labor/form.html', form_action='add', worker=None)

@labor_bp.route('/workers/<int:id>/edit', methods=['GET', 'POST'])
def edit_worker(id):
    worker_to_edit = Worker.query.get_or_404(id)
    if request.method == 'POST':
        try:
            worker_to_edit.full_name = request.form.get('full_name')
            worker_to_edit.phone = request.form.get('phone')
            worker_to_edit.daily_wage = int(request.form.get('daily_wage'))
            worker_to_edit.skills = request.form.get('skills')
            db.session.commit()
            flash('Worker updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating worker: {e}', 'danger')
        return redirect(url_for('labor.list_workers'))
    return render_template('labor/form.html', form_action='edit', worker=worker_to_edit)

@labor_bp.route('/workers/<int:id>/delete', methods=['POST'])
def delete_worker(id):
    worker_to_delete = Worker.query.get_or_404(id)
    try:
        db.session.delete(worker_to_delete)
        db.session.commit()
        flash('Worker deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting worker: {e}', 'danger')
    return redirect(url_for('labor.list_workers'))

@tasks_bp.route('/tasks')
def list_tasks():
    all_tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template('tasks/index.html', tasks=all_tasks)

@tasks_bp.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        try:
            worker_id = request.form.get('worker_id')
            new_task = Task(
                name=request.form.get('name'), description=request.form.get('description'),
                priority=request.form.get('priority'), status=request.form.get('status'),
                field_id=int(request.form.get('field_id')), worker_id=int(worker_id) if worker_id else None
            )
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding task: {e}', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    all_lands = Land.query.order_by(Land.name).all()
    all_workers = Worker.query.order_by(Worker.full_name).all()
    return render_template('tasks/form.html', form_action='add', task=None, lands=all_lands, workers=all_workers)

@tasks_bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
def edit_task(id):
    task_to_edit = Task.query.get_or_404(id)
    if request.method == 'POST':
        try:
            worker_id = request.form.get('worker_id')
            task_to_edit.name = request.form.get('name')
            task_to_edit.description = request.form.get('description')
            task_to_edit.priority = request.form.get('priority')
            task_to_edit.status = request.form.get('status')
            task_to_edit.field_id = int(request.form.get('field_id'))
            task_to_edit.worker_id = int(worker_id) if worker_id else None
            db.session.commit()
            flash('Task updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating task: {e}', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    all_lands = Land.query.order_by(Land.name).all()
    all_workers = Worker.query.order_by(Worker.full_name).all()
    return render_template('tasks/form.html', form_action='edit', task=task_to_edit, lands=all_lands, workers=all_workers)

@tasks_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting task: {e}', 'danger')
    return redirect(url_for('tasks.list_tasks'))

@inventory_bp.route('/inventory')
def list_items():
    all_items = InventoryItem.query.order_by(InventoryItem.name).all()
    return render_template('inventory/index.html', items=all_items)

@inventory_bp.route('/inventory/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        try:
            new_item = InventoryItem(
                name=request.form.get('name'), category=request.form.get('category'),
                stock=float(request.form.get('stock')), unit=request.form.get('unit'),
                alert_threshold=float(request.form.get('alert_threshold'))
            )
            db.session.add(new_item)
            db.session.commit()
            flash('Inventory item added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding item: {e}', 'danger')
        return redirect(url_for('inventory.list_items'))
    return render_template('inventory/form.html', form_action='add', item=None)

@inventory_bp.route('/inventory/<int:id>/edit', methods=['GET', 'POST'])
def edit_item(id):
    item_to_edit = InventoryItem.query.get_or_404(id)
    if request.method == 'POST':
        try:
            item_to_edit.name = request.form.get('name')
            item_to_edit.category = request.form.get('category')
            item_to_edit.stock = float(request.form.get('stock'))
            item_to_edit.unit = request.form.get('unit')
            item_to_edit.alert_threshold = float(request.form.get('alert_threshold'))
            db.session.commit()
            flash('Item updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating item: {e}', 'danger')
        return redirect(url_for('inventory.list_items'))
    return render_template('inventory/form.html', form_action='edit', item=item_to_edit)

@inventory_bp.route('/inventory/<int:id>/delete', methods=['POST'])
def delete_item(id):
    item_to_delete = InventoryItem.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        flash('Item deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting item: {e}', 'danger')
    return redirect(url_for('inventory.list_items'))

@finance_bp.route('/finance')
def list_transactions():
    all_transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.type == 'Income').scalar() or 0.0
    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.type == 'Expense').scalar() or 0.0
    summary = {
        'income': total_income, 'expense': total_expense,
        'profit': total_income - total_expense
    }
    return render_template('finance/index.html', transactions=all_transactions, summary=summary)

@finance_bp.route('/finance/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        try:
            date_str = request.form.get('date')
            trans_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            new_transaction = Transaction(
                description=request.form.get('description'), category=request.form.get('category'),
                amount=float(request.form.get('amount')), type=request.form.get('type'),
                date=trans_date
            )
            db.session.add(new_transaction)
            db.session.commit()
            flash('Transaction added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding transaction: {e}', 'danger')
        return redirect(url_for('finance.list_transactions'))
    return render_template('finance/form.html', form_action='add', transaction=None)

@finance_bp.route('/finance/<int:id>/edit', methods=['GET', 'POST'])
def edit_transaction(id):
    transaction_to_edit = Transaction.query.get_or_404(id)
    if request.method == 'POST':
        try:
            date_str = request.form.get('date')
            trans_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            transaction_to_edit.description = request.form.get('description')
            transaction_to_edit.category = request.form.get('category')
            transaction_to_edit.amount = float(request.form.get('amount'))
            transaction_to_edit.type = request.form.get('type')
            transaction_to_edit.date = trans_date
            db.session.commit()
            flash('Transaction updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating transaction: {e}', 'danger')
        return redirect(url_for('finance.list_transactions'))
    return render_template('finance/form.html', form_action='edit', transaction=transaction_to_edit)

@finance_bp.route('/finance/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    transaction_to_delete = Transaction.query.get_or_404(id)
    try:
        db.session.delete(transaction_to_delete)
        db.session.commit()
        flash('Transaction deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting transaction: {e}', 'danger')
    return redirect(url_for('finance.list_transactions'))

@mandi_bp.route('/')
def market():
    listings = Produce.query.order_by(Produce.date_listed.desc()).all()
    with app.test_request_context():
        market_prices_data = market_prices().get_json()
    return render_template(
        'mandi_connect/market.html', 
        listings=listings, 
        market_prices=market_prices_data
    )

@mandi_bp.route('/sell', methods=['GET', 'POST'])
def sell_produce():
    if request.method == 'POST':
        try:
            harvest_date_str = request.form.get('harvestDate')
            harvest_date_obj = datetime.strptime(harvest_date_str, '%Y-%m-%d').date()
            new_listing = Produce(
                farmer_name=request.form.get('farmer_name', "Anonymous Farmer"), location=request.form.get('location'),
                crop_type=request.form.get('cropType'), quantity=float(request.form.get('quantity')),
                expected_price=int(request.form.get('price')), harvest_date=harvest_date_obj,
                description=request.form.get('description')
            )
            db.session.add(new_listing)
            db.session.commit()
            flash('Your produce has been listed successfully!', 'success')
            return redirect(url_for('mandi.market'))
        except Exception as e:
            db.session.rollback()
            flash(f'There was an error listing your produce: {e}', 'danger')
    return render_template('mandi_connect/sell_form.html')

@mandi_bp.route('/search', methods=['POST'])
def search_produce():
    try:
        data = request.get_json()
        query = Produce.query
        if data.get('crop') and data.get('crop').strip():
            query = query.filter(Produce.crop_type.ilike(f"%{data['crop'].strip()}%"))
        if data.get('location') and data.get('location').strip():
            query = query.filter(Produce.location.ilike(f"%{data['location'].strip()}%"))
        if data.get('price') and data.get('price').strip():
            query = query.filter(Produce.expected_price <= int(data['price']))
        results = query.order_by(Produce.date_listed.desc()).all()
        results_list = [
            {"farmer_name": r.farmer_name, "location": r.location, "crop_type": r.crop_type, "quantity": r.quantity,
             "expected_price": r.expected_price, "harvest_date": r.harvest_date.strftime('%d %b %Y'), "description": r.description}
            for r in results
        ]
        return jsonify(success=True, listings=results_list)
    except Exception as e:
        print(f"❌ Error during search: {e}")
        return jsonify(success=False, error=str(e))

@mandi_bp.route('/listing/<int:id>/delete', methods=['POST'])
def delete_listing(id):
    listing_to_delete = Produce.query.get_or_404(id)
    try:
        db.session.delete(listing_to_delete)
        db.session.commit()
        flash('Listing removed successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error removing listing: {e}', 'danger')
    return redirect(url_for('mandi.market'))


# --- 4. REGISTER BLUEPRINTS ---
app.register_blueprint(land_bp)
app.register_blueprint(labor_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(finance_bp)
app.register_blueprint(mandi_bp)


# =====================================================================
# --- AI SYSTEM INITIALIZATION & HELPERS ---
# =====================================================================
ai_system = None
try:
    api_key = get_api_key()
    if api_key:
        ai_system = KisanMitraAI(api_key=api_key)
    else:
        print("⚠️ Gemini API key not found. AI features will use mock data.")
except Exception as e:
    print(f"❌ Error initializing KisanMitraAI class: {e}")

def _get_news_data():
    if not ai_system or not ai_system.model:
        return {"error": "AI system not available", "articles": []}
    try:
        return ai_system.get_agricultural_news(generation_config={"temperature": 0.8})
    except Exception as e:
        print(f"❌ Error fetching AI news: {e}")
        return {"error": str(e), "articles": []}

def _get_schemes_data():
    if not ai_system or not ai_system.model:
        return {"error": "AI system not available", "schemes": []}
    try:
        return ai_system.get_government_schemes(generation_config={"temperature": 0.3})
    except Exception as e:
        print(f"❌ Error fetching AI schemes: {e}")
        return {"error": str(e), "schemes": []}

def _get_weather_data(location='Kalyan'):
    if not ai_system or not ai_system.model:
        return {"location": location, "current": {"temperature_celsius": "N/A"}, "forecast": [], "agricultural_impact": "Weather data unavailable."}
    try:
        return ai_system.get_weather_analysis(location=location, generation_config={"temperature": 0.2})
    except Exception as e:
        print(f"❌ Error fetching AI weather: {e}")
        return {"error": str(e)}


# --- OTHER CONFIG AND MOCK DATA ---
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CROP_DATA = {'soybean': {'name': 'Soybean', 'msp': 4800}, 'cotton': {'name': 'Cotton', 'msp': 7100}, 'moong': {'name': 'Moong', 'msp': 8600}}
MARKET_DATA = {'nashik': {'soybean': 5200, 'cotton': 7500, 'moong': 9000}}


# =====================================================================
# --- MAIN PAGE ROUTES ---
# =====================================================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/farm-management')
def farm_management():
    total_land = db.session.query(db.func.sum(Land.area)).scalar() or 0
    field_count = Land.query.count()
    active_crops = Land.query.filter(Land.status.in_(['Planted', 'Growing'])).count()
    worker_count = Worker.query.count()
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.type == 'Income').scalar() or 0
    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.type == 'Expense').scalar() or 0
    net_profit = (total_income or 0) - (total_expense or 0)
    recent_tasks = Task.query.order_by(Task.id.desc()).limit(5).all()
    stats = {
        'total_land': total_land, 'field_count': field_count,
        'active_crops': active_crops, 'worker_count': worker_count,
        'monthly_profit': net_profit, 'recent_tasks': recent_tasks
    }
    return render_template('farm_management.html', stats=stats, today=date.today())

@app.route('/fasal-salah')
def fasal_salah():
    return render_template('fasal_salah.html')

@app.route('/mandi-connect')
def mandi_connect():
    return redirect(url_for('mandi.market'))
# In app.py, replace the gyan_kendra page route

@app.route('/gyan-kendra')
def gyan_kendra():
    """Pre-fetches data for all Gyan Kendra tabs."""
    news_data = _get_news_data()
    schemes_data = _get_schemes_data()
    weather_data = _get_weather_data()
    
    return render_template(
        'gyan_kendra.html',
        news_articles=news_data.get('articles', []),
        schemes=schemes_data.get('schemes', []),
        weather=weather_data
    )

@app.route('/paudha-rakshak')
def paudha_rakshak():
    return render_template('paudha_rakshak.html')

@app.route('/resource-optimizer')
def resource_optimizer():
    return render_template('resource_optimizer.html')


# =====================================================================
# --- ALL ORIGINAL API ROUTES ---
# =====================================================================
@app.route('/api/crop-recommendation', methods=['POST'])
def crop_recommendation():
    if not ai_system or not ai_system.model:
        print("-> AI not available, using MOCK data for crop recommendation.")
        data = request.get_json()
        location = data.get('location', 'Kalyan')
        soil_type = data.get('soil_type', 'Black Soil')
        budget = data.get('budget', 50000)
        recommendations = []
        if "Black Soil" in soil_type and budget > 40000:
            recommendations.append({'crop': 'cotton', 'confidence': 88, 'reason': 'Ideal for black soil...', 'data': CROP_DATA.get('cotton', {})})
            recommendations.append({'crop': 'soybean', 'confidence': 75, 'reason': 'Good alternative...', 'data': CROP_DATA.get('soybean', {})})
        elif "Red Soil" in soil_type:
            recommendations.append({'crop': 'moong', 'confidence': 92, 'reason': 'Excellent for red soil...', 'data': CROP_DATA.get('moong', {})})
        else:
            recommendations.append({'crop': 'soybean', 'confidence': 70, 'reason': 'A generally safe choice.', 'data': CROP_DATA.get('soybean', {})})
        return jsonify({'location': location, 'recommendations': recommendations, 'market_data': MARKET_DATA.get('nashik', {}), 'ai_used': False})
    try:
        data = request.get_json()
        ai_response = ai_system.get_crop_recommendation(
            location=data.get('location'), soil_type=data.get('soil_type'),
            irrigation=data.get('irrigation'), land_area=data.get('land_area'),
            season=data.get('season'), budget=data.get('budget'),
            generation_config={"temperature": 0.7}
        )
        return jsonify(ai_response)
    except Exception as e:
        print(f"❌ Error in /api/crop-recommendation: {e}")
        return jsonify({"error": "Failed to get AI recommendation."}), 500

@app.route('/api/disease-detection', methods=['POST'])
def disease_detection():
    if not ai_system or not ai_system.model:
        return jsonify({"error": "AI system not available."}), 503
    if 'image' not in request.files:
        return jsonify({'error': 'No image file found'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        file.save(filepath)
        ai_response = ai_system.analyze_plant_disease(filepath, generation_config={"temperature": 0.4})
        return jsonify(ai_response)
    except Exception as e:
        print(f"❌ Error in /api/disease-detection: {e}")
        return jsonify({"error": "Failed to analyze image with AI."}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
    return jsonify({"error": "An unknown error occurred."}), 500

@app.route('/api/market-prices')
def market_prices():
    location = request.args.get('location', 'Nashik')
    print("📊 Using mock data for market prices")
    return jsonify({
        'location': location, 'current_prices': MARKET_DATA.get(location.lower(), {}),
        'market_trend': 'Prices are stable', 'price_forecast': 'Expected 5-10% increase',
        'demand_analysis': 'High demand for pulses', 'ai_used': False
    })

@app.route('/api/irrigation-calculator', methods=['POST'])
def irrigation_calculator():
    if not ai_system or not ai_system.model:
        return jsonify({"error": "AI system not available"}), 503
    try:
        data = request.get_json()
        ai_response = ai_system.get_irrigation_advice(
            crop=data.get('crop_type'), soil_type=data.get('soil_type'),
            land_area=data.get('land_area'), weather=data.get('weather'),
            growth_stage=data.get('growth_stage'), generation_config={"temperature": 0.3}
        )
        return jsonify(ai_response)
    except Exception as e:
        print(f"❌ Error in /api/irrigation-calculator: {e}")
        return jsonify({"error": "Failed to get AI irrigation advice."}), 500

@app.route('/api/fertilizer-recommendation', methods=['POST'])
def fertilizer_recommendation():
    if not ai_system or not ai_system.model:
        return jsonify({"error": "AI system not available"}), 503
    try:
        data = request.get_json()
        ai_response = ai_system.get_fertilizer_advice(
            crop=data.get('crop_type'), soil_type=data.get('soil_type'),
            growth_stage=data.get('growth_stage'), generation_config={"temperature": 0.5}
        )
        return jsonify(ai_response)
    except Exception as e:
        print(f"❌ Error in /api/fertilizer-recommendation: {e}")
        return jsonify({"error": "Failed to get AI fertilizer advice."}), 500

@app.route('/api/soil-health-analysis', methods=['POST'])
def soil_health_analysis():
    if not ai_system or not ai_system.model:
        return jsonify({"error": "AI system not available"}), 503
    try:
        data = request.get_json()
        ai_response = ai_system.get_soil_health_analysis(
            soil_type=data.get('soil_type'), ph=data.get('ph_level'),
            organic_matter=data.get('organic_matter'), nitrogen=data.get('nitrogen'),
            phosphorus=data.get('phosphorus'), potassium=data.get('potassium'),
            generation_config={"temperature": 0.5}
        )
        return jsonify(ai_response)
    except Exception as e:
        print(f"❌ Error in /api/soil-health-analysis: {e}")
        return jsonify({"error": "Failed to get AI soil analysis."}), 500

@app.route('/api/crop-yield-prediction', methods=['POST'])
def crop_yield_prediction():
    # ... (This still uses mock data, can be upgraded later)
    data = request.get_json()
    crop = data.get('crop')
    land_area = data.get('land_area', 1)
    soil_type = data.get('soil_type', 'Black Soil')
    print("📊 Using DYNAMIC mock data for yield prediction")
    base_yields = {'soybean': 12, 'cotton': 8, 'moong': 6}
    base_yield = base_yields.get(crop.lower(), 10)
    if "Black Soil" in soil_type:
        base_yield *= 1.1
    total_yield = round(base_yield * land_area, 2)
    expected_revenue = int(total_yield * (CROP_DATA.get(crop.lower(), {}).get('msp', 5000)))
    return jsonify({
        'expected_yield_per_acre': f"{round(base_yield, 2)} quintals", 'total_expected_yield': f"{total_yield} quintals",
        'confidence_level': 'Medium', 'expected_revenue': f"₹{expected_revenue:,}",
        'market_price_assumption': f"Based on MSP of ₹{CROP_DATA.get(crop.lower(), {}).get('msp', 5000)}/quintal",
        'ai_used': False
    })

@app.route('/api/farming-calculator', methods=['POST'])
def farming_calculator():
    # ... (This still uses mock data)
    data = request.get_json()
    land_area = data.get('land_area', 1)
    expected_yield = data.get('expected_yield', 10)
    total_cost = 15000 * land_area
    revenue = int(expected_yield) * 5000
    profit = revenue - total_cost
    print("📊 Using mock data for farming calculator")
    return jsonify({'total_cost': f"₹{total_cost:,}", 'expected_revenue': f"₹{revenue:,}", 'net_profit': f"₹{profit:,}", 'ai_used': False})

@app.route('/api/farm-analytics', methods=['POST'])
def farm_analytics():
    # ... (This still uses mock data)
    print("📊 Using mock data for farm analytics")
    return jsonify({
        'performance_insights': ['Soybean yield expected to increase by 15%'],
        'recommendations': ['Apply organic fertilizer to improve soil health'],
        'ai_used': False
    })

@app.route('/api/task-optimization', methods=['POST'])
def task_optimization():
    # ... (This still uses mock data)
    print("📊 Using mock data for task optimization")
    return jsonify({
        'optimized_schedule': [{'task': 'Irrigation', 'worker': 'Ramesh Kumar', 'field': 'Field 1'}],
        'efficiency_improvements': ['Group similar tasks'],
        'ai_used': False
    })
    
# In app.py, add/replace these API routes

@app.route('/api/agricultural-news', methods=['GET'])
def agricultural_news():
    if not ai_system or not ai_system.model:
        return jsonify({"error": "AI system not available"}), 503
    try:
        ai_response = ai_system.get_agricultural_news(generation_config={"temperature": 0.8})
        return jsonify(ai_response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/weather-analysis', methods=['GET'])
def weather_analysis():
    location = request.args.get('location', 'Kalyan')
    if not ai_system or not ai_system.model:
        return jsonify({"error": "AI system not available"}), 503
    try:
        ai_response = ai_system.get_weather_analysis(location=location, generation_config={"temperature": 0.2})
        return jsonify(ai_response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# This is a new route to add
@app.route('/api/government-schemes', methods=['GET'])
def government_schemes():
    if not ai_system or not ai_system.model:
        return jsonify({"error": "AI system not available"}), 503
    try:
        ai_response = ai_system.get_government_schemes(generation_config={"temperature": 0.3})
        return jsonify(ai_response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
    app.run(debug=True, host='0.0.0.0', port=5000)