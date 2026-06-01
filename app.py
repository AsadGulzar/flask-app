import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY',
    'devops_secret_key'
)

DB_USERNAME = os.environ.get('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
DB_HOST = os.environ.get('POSTGRES_HOST', 'db')
DB_NAME = os.environ.get('POSTGRES_DB', 'flask_db')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    products = Product.query.all()
    return render_template(
        'index.html',
        products=products
    )


@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if request.method == 'POST':

        try:
            name = request.form['name']
            price = float(request.form['price'])
            description = request.form['description']
            category = request.form['category']

            new_product = Product(
                name=name,
                price=price,
                description=description,
                category=category
            )

            db.session.add(new_product)
            db.session.commit()

            flash(
                "Product Added Successfully!",
                "success"
            )

        except Exception:
            db.session.rollback()
            flash(
                "Failed to add product.",
                "danger"
            )

        return redirect(url_for('admin'))

    products = Product.query.all()

    return render_template(
        'admin.html',
        products=products
    )


@app.route('/delete/<int:id>')
def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    flash(
        "Product Deleted!",
        "warning"
    )

    return redirect(url_for('admin'))


@app.route('/about')
def about():

    env_info = {
        "Database Host": DB_HOST,
        "Database Name": DB_NAME,
        "App Environment": os.environ.get(
            'FLASK_ENV',
            'Production'
        )
    }

    return render_template(
        'about.html',
        env_info=env_info
    )


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000
    )