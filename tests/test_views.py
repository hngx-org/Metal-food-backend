import requests
import pytest

# important!: include the base url before running test 
base_url = ""

# Define access token for authentication
access_token = "auth-token"

# function to make authenticated requests
def make_authenticated_request(method, url, data=None):
    """
    Make an authenticated HTTP request to the API.

    Args:
        method (str): The HTTP method (e.g., 'GET', 'POST', 'PUT').
        url (str): The URL of the API endpoint.
        data (dict): Optional request data in JSON format.

    Returns:
        requests.Response: The HTTP response object.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.request(method, url, headers=headers, json=data)
    return response


# Authentication Tests
def test_login():
    """
    Test user login functionality.

    Sends a POST request to the login endpoint with user credentials and checks the response.
    """
    url = f"{base_url}/auth/login"
    data = {"email": "user@example.com", "password": "password123"}
    response = make_authenticated_request("POST", url, data)
    assert response.status_code == 200
    assert response.json()["message"] == "User authenticated successfully"
    assert "access_token" in response.json()["data"]
    assert "email" in response.json()["data"]
    assert "id" in response.json()["data"]
    assert "isAdmin" in response.json()["data"]


def test_user_signup():
    """
    Test user signup functionality.

    Sends a POST request to the user signup endpoint with user data and checks the response.
    """
    url = f"{base_url}/auth/user/signup"
    data = {
        "email": "user@example.com",
        "password": "password123",
        "first_name": "",
        "last_name": "",
        "phone_number": "",
    }
    response = make_authenticated_request("POST", url, data)
    assert response.status_code == 200
    assert response.json()["message"] == "User signed up successfully"
    assert "access_token" in response.json()["data"]
    assert "email" in response.json()["data"]
    assert "id" in response.json()["data"]
    assert "isAdmin" in response.json()["data"]


# Organization Tests
def test_create_organization():
    """
    Test organization creation functionality.

    Sends a POST request to create an organization and checks the response.
    """
    url = f"{base_url}/organization/create"
    data = {"organization_name": "", "lunch_price": "#1000"}
    response = make_authenticated_request("POST", url, data)
    assert response.status_code == 200
    assert response.json()["message"] == "Organization created successfully"
    assert "organization_id" in response.json()["data"]


def test_staff_signup():
    """
    Test staff signup functionality.

    Sends a POST request to the staff signup endpoint with staff data and checks the response.
    """
    url = f"{base_url}/organization/staff/signup"
    data = {
        "email": "user@example.com",
        "password": "password123",
        "otp_token": "",  # Replace with the actual OTP token
        "first_name": "",
        "last_name": "",
        "phone_number": "",
    }
    response = make_authenticated_request("POST", url, data)
    assert response.status_code == 200
    assert response.json()["message"] == "Staff signed up successfully"
    assert "staff_id" in response.json()["data"]


def test_create_organization_invite():
    """
    Test organization invitation functionality.

    Sends a POST request to invite a user to an organization and checks the response.
    """
    url = f"{base_url}/organization/invite"
    data = {"email": "jane@example.com"}
    response = make_authenticated_request("POST", url, data)
    assert response.status_code == 200
    assert response.json()["message"] == "Invitation sent successfully"


# User Section Tests
def test_get_user_profile():
    """
    Test fetching user profile functionality.

    Sends a GET request to retrieve user profile data and checks the response.
    """
    url = f"{base_url}/user/profile"
    response = make_authenticated_request("GET", url)
    assert response.status_code == 200
    assert response.json()["message"] == "User data fetched successfully"
    assert "name" in response.json()["data"]
    assert "email" in response.json()["data"]
    assert "profile_picture" in response.json()["data"]
    assert "phonenumber" in response.json()["data"]
    assert "bank_number" in response.json()["data"]
    assert "bank_code" in response.json()["data"]
    assert "bank_name" in response.json()["data"]
    assert "isAdmin" in response.json()["data"]


def test_add_bank_account():
    """
    Test adding bank account functionality.

    Sends a POST request to add a bank account and checks the response.
    """
    url = f"{base_url}/user/bank"
    data = {
        "bank_number": "1234-5678-9012-3456",
        "bank_code": "123456",
        "bank_name": "Bank Name",
    }
    response = make_authenticated_request("POST", url, data)
    assert response.status_code == 200
    assert response.json()["message"] == "Bank account created successfully"


def test_get_all_users():
    """
    Test fetching all users functionality.

    Sends a GET request to retrieve all user data and checks the response.
    """
    url = f"{base_url}/users"
    response = make_authenticated_request("GET", url)
    assert response.status_code == 200
    assert response.json()["message"] == "Users fetched successfully"
    assert "data" in response.json()


def test_search_users():
    """
    Test searching for users functionality.

    Sends a GET request to search for a user by name or email and checks the response.
    """
    search_term = "JohnDoe"
    url = f"{base_url}/search/{search_term}"
    response = make_authenticated_request("GET", url)
    assert response.status_code == 200
    assert response.json()["message"] == "User found"
    assert "data" in response.json()


# Lunch Section Tests
def test_send_lunch_request():
    """
    Test sending a lunch request functionality.

    Sends a POST request to send a lunch request and checks the response.
    """
    url = f"{base_url}/lunch/send"
    data = {
        "receivers": ["user_id"],
        "quantity": 5,
        "note": "Special instructions for the lunch",
    }
    response = make_authenticated_request("POST", url, data)
    assert response.status_code == 201
    assert response.json()["message"] == "Lunch request created successfully"


def test_get_lunch_request():
    """
    Test fetching a lunch request functionality.

    Sends a GET request to retrieve a specific lunch request and checks the response.
    """
    lunch_id = "unique-lunch-id"
    url = f"{base_url}/lunch/{lunch_id}"
    response = make_authenticated_request("GET", url)
    assert response.status_code == 200
    assert response.json()["message"] == "Lunch request fetched successfully"
    assert "data" in response.json()


def test_get_all_lunches():
    """
    Test fetching all lunch requests functionality.

    Sends a GET request to retrieve all lunch requests and checks the response.
    """
    url = f"{base_url}/lunch/all"
    response = make_authenticated_request("GET", url)
    assert response.status_code == 200
    assert response.json()["message"] == "All lunches fetched successfully"
    assert "data" in response.json()


def test_redeem_lunch_request():
    """
    Test redeeming a lunch request functionality.

    Sends a PUT request to redeem a specific lunch request and checks the response.
    """
    lunch_id = "unique-lunch-id"
    url = f"{base_url}/lunch/redeem/{lunch_id}"
    response = make_authenticated_request("PUT", url)
    assert response.status_code == 200
    assert response.json()["message"] == "Lunch redeemed successfully"


# Withdrawal Request Tests
def test_create_withdrawal_request():
    """
    Test creating a withdrawal request functionality.

    Sends a POST request to create a withdrawal request and checks the response.
    """
    url = f"{base_url}/withdrawal/request"
    data = {
        "bank_name": "Bank",
        "bank_number": "1234-5678-9012-3456",
        "bank_code": "123456",
        "amount": 100,
    }
    response = make_authenticated_request("POST", url, data)
    assert response.status_code == 201
    assert response.json()["message"] == "Withdrawal request created successfully"
    assert "withdrawal_id" in response.json()["data"]


if __name__ == "__main__":
    pytest.main()

