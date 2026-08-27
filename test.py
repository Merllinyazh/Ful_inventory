from fastapi.testclient import TestClient
import uuid
from app import app

client = TestClient(app)


# ==========================================
# TEST DATA
# ==========================================

admin_user = {
    "username": "testadmin",
    "email": "testadmin@example.com",
    "password": "123456",
    "role": "admin"
}

staff_user = {
    "username": "teststaff",
    "email": "teststaff@example.com",
    "password": "123456",
    "role": "staff"
}


# ==========================================
# HOME
# ==========================================

def test_home():

    response = client.get("/")

    assert response.status_code == 200


# ==========================================
# AUTHENTICATION
# ==========================================

def test_register_admin():

    response = client.post(
        "/auth/register",
        json=admin_user
    )

    # 201 if new user, 409 if already exists
    assert response.status_code in [201, 409]


def test_register_staff():

    response = client.post(
        "/auth/register",
        json=staff_user
    )

    assert response.status_code in [201, 409]


def test_login_admin():

    response = client.post(
        "/auth/login",
        json={
            "email": admin_user["email"],
            "password": admin_user["password"]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "Bearer"


def test_login_staff():

    response = client.post(
        "/auth/login",
        json={
            "email": staff_user["email"],
            "password": staff_user["password"]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data


def get_admin_headers():

    response = client.post(
        "/auth/login",
        json={
            "email": admin_user["email"],
            "password": admin_user["password"]
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def get_staff_headers():

    response = client.post(
        "/auth/login",
        json={
            "email": staff_user["email"],
            "password": staff_user["password"]
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_protected_route():

    headers = get_admin_headers()

    response = client.get(
        "/auth/protected",
        headers=headers
    )

    assert response.status_code == 200


# ==========================================
# PRODUCT MANAGEMENT
# ==========================================

def test_create_product():

    headers = get_admin_headers()

    product = {
        "name": "Test Laptop",
        "sku": "TEST-LAPTOP-001",
        "price": 50000,
        "quantity": 0
    }

    response = client.post(
        "/products/",
        json=product,
        headers=headers
    )

    assert response.status_code in [201, 409]


def test_get_products():

    headers = get_staff_headers()

    response = client.get(
        "/products/",
        headers=headers
    )

    assert response.status_code == 200


def test_get_single_product():

    headers = get_staff_headers()

    response = client.get(
        "/products/1",
        headers=headers
    )

    assert response.status_code in [200, 404]


def test_update_product():

    headers = get_admin_headers()

    # Create a unique product first
    sku = f"TEST-{uuid.uuid4().hex[:8]}"

    create_response = client.post(
        "/products/",
        json={
            "name": "Test Laptop",
            "sku": sku,
            "price": 50000,
            "quantity": 0
        },
        headers=headers
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["product"]["id"]

    # Update that exact product
    updated_sku = f"UPDATED-{uuid.uuid4().hex[:8]}"

    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Updated Test Laptop",
            "sku": updated_sku,
            "price": 55000,
            "quantity": 0
        },
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["product"]["sku"] == updated_sku


def test_delete_product():

    headers = get_admin_headers()

    response = client.delete(
        "/products/9999",
        headers=headers
    )

    # Product may not exist
    assert response.status_code == 404


# ==========================================
# LOCATION MANAGEMENT
# ==========================================

def test_create_location():

    headers = get_admin_headers()

    location = {
        "name": "Test Warehouse",
        "address": "Test Address"
    }

    response = client.post(
        "/locations/",
        json=location,
        headers=headers
    )

    assert response.status_code in [201, 409]


def test_get_locations():

    headers = get_staff_headers()

    response = client.get(
        "/locations/",
        headers=headers
    )

    assert response.status_code == 200


def test_get_single_location():

    headers = get_staff_headers()

    response = client.get(
        "/locations/1",
        headers=headers
    )

    assert response.status_code in [200, 404]


def test_update_location():

    headers = get_admin_headers()

    location = {
        "name": "Updated Warehouse",
        "address": "Updated Address"
    }

    response = client.put(
        "/locations/1",
        json=location,
        headers=headers
    )

    assert response.status_code in [200, 404]


def test_delete_location():

    headers = get_admin_headers()

    response = client.delete(
        "/locations/9999",
        headers=headers
    )

    assert response.status_code == 404


# ==========================================
# STOCK MOVEMENT
# ==========================================

def test_stock_in():

    headers = get_admin_headers()

    movement = {
        "product_id": 1,
        "from_location_id": None,
        "to_location_id": 1,
        "quantity": 10,
        "movement_type": "IN"
    }

    response = client.post(
        "/movement/",
        json=movement,
        headers=headers
    )

    assert response.status_code in [200, 404]


def test_stock_out():

    headers = get_admin_headers()

    movement = {
        "product_id": 1,
        "from_location_id": 1,
        "to_location_id": None,
        "quantity": 2,
        "movement_type": "OUT"
    }

    response = client.post(
        "/movement/",
        json=movement,
        headers=headers
    )

    assert response.status_code in [200, 400, 404]


def test_stock_transfer():

    headers = get_admin_headers()

    movement = {
        "product_id": 1,
        "from_location_id": 1,
        "to_location_id": 2,
        "quantity": 2,
        "movement_type": "TRANSFER"
    }

    response = client.post(
        "/movement/",
        json=movement,
        headers=headers
    )

    assert response.status_code in [200, 400, 404]


# ==========================================
# STOCK
# ==========================================

def test_get_all_stock():

    headers = get_staff_headers()

    response = client.get(
        "/stock/",
        headers=headers
    )

    assert response.status_code == 200


def test_get_stock_by_location():

    headers = get_staff_headers()

    response = client.get(
        "/stock/location/1",
        headers=headers
    )

    assert response.status_code in [200, 404]


# ==========================================
# AUDIT LOG
# ==========================================

def test_get_audit_logs():

    headers = get_admin_headers()

    response = client.get(
        "/audit/",
        headers=headers
    )

    assert response.status_code == 200


def test_get_user_audit_logs():

    headers = get_admin_headers()

    response = client.get(
        "/audit/user/1",
        headers=headers
    )

    assert response.status_code in [200, 404]


# ==========================================
# AUTHORIZATION TESTS
# ==========================================

def test_staff_can_get_products():

    headers = get_staff_headers()

    response = client.get(
        "/products/",
        headers=headers
    )

    assert response.status_code == 200


def test_staff_cannot_create_product():

    headers = get_staff_headers()

    product = {
        "name": "Unauthorized Product",
        "sku": "STAFF-TEST-001",
        "price": 1000,
        "quantity": 0
    }

    response = client.post(
        "/products/",
        json=product,
        headers=headers
    )

    assert response.status_code == 403