import pytest
from datetime import date
from database.crud.user_crud import UserCrud
from database.models.user_model import User


class TestUserCrud:
    """Test UserCrud database crud operations."""
    
    def test_create_user(self, db_session):
        """Test creating a new user in the database."""
        crud = UserCrud(db_session)
        
        user = crud.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            birthdate=date(2000, 1, 1)
        )
        
        assert user is not None
        assert user.id is not None  
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password != "password123"
        assert user.birthdate == date(2000, 1, 1)
        
        #assert hta password is hashed with bcrypt
        assert user.password.startswith("$2b$") or user.password.startswith("$2a$")
    
    def test_get_user_by_id(self, test_user, user_crud):
        """Test gettiug a user by ID from database."""
        user_id = test_user.id
        
        get_user = user_crud.get_user_by_id(user_id)
        
        assert get_user is not None
        assert get_user.id == user_id
        assert get_user.username == "bob"
        assert get_user.email == "bob@example.com"
    
    def test_get_user_by_id_nonexistent(self, user_crud):
        """Test getting a non-existent user by ID."""
        user = user_crud.get_user_by_id(12312)
        assert user is None
    
    def test_get_user_by_email(self, test_user, user_crud):
        """Test getting a user by email from database."""
        user = user_crud.get_user_by_email("bob@example.com")

        assert user is not None
        assert user.email == "bob@example.com"
        assert user.username == "bob"
        assert user.id == test_user.id
    
    def test_get_user_by_email_nonexistent(self, user_crud):
        """Test getting a user by non-existent email."""
        user = user_crud.get_user_by_email("alice@example.com")
        
        assert user is None
    
    def test_get_user_by_username(self, test_user, user_crud):
        """Test gettng a user by username from database."""
        user = user_crud.get_user_by_username("bob")
        

        assert user is not None
        assert user.username == "bob"
        assert user.email == "bob@example.com"
        assert user.id == test_user.id
    
    def test_get_all_users(self, test_user, user_crud):
        """Test getting all users from database."""
        user_crud.create_user("fishstick", "fishstick@example.com", "wowowow", date(2001, 10, 1))
        user_crud.create_user("meatball", "meatball@example.com", "123456", date(2002, 11, 1))
        user_crud.create_user("corndog", "corndog@example.com", "tungtungtung", date(2003, 12, 1))
    
        all_users = user_crud.get_all_users()

        assert all_users is not None
        assert len(all_users) == 4

        usernames = [user.username for user in all_users]
        assert "bob" in usernames
        assert "fishstick" in usernames
        assert "meatball" in usernames
        assert "corndog" in usernames
    
    def test_authenticate_user_correct_password(self, test_user, user_crud):
        """Test user authentication with correct password."""
        authenticated_user = user_crud.authenticate_user("bob@example.com", "bob123")
        
        assert authenticated_user is not None
        assert authenticated_user.id == test_user.id
        assert authenticated_user.username == "bob"
        assert authenticated_user.email == "bob@example.com"
    
    def test_authenticate_user_incorrect_password(self, test_user, user_crud):
        """Test user authentication with incorrect password."""
        not_authenticated_user = user_crud.authenticate_user("bob@example.com", "alksdjasd")
        
        assert not_authenticated_user is None
    
    def test_authenticate_user_nonexistent_email(self, user_crud):
        """Test authenticating a nonexistent user."""
        user_not_found = user_crud.authenticate_user("fireball@example.com", "fireinthehole")
        
        assert user_not_found is None
    
    def test_delete_user(self, test_user, user_crud):
        """Test deleting a user from the database."""
        user_id = test_user.id
        
        deleted_user = user_crud.delete_user(user_id)
        
        assert deleted_user is True
        
        get_user = user_crud.get_user_by_id(user_id)
        assert get_user is None
    
    def test_delete_user_nonexistent(self, user_crud):
        """Test deleting a non-existent user from the database."""
        deleted_user = user_crud.delete_user(99999)
        
        assert deleted_user is False
    
    def test_hash_password(self, user_crud):
        """Test password hashing produces different hashes for same password with bcrypt."""
        password = "test_password"
        
        hash1 = user_crud.hash_password(password)
        hash2 = user_crud.hash_password(password)
        
        assert hash1 != hash2
        
        assert user_crud.verify_password(password, hash1) is True
        assert user_crud.verify_password(password, hash2) is True
    
    def test_verify_password(self, user_crud):
        """Test password verification works correctly with bcrypt."""
        password = "test_password"
        hashed = user_crud.hash_password(password)
        
        assert user_crud.verify_password(password, hashed) is True
        
        assert user_crud.verify_password("wrong_password", hashed) is False
    


