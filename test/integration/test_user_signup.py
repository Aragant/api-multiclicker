import pytest
from domain.user.use_cases.signup import signup
from domain.user.user_schema import UserSignUp
from infrastructure.error.error import DuplicateEntryError
from domain.user.user_repository import UserRepository

@pytest.mark.asyncio
async def test_signup_success(transaction):
    # Arrange
    user_data = UserSignUp(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!"
    )
    
    # Act
    result = await signup(user_data)
    
    # Assert
    assert result.username == user_data.username
    assert result.email == user_data.email
    assert result.id is not None
    assert result.disabled is False

@pytest.mark.asyncio
async def test_signup_duplicate_email(transaction):
    # Arrange
    user_data = UserSignUp(
        username="testuser1",
        email="duplicate@example.com",
        password="TestPassword123!"
    )
    
    # Create first user
    await signup(user_data)
    
    # Try to create second user with same email
    duplicate_user = UserSignUp(
        username="testuser2",
        email="duplicate@example.com",
        password="TestPassword123!"
    )
    
    # Act & Assert
    with pytest.raises(DuplicateEntryError):
        await signup(duplicate_user)

@pytest.mark.asyncio
async def test_signup_sso_constraints(transaction):
    # Arrange
    user_data = UserSignUp(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!"
    )
    
    # Act & Assert
    with pytest.raises(ValueError, match="A password should not be provided for SSO registers"):
        await signup(user_data, provider="google")
    
    # Test without password for non-SSO
    user_data_no_password = UserSignUp(
        username="testuser",
        email="test@example.com",
        password=None
    )
    
    with pytest.raises(ValueError, match="A password should be provided for non SSO registers"):
        await signup(user_data_no_password) 