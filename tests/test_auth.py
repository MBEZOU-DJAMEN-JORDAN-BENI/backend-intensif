import pytest
from fastapi import status

# ===============================
# TESTS REGIDTER
# ==============================

def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
    )
    # Verifer la condition vrai
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "password" not in data
    
    
def test_register_duplicate_username(client, test_user):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser", # deja exixtant
            "email": "other@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already register" in response.json()["detail"].lower()
    
    
def test_register_diplicate_email(client, test_user):
    response = client.post(
        "/auth/register",
        json={
            "username": "otheruser",
            "email": "test@example.com", # deja existant
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already register" in response.json()["detail"].lower()


def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "pas-un-email",
            "password": "password123"
        }
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    

def test_register_short_passowrd(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "12345"
        }
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
   
    
#===================================
# TEST LOGIN
#===================================

def test_login_success(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_nonexistent_user(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": "nonexiststent",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ==================================
# TESTS /ME
# ==================================

def test_get_me_authenticated(client, auth_headers):
    response = client.get(
        "/auth/me",
        headers=auth_headers # Token JWT dans le header
    )
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    

def test_get_me_authenticated(client):
    response = client.get("/auth/me")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    

def test_get_me_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer token-invalide"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED