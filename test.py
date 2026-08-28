from fastapi.testclient import TestClient
import uuid
from app import app

client = TestClient(app)


# ==========================================
# TEST USERS
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
# HELPER FUNCTIONS
# ==========================================

def get_token(user):
    response = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": user["password"]
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def register_test_users():
    client.post("/auth/register", json=admin_user)
    client.post("/auth/register", json=staff_user)


# ==========================================
# HOME
# ==========================================

def test_home():
    response = client.get("/")
    assert response.status_code == 200


# ==========================================
# AUTHENTICATION
# ==========================================

def test_authentication():

    register_test_users()

    response = client.post(
        "/auth/login",
        json={
            "email": admin_user["email"],
            "password": admin_user["password"]
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


# ==========================================
# PRODUCT MANAGEMENT
# ==========================================

def test_product_management():

    register_test_users()
    headers = get_token(admin_user)

    sku = f"TEST-{uuid.uuid4().hex[:8]}"

    # CREATE
    response = client.post(
        "/products/",
        json={
            "name": "Test Laptop",
            "sku": sku,
            "price": 50000,
            "quantity": 0
        },
        headers=headers
    )

    assert response.status_code == 201

    product_id = response.json()["product"]["id"]

    # GET
    response = client.get(
        f"/products/{product_id}",
        headers=headers
    )

    assert response.status_code == 200

    # UPDATE
    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Updated Laptop",
            "sku": f"UPDATED-{uuid.uuid4().hex[:8]}",
            "price": 55000,
            "quantity": 0
        },
        headers=headers
    )

    assert response.status_code == 200


# ==========================================
# LOCATION MANAGEMENT
# ==========================================

def test_location_management():

    register_test_users()
    headers = get_token(admin_user)

    location_name = f"Warehouse-{uuid.uuid4().hex[:6]}"

    # CREATE
    response = client.post(
        "/locations/",
        json={
            "name": location_name,
            "address": "Test Address"
        },
        headers=headers
    )

    assert response.status_code == 201

    location_id = response.json()["location"]["id"]

    # GET
    response = client.get(
        f"/locations/{location_id}",
        headers=headers
    )

    assert response.status_code == 200


# ==========================================
# STOCK MOVEMENT
# ==========================================

def test_stock_movement():

    register_test_users()
    headers = get_token(admin_user)

    # Create product
    response = client.post(
        "/products/",
        json={
            "name": "Movement Product",
            "sku": f"MOVE-{uuid.uuid4().hex[:8]}",
            "price": 1000,
            "quantity": 0
        },
        headers=headers
    )

    assert response.status_code == 201

    product_id = response.json()["product"]["id"]

    # Create location
    response = client.post(
        "/locations/",
        json={
            "name": f"Movement Warehouse-{uuid.uuid4().hex[:6]}",
            "address": "Test Address"
        },
        headers=headers
    )

    assert response.status_code == 201

    location_id = response.json()["location"]["id"]

    # STOCK IN
    response = client.post(
        "/movement/",
        json={
            "product_id": product_id,
            "to_location_id": location_id,
            "quantity": 10,
            "movement_type": "IN"
        },
        headers=headers
    )

    assert response.status_code == 200


# ==========================================
# STOCK + AUDIT
# ==========================================

def test_stock_and_audit():

    register_test_users()

    admin_headers = get_token(admin_user)

    # STOCK
    response = client.get(
        "/stock/",
        headers=admin_headers
    )

    assert response.status_code == 200

    # AUDIT LOG
    response = client.get(
        "/audit/",
        headers=admin_headers
    )

    assert response.status_code == 200


# ==========================================
# AUTHORIZATION
# ==========================================

def test_staff_permissions():

    register_test_users()

    staff_headers = get_token(staff_user)

    # Staff CAN get products
    response = client.get(
        "/products/",
        headers=staff_headers
    )

    assert response.status_code == 200

    # Staff CANNOT create products
    response = client.post(
        "/products/",
        json={
            "name": "Unauthorized Product",
            "sku": f"STAFF-{uuid.uuid4().hex[:8]}",
            "price": 1000,
            "quantity": 0
        },
        headers=staff_headers
    )

    assert response.status_code == 403