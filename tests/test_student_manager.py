import pytest

from src.student_manager import Student, StudentManager


# =====================================================
# Student: creating a student
# =====================================================

def test_student_has_correct_details(sample_student):
    assert sample_student.student_id == "S001"
    assert sample_student.name == "Alice Smith"
    assert sample_student.email == "alice@example.com"


def test_new_student_has_no_grades(sample_student):
    assert sample_student.grades == {}


def test_two_students_do_not_share_grades():
    first = Student("S1", "A", "a@x.com")
    second = Student("S2", "B", "b@x.com")
    first.add_grade("MATH", 90)
    assert second.grades == {}


@pytest.mark.parametrize("student_id", ["", None, 123])
def test_student_bad_id_raises_value_error(student_id):
    with pytest.raises(ValueError, match="student_id"):
        Student(student_id, "Alice", "alice@example.com")


@pytest.mark.parametrize("name", ["", None, 123])
def test_student_bad_name_raises_value_error(name):
    with pytest.raises(ValueError, match="name"):
        Student("S1", name, "alice@example.com")


@pytest.mark.parametrize("email", ["", None, 123, "alice.example.com"])
def test_student_bad_email_raises_value_error(email):
    with pytest.raises(ValueError, match="email"):
        Student("S1", "Alice", email)


# =====================================================
# Student: add_grade
# =====================================================

@pytest.mark.parametrize("score", [0, 50, 99.99, 100])
def test_add_grade_valid_scores(sample_student, score):
    sample_student.add_grade("MATH101", score)
    assert sample_student.grades["MATH101"] == score


def test_add_grade_saves_score_as_float(sample_student):
    sample_student.add_grade("MATH101", 80)
    assert isinstance(sample_student.grades["MATH101"], float)


def test_add_grade_replaces_old_grade_for_same_course(sample_student):
    sample_student.add_grade("MATH101", 60)
    sample_student.add_grade("MATH101", 95)
    assert sample_student.grades == {"MATH101": 95.0}


def test_add_grade_keeps_other_courses(sample_student):
    sample_student.add_grade("MATH101", 60)
    sample_student.add_grade("CS101", 70)
    assert sample_student.grades == {"MATH101": 60.0, "CS101": 70.0}


@pytest.mark.parametrize("score", [-0.01, -1, 100.01, 101])
def test_add_grade_out_of_range_raises_value_error(sample_student, score):
    with pytest.raises(ValueError, match="out of range"):
        sample_student.add_grade("MATH101", score)
    # the bad grade must not be saved
    assert sample_student.grades == {}


@pytest.mark.parametrize("score", ["90", None, True, False])
def test_add_grade_bad_type_raises_type_error(sample_student, score):
    with pytest.raises(TypeError, match="numeric"):
        sample_student.add_grade("MATH101", score)
    assert sample_student.grades == {}


@pytest.mark.parametrize("course", ["", None, 101])
def test_add_grade_bad_course_raises_value_error(sample_student, course):
    with pytest.raises(ValueError, match="course_code"):
        sample_student.add_grade(course, 80)
    assert sample_student.grades == {}


# =====================================================
# Student: get_gpa
# =====================================================

def test_gpa_is_zero_when_no_grades(sample_student):
    assert sample_student.get_gpa() == 0.0


@pytest.mark.parametrize("score, expected_gpa", [
    (100, 4.0),
    (90, 4.0),          # exactly 90 -> 4.0
    (89.99, 3.0),       # just below 90 -> 3.0
    (80, 3.0),          # exactly 80 -> 3.0
    (79.99, 2.0),
    (70, 2.0),
    (69.99, 1.0),
    (60, 1.0),
    (59.99, 0.0),
    (0, 0.0),
])
def test_gpa_for_one_grade(sample_student, score, expected_gpa):
    sample_student.add_grade("MATH101", score)
    assert sample_student.get_gpa() == expected_gpa


def test_gpa_averages_all_courses(sample_student):
    sample_student.add_grade("A", 95)   # 4.0
    sample_student.add_grade("B", 85)   # 3.0
    sample_student.add_grade("C", 75)   # 2.0
    sample_student.add_grade("D", 65)   # 1.0
    sample_student.add_grade("E", 10)   # 0.0
    assert sample_student.get_gpa() == 2.0


def test_gpa_uses_points_not_raw_scores(sample_student):
    sample_student.add_grade("A", 100)  # 4.0
    sample_student.add_grade("B", 60)   # 1.0
    assert sample_student.get_gpa() == 2.5


def test_gpa_rounds_to_2_decimals(sample_student):
    sample_student.add_grade("A", 95)   # 4.0
    sample_student.add_grade("B", 85)   # 3.0
    sample_student.add_grade("C", 85)   # 3.0
    # 10 / 3 = 3.333..., so the answer should be 3.33
    assert sample_student.get_gpa() == 3.33


def test_gpa_changes_after_grade_update(sample_student):
    sample_student.add_grade("A", 50)
    assert sample_student.get_gpa() == 0.0
    sample_student.add_grade("A", 95)
    assert sample_student.get_gpa() == 4.0


# =====================================================
# StudentManager: add_student
# =====================================================

def test_new_manager_is_empty(empty_manager):
    assert empty_manager.get_total_students() == 0
    assert empty_manager.get_all_students() == []


def test_add_student_with_student_object(empty_manager, sample_student):
    result = empty_manager.add_student(sample_student)
    assert result is sample_student
    assert empty_manager.get_student("S001") is sample_student
    assert empty_manager.get_total_students() == 1


def test_add_student_with_separate_details(empty_manager):
    result = empty_manager.add_student("S002", "Bob", "bob@example.com")
    assert isinstance(result, Student)
    assert result.student_id == "S002"
    assert result.name == "Bob"
    assert result.email == "bob@example.com"
    assert empty_manager.get_student("S002") is result


def test_add_duplicate_id_raises_value_error(empty_manager, sample_student):
    empty_manager.add_student(sample_student)
    other = Student("S001", "Someone Else", "else@example.com")
    with pytest.raises(ValueError, match="already exists"):
        empty_manager.add_student(other)


def test_duplicate_id_does_not_overwrite_original(empty_manager, sample_student):
    empty_manager.add_student(sample_student)
    other = Student("S001", "Someone Else", "else@example.com")
    with pytest.raises(ValueError):
        empty_manager.add_student(other)
    # the first student must still be there, unchanged
    assert empty_manager.get_student("S001") is sample_student
    assert empty_manager.get_student("S001").name == "Alice Smith"
    assert empty_manager.get_total_students() == 1


def test_duplicate_id_with_separate_details_raises_value_error(empty_manager):
    empty_manager.add_student("S1", "Alice", "alice@example.com")
    with pytest.raises(ValueError, match="already exists"):
        empty_manager.add_student("S1", "Bob", "bob@example.com")
    assert empty_manager.get_student("S1").name == "Alice"


@pytest.mark.parametrize("name, email", [
    (None, "a@x.com"),
    ("Alice", None),
    (None, None),
])
def test_add_student_missing_name_or_email_raises_value_error(empty_manager, name, email):
    with pytest.raises(ValueError, match="name and email"):
        empty_manager.add_student("S1", name, email)
    assert empty_manager.get_total_students() == 0


@pytest.mark.parametrize("bad_input", [123, None, 1.5, ["S1"]])
def test_add_student_wrong_type_raises_type_error(empty_manager, bad_input):
    with pytest.raises(TypeError):
        empty_manager.add_student(bad_input)
    assert empty_manager.get_total_students() == 0


def test_add_student_with_bad_email_raises_value_error(empty_manager):
    with pytest.raises(ValueError):
        empty_manager.add_student("S1", "Alice", "not-an-email")
    assert empty_manager.get_total_students() == 0


# =====================================================
# StudentManager: get_student
# =====================================================

def test_get_student_found(populated_manager):
    student = populated_manager.get_student("S003")
    assert student.name == "Carol"


@pytest.mark.parametrize("student_id", ["S999", "", "s001"])
def test_get_student_unknown_id_raises_key_error(populated_manager, student_id):
    with pytest.raises(KeyError):
        populated_manager.get_student(student_id)


# =====================================================
# StudentManager: update_grade and calculate_gpa
# =====================================================

def test_update_grade_returns_new_gpa(empty_manager):
    empty_manager.add_student("S1", "Alice", "alice@example.com")
    assert empty_manager.update_grade("S1", "MATH", 95) == 4.0
    assert empty_manager.update_grade("S1", "CS", 65) == 2.5


def test_update_grade_changes_the_student(populated_manager):
    populated_manager.update_grade("S003", "MATH101", 99)
    assert populated_manager.get_student("S003").grades["MATH101"] == 99.0
    assert populated_manager.calculate_gpa("S003") == 4.0


def test_update_grade_unknown_student_raises_key_error(populated_manager):
    with pytest.raises(KeyError):
        populated_manager.update_grade("S999", "MATH101", 80)


def test_update_grade_bad_score_raises_value_error(populated_manager):
    gpa_before = populated_manager.calculate_gpa("S001")
    with pytest.raises(ValueError):
        populated_manager.update_grade("S001", "MATH101", 150)
    # GPA must stay the same after a failed update
    assert populated_manager.calculate_gpa("S001") == gpa_before


def test_update_grade_bad_type_raises_type_error(populated_manager):
    with pytest.raises(TypeError):
        populated_manager.update_grade("S001", "MATH101", "A")


def test_update_grade_bad_course_raises_value_error(populated_manager):
    with pytest.raises(ValueError):
        populated_manager.update_grade("S001", "", 80)


@pytest.mark.parametrize("student_id, expected_gpa", [
    ("S001", 4.0),
    ("S002", 3.0),
    ("S003", 2.0),
    ("S004", 1.0),
    ("S005", 0.0),
])
def test_calculate_gpa(populated_manager, student_id, expected_gpa):
    assert populated_manager.calculate_gpa(student_id) == expected_gpa


def test_calculate_gpa_is_zero_without_grades(empty_manager):
    empty_manager.add_student("S1", "Alice", "alice@example.com")
    assert empty_manager.calculate_gpa("S1") == 0.0


def test_calculate_gpa_unknown_student_raises_key_error(populated_manager):
    with pytest.raises(KeyError):
        populated_manager.calculate_gpa("S999")


# =====================================================
# StudentManager: remove_student
# =====================================================

def test_remove_student_returns_true(populated_manager):
    assert populated_manager.remove_student("S002") is True


def test_remove_student_lowers_the_count(populated_manager):
    assert populated_manager.get_total_students() == 5
    populated_manager.remove_student("S002")
    assert populated_manager.get_total_students() == 4


def test_removed_student_cannot_be_found(populated_manager):
    populated_manager.remove_student("S002")
    with pytest.raises(KeyError):
        populated_manager.get_student("S002")


def test_remove_keeps_the_other_students(populated_manager):
    populated_manager.remove_student("S002")
    ids = [s.student_id for s in populated_manager.get_all_students()]
    assert ids == ["S001", "S003", "S004", "S005"]


def test_remove_unknown_student_raises_key_error(populated_manager):
    with pytest.raises(KeyError):
        populated_manager.remove_student("S999")
    assert populated_manager.get_total_students() == 5


def test_remove_same_student_twice_raises_key_error(populated_manager):
    populated_manager.remove_student("S001")
    with pytest.raises(KeyError):
        populated_manager.remove_student("S001")


def test_id_can_be_used_again_after_removal(empty_manager):
    empty_manager.add_student("S1", "Alice", "alice@example.com")
    empty_manager.remove_student("S1")
    empty_manager.add_student("S1", "Bob", "bob@example.com")
    assert empty_manager.get_student("S1").name == "Bob"


# =====================================================
# StudentManager: get_all_students and get_total_students
# =====================================================

def test_get_all_students(populated_manager):
    students = populated_manager.get_all_students()
    assert len(students) == 5
    names = [s.name for s in students]
    assert names == ["Alice", "Bob", "Carol", "Dave", "Eve"]


def test_get_all_students_returns_a_copy(populated_manager):
    students = populated_manager.get_all_students()
    students.clear()
    # clearing our copy must not touch the manager
    assert populated_manager.get_total_students() == 5


def test_total_goes_up_with_each_student(empty_manager):
    empty_manager.add_student("S1", "A", "a@x.com")
    assert empty_manager.get_total_students() == 1
    empty_manager.add_student("S2", "B", "b@x.com")
    assert empty_manager.get_total_students() == 2
    empty_manager.add_student("S3", "C", "c@x.com")
    assert empty_manager.get_total_students() == 3


# =====================================================
# StudentManager: get_top_performers
# =====================================================

def test_top_performers_default_is_top_3(populated_manager):
    top = populated_manager.get_top_performers()
    assert [s.name for s in top] == ["Alice", "Bob", "Carol"]


def test_top_performers_n_equals_1(populated_manager):
    top = populated_manager.get_top_performers(1)
    assert [s.name for s in top] == ["Alice"]


def test_top_performers_n_equals_all_students(populated_manager):
    top = populated_manager.get_top_performers(5)
    assert [s.name for s in top] == ["Alice", "Bob", "Carol", "Dave", "Eve"]


def test_top_performers_n_bigger_than_total(populated_manager):
    top = populated_manager.get_top_performers(100)
    assert len(top) == 5


def test_top_performers_on_empty_manager(empty_manager):
    assert empty_manager.get_top_performers(3) == []


def test_top_performers_sorted_by_gpa_not_by_order_added(empty_manager):
    low = empty_manager.add_student("S1", "Low", "l@x.com")
    high = empty_manager.add_student("S2", "High", "h@x.com")
    low.add_grade("A", 50)
    high.add_grade("A", 95)
    assert empty_manager.get_top_performers(2) == [high, low]


def test_top_performers_tie_is_sorted_by_name_z_to_a(empty_manager):
    amy = empty_manager.add_student("S1", "Amy", "amy@x.com")
    zed = empty_manager.add_student("S2", "Zed", "zed@x.com")
    amy.add_grade("A", 95)
    zed.add_grade("A", 95)
    top = empty_manager.get_top_performers(2)
    assert [s.name for s in top] == ["Zed", "Amy"]


@pytest.mark.parametrize("n", [0, -1, -10])
def test_top_performers_zero_or_negative_n_raises_value_error(populated_manager, n):
    with pytest.raises(ValueError, match="positive"):
        populated_manager.get_top_performers(n)


# =====================================================
# StudentManager: filter_by_min_gpa
# =====================================================

@pytest.mark.parametrize("min_gpa, expected_names", [
    (0.0, ["Alice", "Bob", "Carol", "Dave", "Eve"]),
    (1.0, ["Alice", "Bob", "Carol", "Dave"]),
    (2.0, ["Alice", "Bob", "Carol"]),
    (3.0, ["Alice", "Bob"]),
    (3.5, ["Alice"]),
    (4.0, ["Alice"]),
])
def test_filter_by_min_gpa(populated_manager, min_gpa, expected_names):
    result = populated_manager.filter_by_min_gpa(min_gpa)
    assert [s.name for s in result] == expected_names


def test_filter_includes_student_exactly_at_min_gpa(populated_manager):
    names = [s.name for s in populated_manager.filter_by_min_gpa(2.0)]
    assert "Carol" in names


def test_filter_excludes_student_just_below_min_gpa(populated_manager):
    names = [s.name for s in populated_manager.filter_by_min_gpa(2.01)]
    assert "Carol" not in names


def test_filter_on_empty_manager(empty_manager):
    assert empty_manager.filter_by_min_gpa(2.0) == []


@pytest.mark.parametrize("min_gpa", [-0.01, -1, 4.01, 5])
def test_filter_out_of_range_raises_value_error(populated_manager, min_gpa):
    with pytest.raises(ValueError, match="between 0.0 and 4.0"):
        populated_manager.filter_by_min_gpa(min_gpa)


def test_filter_uses_updated_grades(populated_manager):
    populated_manager.update_grade("S005", "MATH101", 95)
    names = [s.name for s in populated_manager.filter_by_min_gpa(4.0)]
    assert names == ["Alice", "Eve"]