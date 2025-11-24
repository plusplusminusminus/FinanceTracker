"""Testing the Authentication class"""

import pytest
from unittest.mock import Mock
from datetime import date
from app.authentication import Authentication

class TestAuthentication:
    """Test Authentication functions and logic."""
    
    def test_login_success(self, mock_db, mock_user, mock_user_crud):
        """Test successful login with valid enail and password."""
        mock_user_crud.authenticate_user.return_value = mock_user
        
        auth = Authentication(mock_db)
        auth._user_crud = mock_user_crud
        
        valid_login, user, message = auth.login("bob@example.com", "12345")
        
        assert valid_login is True
        assert user == mock_user
        assert "Login successful" in message
        # make sure authentication was caleld only once when user is logging in
        mock_user_crud.authenticate_user.assert_called_once_with("bob@example.com", "12345")
    
    def test_login_invalid_credentials(self, mock_db, mock_user_crud):
        """Test login with invalid email and password."""
        mock_user_crud.authenticate_user.return_value = None
        
        auth = Authentication(mock_db)
        auth._user_crud = mock_user_crud
        
        valid_login, user, message = auth.login("bob@example.com", "54321")
        
        assert valid_login is False
        assert user is None
        assert "Invalid login credentials" in message
    
    def test_login_missing_email(self, mock_db):
        """Test login validation wiht missing email."""
        auth = Authentication(mock_db)

        valid_login, user, message = auth.login("", "12345")
        
        assert valid_login is False
        assert user is None
        assert "Email and password are required" in message
    
    def test_login_missing_password(self, mock_db):
        """Test login validation with missing password."""
        auth = Authentication(mock_db)

        valid_login, user, message = auth.login("bob@example.com", "")
        
        assert valid_login is False
        assert user is None
        assert "Email and password are required" in message
    
    
    def test_register_success(self, mock_db, mock_user, mock_user_crud):
        """Test successful user registration."""
        mock_user_crud.get_user_by_email.return_value = None
        mock_user_crud.create_user.return_value = mock_user
        
        auth = Authentication(mock_db)
        auth._user_crud = mock_user_crud
        

        valid_registration, message = auth.register(username="newuser",email="new@example.com",password="12345",birthdate=date(2003, 5, 1)
        )

        assert valid_registration is True
        assert "User created sucessfully" in message
        mock_user_crud.get_user_by_email.assert_called_once_with("new@example.com")
        mock_user_crud.create_user.assert_called_once_with("newuser", "new@example.com", "12345", date(2003, 5, 1))
    
    def test_register_short_password(self, mock_db):
        """Test registration with short password"""
        auth = Authentication(mock_db)

        valid_registration, message = auth.register(
            username="testuser",
            email="test@example.com",
            password="1234"
        )

        assert valid_registration is False
        assert "Password have to be longer than 5 characters" in message
    
    
    def test_register_email_already_exists(self, mock_db, mock_user_crud):
        """Test registration with email that already exists."""
        existing_user = Mock()
        mock_user_crud.get_user_by_email.return_value = existing_user
        
        auth = Authentication(mock_db)
        auth._user_crud = mock_user_crud
        
        valid_registration, message = auth.register(username="bob",email="bob@example.com",password="12345")
        assert valid_registration is False
        assert "Email already exists" in message
        mock_user_crud.get_user_by_email.assert_called_once_with("bob@example.com")
        mock_user_crud.create_user.assert_not_called()
    
    def test_register_missing_username(self, mock_db):
        """Test registration with missing username."""
        auth = Authentication(mock_db)
        
        valid_registration, message = auth.register("", "test@example.com", "12345")
        
        assert valid_registration is False
        assert "Username, email, and password are required" in message
    
    def test_register_missing_email(self, mock_db):
        """Test registration with missing email."""
        auth = Authentication(mock_db)
        
        valid_registration, message = auth.register("testuser", "", "12345")
        
        assert valid_registration is False
        assert "Username, email, and password are required" in message
    
    def test_register_missing_password(self, mock_db):
        """Test registration with missing password."""
        auth = Authentication(mock_db)
        
        valid_registration, message = auth.register("testuser", "test@example.com", "")
        
        assert valid_registration is False
        assert "Username, email, and password are required" in message
    
    def test_logout(self, mock_db):
        """Test logout to see success."""
        auth = Authentication(mock_db)
        
        valid_logout, message = auth.logout()
        
        assert valid_logout is True
        assert "Logout successful" in message

