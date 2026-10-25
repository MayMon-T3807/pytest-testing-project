import pytest

from src.student_manager import Student, StudentManager


@pytest.fixture
def empty_manager():
    # a brand new manager with no students
    return StudentManager()


@pytest.fixture
def sample_student():
    # one valid student with no grades yet
    return Student(student_id="S001", name="Alice Smith", email="alice@example.com")


@pytest.fixture
def populated_manager():
    # a manager with 5 students, each with a different GPA
    manager = StudentManager()

    alice = manager.add_student("S001", "Alice", "alice@example.com")
    alice.add_grade("MATH101", 95)
    alice.add_grade("CS101", 92)      # GPA 4.0

    bob = manager.add_student("S002", "Bob", "bob@example.com")
    bob.add_grade("MATH101", 85)
    bob.add_grade("CS101", 82)        # GPA 3.0

    carol = manager.add_student("S003", "Carol", "carol@example.com")
    carol.add_grade("MATH101", 75)    # GPA 2.0

    dave = manager.add_student("S004", "Dave", "dave@example.com")
    dave.add_grade("MATH101", 65)     # GPA 1.0

    eve = manager.add_student("S005", "Eve", "eve@example.com")
    eve.add_grade("MATH101", 40)      # GPA 0.0

    return manager


@pytest.fixture
def valid_registration_data():
    # a registration form that should pass every rule
    return {
        "username": "alice_01",
        "email": "alice@example.com",
        "password": "Str0ng!Pass",
        "age": 25,
    }