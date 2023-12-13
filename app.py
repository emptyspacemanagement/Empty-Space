from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class FindSpace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pallet_quantity = db.Column(db.Integer)
    postcode = db.Column(db.String(10))
    max_radius = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    company_name = db.Column(db.String(50))

class OfferSpace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pallet_space_available = db.Column(db.Integer)
    warehouse_address = db.Column(db.String(100))
    start_date_available = db.Column(db.Date)
    end_date_available = db.Column(db.Date)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    company_name = db.Column(db.String(50))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_warehouse_space', methods=['GET', 'POST'])
def find_warehouse_space():
    if request.method == 'POST':
        with app.app_context():
            find_data = {
                'pallet_quantity': int(request.form['pallet_quantity']),
                'postcode': request.form['postcode'],
                'max_radius': int(request.form['max_radius']),
                'start_date': datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
                'end_date': datetime.strptime(request.form['end_date'], '%Y-%m-%d').date(),
                'name': request.form['name'],
                'email': request.form['email'],
                'company_name': request.form['company_name']
            }
            find_space = FindSpace(**find_data)
            db.session.add(find_space)
            db.session.commit()
            flash('Thank you, you have successfully submitted a request', 'success')
            return redirect(url_for('index'))
    return render_template('find_warehouse_space.html')

@app.route('/offer_warehouse_space', methods=['GET', 'POST'])
def offer_warehouse_space():
    if request.method == 'POST':
        with app.app_context():
            offer_data = {
                'pallet_space_available': int(request.form['pallet_space_available']),
                'warehouse_address': request.form['warehouse_address'],
                'start_date_available': datetime.strptime(request.form['start_date_available'], '%Y-%m-%d').date(),
                'end_date_available': datetime.strptime(request.form['end_date_available'], '%Y-%m-%d').date(),
                'name': request.form['name'],
                'email': request.form['email'],
                'company_name': request.form['company_name']
            }
            offer_space = OfferSpace(**offer_data)
            db.session.add(offer_space)
            db.session.commit()
            flash('Thank you, you have successfully submitted a request', 'success')
            return redirect(url_for('index'))
    return render_template('offer_warehouse_space.html')

@app.route('/database')
def database():
    find_spaces = FindSpace.query.all()
    offer_spaces = OfferSpace.query.all()
    return render_template('database.html', find_spaces=find_spaces, offer_spaces=offer_spaces)

@app.route('/delete_find_space/<int:id>')
def delete_find_space(id):
    find_space = FindSpace.query.get(id)
    if find_space:
        db.session.delete(find_space)
        db.session.commit()
        flash('Entry deleted successfully', 'success')
    else:
        abort(404)  # Entry not found
    return redirect(url_for('database'))

@app.route('/delete_offer_space/<int:id>')
def delete_offer_space(id):
    offer_space = OfferSpace.query.get(id)
    if offer_space:
        db.session.delete(offer_space)
        db.session.commit()
        flash('Entry deleted successfully', 'success')
    else:
        abort(404)  # Entry not found
    return redirect(url_for('database'))

if __name__ == '__main__':
    app.run(debug=True)