import pytest
from fastapi import status

# ============================================
# FIXTURE : Todo de test
# ============================================

@pytest.fixture
def test_todo(client, auth_headers):
    response = client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "Test Description",
            "priority": 1
        },
        headers=auth_headers
    )
    return response.json()


# ============================================
# TESTS CREATE TODO
# ============================================

def test_create_todo_authenticated(client, auth_headers):
    response = client.post(
        "/todos/",
        json={
            "title": "New Todo",
            "description": "Description",
            "priority": 2
        },
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["title"] == "New Todo"
    assert data["description"] == "Description"
    assert data["done"] == False
    assert data["priority"] == 2
    assert "id" in data
    assert "user_id" in data


def test_create_todo_unauthenticated(client):
    response = client.post(
        "/todos/",
        json={
            "title": "New Todo",
            "description": "Description"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_todo_missing_title(client, auth_headers):
    response = client.post(
        "/todos/",
        json={
            "description": "Description"
        },
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ============================================
# TESTS GET TODOS
# ============================================

def test_get_todos_empty(client, auth_headers):
    response = client.get("/todos/", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_todos_with_data(client, auth_headers, test_todo):
    response = client.get("/todos/", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Todo"


def test_get_todos_only_own(client, auth_headers, test_todo):
    # Créer un deuxième utilisateur
    client.post(
        "/auth/register",
        json={
            "username": "otheruser",
            "email": "other@example.com",
            "password": "password123"
        }
    )
    
    # Login avec le deuxième utilisateur
    login_response = client.post(
        "/auth/login",
        data={
            "username": "otheruser",
            "password": "password123"
        }
    )
    
    other_token = login_response.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}
    
    # Le deuxième utilisateur ne doit pas voir les todos du premier
    response = client.get("/todos/", headers=other_headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []  # Liste vide


# ============================================
# TESTS GET TODO BY ID
# ============================================

def test_get_todo_by_id_success(client, auth_headers, test_todo):
    todo_id = test_todo["id"]
    
    response = client.get(f"/todos/{todo_id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == todo_id


def test_get_todo_nonexistent(client, auth_headers):
    response = client.get("/todos/999", headers=auth_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ============================================
# TESTS UPDATE TODO
# ============================================

def test_update_todo_success(client, auth_headers, test_todo):
    todo_id = test_todo["id"]
    
    response = client.put(
        f"/todos/{todo_id}",
        json={
            "title": "Updated Title",
            "done": True
        },
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["done"] == True


# ============================================
# TESTS DELETE TODO
# ============================================

def test_delete_todo_success(client, auth_headers, test_todo):
    todo_id = test_todo["id"]
    
    response = client.delete(f"/todos/{todo_id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Vérifier que le todo n'existe plus
    get_response = client.get(f"/todos/{todo_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_todo_nonexistent(client, auth_headers):
    response = client.delete("/todos/999", headers=auth_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND