import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product

app = Flask(__name__)
app.secret_key = "devops_secret_key"

# PostgreSQL Connection String (Docker Compose variables se connect hoga)
DB_USERNAME = os.environ.get('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')
DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DB_NAME = os.environ.get('POSTGRES_DB', 'flask_db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Database create karne ke liye route (DevOps setup ke baad chalane ke liye)
@app.before_request
def create_tables():
    db.create_all()

# 1. Home Page - Product Catalog
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# 2. Admin Page - Add/Manage Products
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        category = request.form['category']
        
        if not name or not price:
            flash("Name and Price are required!", "danger")
            return redirect(url_for('admin'))
            
        new_product = Product(name=name, price=float(price), description=description, category=category)
        db.session.add(new_product)
        db.session.commit()
        flash("Product Added Successfully!", "success")
        return redirect(url_for('index'))
        
    products = Product.query.all()
    return render_template('admin.html', products=products)

# Delete Product Action
@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product Deleted!", "warning")
    return redirect(url_for('admin'))

# 3. About / System Info Page
@app.route('/about')
def about():
    # DevOps context ke liye system environment variables show kar rahe hain
    env_info = {
        "Database Host": DB_HOST,
        "Database Name": DB_NAME,
        "App Environment": os.environ.get('FLASK_ENV', 'Development')
    }
    return render_template('about.html', env_info=env_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)