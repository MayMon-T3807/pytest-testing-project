import pytest

from src.data_validator import (
    ValidationError,
    InvalidEmailError,
    WeakPasswordError,
    InvalidAgeError,
    InvalidUsernameError,
    validate_email,
    validate_password,
    validate_username,
    validate_age,
    validate_registration,
)


# =====================================================
# Custom exceptions
# =====================================================

@pytest.mark.parametrize("error_class", [
    InvalidEmailError,
    WeakPasswordError,
    InvalidAgeError,
    InvalidUsernameError,
])
def test_custom_errors_are_validation_errors(error_class):
    assert issubclass(error_class, ValidationError)


def test_validation_error_is_an_exception():
    assert issubclass(ValidationError, Exception)


# =====================================================
# validate_email
# =====================================================

@pytest.mark.parametrize("email", [
    "user@example.com",             # standard
    "first.last@example.com",       # dot in the name
    "user_name@example.com",        # underscore
    "user-name@example.com",        # hyphen
    "user+tag@example.com",         # plus addressing
    "user123@example123.com",       # digits
    "USER@EXAMPLE.COM",             # capital letters
    "user@mail.example.com",        # subdomain
    "user@sub.domain.co.uk",        # many parts
    "user@my-domain.com",           # hyphen in domain
    "a@b.co",                       # shortest possible
])
def test_email_valid(email):
    assert validate_email(email) is True


def test_email_surrounding_spaces_are_trimmed():
    # the function strips spaces at the start and end before checking
    assert validate_email("  user@example.com  ") is True


@pytest.mark.parametrize("email", ["", "   "])
def test_email_empty_raises_error(email):
    with pytest.raises(InvalidEmailError, match="empty"):
        validate_email(email)


@pytest.mark.parametrize("email", [
    "userexample.com",          # missing @
    "user@",                    # missing domain
    "@example.com",             # missing name
    "user@example",             # missing .com part
    "user@example.c",           # extension too short
    "user@example.123",         # extension is not letters
    "user@.com",                # domain is empty
    "user@@example.com",        # two @ signs
    "user..name@example.com",   # two dots in a row
    "user@example..com",        # two dots in the domain
    "user name@example.com",    # space in the name
    "user@exam ple.com",        # space in the domain
    "user!@example.com",        # bad symbol
    "user@exa_mple.com",        # underscore in the domain
])
def test_email_invalid_format_raises_error(email):
    with pytest.raises(InvalidEmailError, match="not a valid email"):
        validate_email(email)


@pytest.mark.parametrize("email", [None, 123, 1.5, ["user@example.com"], True])
def test_email_not_a_string_raises_type_error(email):
    with pytest.raises(TypeError, match="string"):
        validate_email(email)


# =====================================================
# validate_password
# =====================================================

@pytest.mark.parametrize("password", [
    "Str0ng!Pass",          # normal strong password
    "Abcdef1!",             # exactly 8 characters
    "Aa1!" + "x" * 124,     # exactly 128 characters
    "My$ecret99",
])
def test_password_valid(password):
    assert validate_password(password) is True


@pytest.mark.parametrize("special", list("!@#$%^&*()_+-=[]{}|;:,.<>?"))
def test_password_accepts_every_special_character(special):
    assert validate_password("Abcdefg1" + special) is True


def test_password_too_short_raises_error():
    with pytest.raises(WeakPasswordError, match="at least 8"):
        validate_password("Abcde1!")        # 7 characters


def test_password_empty_raises_error():
    with pytest.raises(WeakPasswordError, match="at least 8"):
        validate_password("")


def test_password_too_long_raises_error():
    with pytest.raises(WeakPasswordError, match="128"):
        validate_password("Aa1!" + "x" * 125)   # 129 characters


@pytest.mark.parametrize("password", ["Abcd 1!x", "Abcd\t1!xy", "Abcdef1!\n"])
def test_password_with_whitespace_raises_error(password):
    with pytest.raises(WeakPasswordError, match="whitespace"):
        validate_password(password)


def test_password_without_uppercase_raises_error():
    with pytest.raises(WeakPasswordError, match="uppercase"):
        validate_password("lowercase1!")


def test_password_without_lowercase_raises_error():
    with pytest.raises(WeakPasswordError, match="lowercase"):
        validate_password("UPPERCASE1!")


def test_password_without_digit_raises_error():
    with pytest.raises(WeakPasswordError, match="digit"):
        validate_password("NoDigits!!")


@pytest.mark.parametrize("password", ["Password123", "Abcdefg1~", "Abcdefg1'"])
def test_password_without_special_character_raises_error(password):
    with pytest.raises(WeakPasswordError, match="special"):
        validate_password(password)


@pytest.mark.parametrize("password", [None, 12345678, 1.5, ["Abcdef1!"], True])
def test_password_not_a_string_raises_type_error(password):
    with pytest.raises(TypeError, match="string"):
        validate_password(password)


# =====================================================
# validate_username
# =====================================================

@pytest.mark.parametrize("username", [
    "abc",                  # exactly 3 characters
    "a" + "b" * 19,         # exactly 20 characters
    "alice",
    "Alice_01",             # capital, underscore and digits
    "user123",
    "a_b",
    "ABC",
])
def test_username_valid(username):
    assert validate_username(username) is True


@pytest.mark.parametrize("username", [
    "",
    "a",
    "ab",                   # one too short
    "a" * 21,               # one too long
    "a" * 50,
])
def test_username_wrong_length_raises_error(username):
    with pytest.raises(InvalidUsernameError, match="between 3 and 20"):
        validate_username(username)


@pytest.mark.parametrize("username", [
    "1abc",                 # starts with a digit
    "_abc",                 # starts with an underscore
    " abc",                 # starts with a space
    "ab cd",                # space inside
    "user!",                # special character
    "user-name",            # hyphen
    "user@name",
    "user.name",
])
def test_username_bad_format_raises_error(username):
    with pytest.raises(InvalidUsernameError, match="start with a letter"):
        validate_username(username)


@pytest.mark.parametrize("username", [None, 123, 1.5, ["alice"], True])
def test_username_not_a_string_raises_type_error(username):
    with pytest.raises(TypeError, match="string"):
        validate_username(username)


# =====================================================
# validate_age
# =====================================================

@pytest.mark.parametrize("age", [13, 14, 25, 119, 120])
def test_age_valid(age):
    assert validate_age(age) is True


@pytest.mark.parametrize("age", [12, 1, 0, -1, -50])
def test_age_too_young_raises_error(age):
    with pytest.raises(InvalidAgeError, match="at least 13"):
        validate_age(age)


@pytest.mark.parametrize("age", [121, 150, 1000])
def test_age_too_old_raises_error(age):
    with pytest.raises(InvalidAgeError, match="exceed 120"):
        validate_age(age)


@pytest.mark.parametrize("age", [25.5, 13.0, "25", None, True, False, [25]])
def test_age_not_an_integer_raises_type_error(age):
    with pytest.raises(TypeError, match="integer"):
        validate_age(age)


# =====================================================
# validate_registration
# =====================================================

def test_registration_valid(valid_registration_data):
    assert validate_registration(valid_registration_data) is True


def test_registration_extra_fields_are_allowed(valid_registration_data):
    valid_registration_data["nickname"] = "Ali"
    assert validate_registration(valid_registration_data) is True


@pytest.mark.parametrize("missing_field", ["username", "email", "password", "age"])
def test_registration_missing_field_raises_error(valid_registration_data, missing_field):
    del valid_registration_data[missing_field]
    with pytest.raises(ValidationError, match="Missing required") as error:
        validate_registration(valid_registration_data)
    assert missing_field in str(error.value)


def test_registration_empty_dictionary_raises_error():
    with pytest.raises(ValidationError, match="Missing required"):
        validate_registration({})


@pytest.mark.parametrize("field, bad_value, expected_error", [
    ("username", "ab", InvalidUsernameError),
    ("username", "1alice", InvalidUsernameError),
    ("email", "not-an-email", InvalidEmailError),
    ("email", "user@example", InvalidEmailError),
    ("password", "weak", WeakPasswordError),
    ("password", "NoSpecial123", WeakPasswordError),
    ("age", 12, InvalidAgeError),
    ("age", 121, InvalidAgeError),
])
def test_registration_bad_field_raises_matching_error(
    valid_registration_data, field, bad_value, expected_error
):
    valid_registration_data[field] = bad_value
    with pytest.raises(expected_error):
        validate_registration(valid_registration_data)


@pytest.mark.parametrize("field, bad_value", [
    ("username", 123),
    ("email", 123),
    ("password", 123),
    ("age", "25"),
])
def test_registration_wrong_field_type_raises_type_error(
    valid_registration_data, field, bad_value
):
    valid_registration_data[field] = bad_value
    with pytest.raises(TypeError):
        validate_registration(valid_registration_data)


def test_registration_checks_username_first(valid_registration_data):
    valid_registration_data["username"] = "ab"
    valid_registration_data["email"] = "not-an-email"
    with pytest.raises(InvalidUsernameError):
        validate_registration(valid_registration_data)


@pytest.mark.parametrize("data", [None, [], "username", 123, ("username", "email")])
def test_registration_not_a_dictionary_raises_type_error(data):
    with pytest.raises(TypeError, match="dictionary"):
        validate_registration(data)