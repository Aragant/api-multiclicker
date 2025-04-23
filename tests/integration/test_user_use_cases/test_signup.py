from pydantic_core import ValidationError
import pytest

from domain.user.use_cases.signup import signup
from domain.user.user_schema import UserSignUp
from infrastructure.error.error import DuplicateEntryError, UnprocessableEntityError


@pytest.mark.asyncio
async def test_signup_when_duplicate_email_should_raise_DuplicateEntryError():
    user_data = UserSignUp(
        username="testuser1",
        email="duplicate@example.com",
        password="TestPassword123!"
    )

    await signup(user_data)

    duplicate_user = UserSignUp(
        username="testuser2",
        email="duplicate@example.com",
        password="TestPassword123!"
    )

    with pytest.raises(DuplicateEntryError):
        await signup(duplicate_user)

@pytest.mark.asyncio
async def test_signup_when_duplicate_username_should_raise_DuplicateEntryError():
    user_data = UserSignUp(
        username="testuser",
        email="example@example.fr",
        password="TestPassword123!"
    )

    await signup(user_data)

    duplicate_user = UserSignUp(
        username="testuser",
        email="duplicate@example.fr",
        password="TestPassword123!"
    )

    with pytest.raises(DuplicateEntryError):
        await signup(duplicate_user)
        

# test when email not provided
@pytest.mark.asyncio
async def test_signup_when_email_not_provided_should_raise_UnprocessableEntity():
    with pytest.raises(ValidationError) as exc_info:
        UserSignUp(
            username="testuser",
            password="TestPassword123!"
        )

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("email",)

@pytest.mark.asyncio
async def test_signup_when_username_not_provided_should_raise_UnprocessableEntity():
    with pytest.raises(ValidationError) as exc_info:
        UserSignUp(
            email="example@example.fr",
            password="TestPassword123!"
        )

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("username",)
    

@pytest.mark.asyncio
async def test_signup_when_password_not_provided_should_raise_UnprocessableEntity():
    with pytest.raises(ValidationError) as exc_info:
        UserSignUp(
            email="example@example.fr",
            username="testuser"
        )

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("password",)
    

@pytest.mark.asyncio
async def test_signup_when_password_has_not_at_least_8_characters_should_raise_UnprocessableEntity():
    user_data = UserSignUp(
        email="example@example.fr",
        username="testuser",
        password="short"
    )
    
    with pytest.raises(UnprocessableEntityError):
        await signup(user_data)
        
@pytest.mark.asyncio
async def test_signup_when_password_has_not_at_least_1_uppercase_should_raise_UnprocessableEntity():
    user_data = UserSignUp(
        email="example@example.fr",
        username="testuser",
        password="shortazazeaz"
    )
    
    with pytest.raises(UnprocessableEntityError):
        await signup(user_data)
        

@pytest.mark.asyncio
async def test_signup_when_password_has_not_at_least_1_lowercase_should_raise_UnprocessableEntity():
    user_data = UserSignUp(
        email="example@example.fr",
        username="testuser",
        password="SHORTAZAZEAZ"
    )
    
    with pytest.raises(UnprocessableEntityError):
        await signup(user_data)
        

@pytest.mark.asyncio
async def test_signup_when_password_has_not_at_least_1_digit_should_raise_UnprocessableEntity():
    user_data = UserSignUp(
        email="example@example.fr",
        username="testuser",
        password="shortAZAZEAZ"
    )
    
    with pytest.raises(UnprocessableEntityError):
        await signup(user_data)
        

@pytest.mark.asyncio
async def test_signup_when_success_should_return_user():
    user_data = UserSignUp(
        email="example@example.fr",
        username="testuser",
        password="TestPassword123"
    )
    
    user = await signup(user_data)
    
    assert user.username == user_data.username
    assert user.email == user_data.email
    
