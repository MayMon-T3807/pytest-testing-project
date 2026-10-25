# Project 7 Report: Automated Testing with Pytest

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Pytest Version & Framework:**`, `**GitHub Repository URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information
- **Name:** May Mon Thant
- **MMDT ID:** MMDT062

---

## Section 1: Test Suite Configuration
- **Pytest Version & Framework:** Pytest 9.1.1 with pytest-cov 7.1.0, Python 3.13, run on Windows in a virtual environment
- **Total Test Cases Written:** 394 test cases (calculator, data validator and student manager tests)
- **Measured Code Coverage (%):** 100% (statement and branch coverage on src/)
- **Key Fixtures Implemented:** empty_manager (a fresh StudentManager), sample_student (one valid Student), populated_manager (5 students with different GPAs), valid_registration_data (a valid registration dictionary)

---

## Section 2: Test Case Design & Boundary Analysis
- **Calculator Boundary & Edge Cases:** Empty lists and tuples, single-item lists, scores at exactly 0 and 100 and just outside them (-0.01 and 100.01), float scores and rounding to 2 decimals, duplicate maximums, all-negative lists, is_prime for -1, 0, 1, 2, 3, odd composites like 9, 25, 49 and 121, large primes like 97 and 7919, 0! and 20!, 0 raised to a negative power, and booleans, strings and None as wrong types.
- **Validator Exception Scenarios:** Emails with a missing @, missing domain, missing extension, consecutive dots and spaces; passwords that are too short (7 characters), too long (129 characters) or missing an uppercase letter, lowercase letter, digit or special character, with the error message checked using match; usernames of length 2, 3, 20 and 21 and ones starting with a digit or underscore; ages 12, 13, 120 and 121; booleans and strings as wrong types; and registrations with a missing field, a bad child field, or data that is not a dictionary.
- **Student Manager State Transitions:** Adding a student by object and by details, rejecting a duplicate ID without overwriting the first student, updating a grade and checking the recalculated GPA, GPA brackets at exactly 90, 80, 70 and 60 and just below, removing a student so the count drops and later lookups raise KeyError, reusing an ID after removal, top performers with n equal to 1, all students and more than the total, and filtering by minimum GPA at the exact boundary.

---

## Section 3: Local Verification & Feature Checklist
*Check the test modules and features you successfully implemented and verified locally by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Module 1: Calculator Unit Tests with Boundary & Type Assertions (`test_calculator.py`)
- [x] Parameterized Testing with `@pytest.mark.parametrize` for Multiple Input Scenarios
- [x] Module 2: Data Validator Tests with Custom Exception Assertions (`pytest.raises`)
- [x] Module 3: Student Management System Tests with State Mutation & CRUD Verification
- [x] Reusable Pytest Fixtures in `conftest.py` for Modular Test Setup
- [x] Mutation Testing & Bug Detection Verification (Catching Hidden Mutants)
- [x] Code Coverage Analysis with `pytest-cov` (>= 85% Coverage)

---

## Section 4: Deployed and Presentation Information
- **GitHub Repository URL:** [Provide your public GitHub repository URL here]
- **Video Presentation Link:** [Provide an accessible link to your 5–7 minute video presentation]

---

## Section 5: Discussion
*Provide your written analysis for each point by replacing the bracket placeholders below:*
- **Explain why a test suite that passes 100% does not guarantee code correctness, and how mutation testing or evaluating tests against buggy code verifies test suite effectiveness.**
    All 394 of my tests pass and my coverage is 100%, but that does not prove my code has no bugs. It only means my tests did not find any problem. A test can run a line of code without checking the result well, so a bug can still hide there. Mutation testing helps because it puts small bugs into the code on purpose, like changing score > 100 to score >= 100, or letting a duplicate student ID replace the old student. Then my tests run on the buggy code. If a test fails, it caught the bug. If all tests still pass, my tests are too weak. That is why I tested edge values like 0, 100, 100.01, the GPA cut-offs at 90, 80, 70 and 60, and the ages 12, 13, 120 and 121.
- **Compare classical unit and integration testing in software engineering with modern AI engineering evaluation (e.g., LLM benchmarks, unit testing AI agents/tool calls, and Process Reward Models / LLM-as-a-judge).**
    Classical testing works with code that gives the same answer every time. For example, calculate_average with 80, 90 and 100 always gives 90, so one assert is enough and the test either passes or fails. AI is harder to test because its answers can change each time, and there can be more than one good answer. So AI evaluation uses different tools. Benchmarks ask a model many questions and give a score, like the percent it got right. For AI agents, we can check that the agent picked the right tool and gave the right inputs, which is like how my validators check inputs and raise errors. LLM-as-a-judge uses another AI to grade an answer when exact matching is not possible. Process Reward Models check each reasoning step, not only the final answer, like checking every test case instead of only the total. In both cases, we should test edge cases and wrong inputs, not just easy ones. The difference is that classical tests give a clear yes or no, but AI evaluation often gives a score that has some uncertainty.