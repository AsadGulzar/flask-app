import pytest
from app import app, db
from models import Product

@pytest.fixture
def client():
    # Test environment configuration
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Isolation test database
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

# Test 1: Check if Homepage loads correctly (Status 200)
def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"DevOps Cloud Store" in response.data

# Test 2: Check if About Page loads env-info
def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"DevOps Deployment Metadata" in response.data

# Test 3: Check if Product Injection works via Database Mocking
def test_add_product(client):
    response = client.post('/admin', data=dict(
        name="Test AWS Course",
        price="49.99",
        category="DevOps Tools",
        description="Automated unit testing description"
    ), follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Test AWS Course" in response.data