import pytest
from jose import jwt, JWTError
from app import schemas
from app.config import settings


# def test_root(client):
#     response = client.get("/")
#     print(response.json().get("message"))
#     assert response.status_code == 200
#     assert response.json().get("message") == "Hello World"


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "abc@gmail.com", "password": "123"})
    print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "abc@gmail.com"


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    # print(res.json())

    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token,
                         settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert res.status_code == 200
    assert test_user['id'] == payload.get('user_id')    # Validating the token
    assert res.json().get("token_type") == 'bearer'


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('abc@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('abc@gmail.com', None, 422),
])
def test_incorrect_login(email, password, status_code, test_user, client):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
