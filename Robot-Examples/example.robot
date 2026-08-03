*** Settings ***
# Documentation and imports for this test suite
Documentation     Example test suite demonstrating Robot Framework basics
Library           Collections          # Built-in library for list/dict operations
Library           ./custom_keywords.py # Our own custom keyword library (Python file)

*** Variables ***
# Variables are reusable values, referenced later with ${VAR_NAME}
${BASE_URL}       https://example.com/api
${VALID_USER}     admin
${VALID_PASS}     secret123

*** Test Cases ***
# Each Test Case is a sequence of Keywords (built-in or custom)
Login With Valid Credentials Should Succeed
    [Documentation]    Verifies that a valid login returns success
    ${result}=    Perform Login    ${VALID_USER}    ${VALID_PASS}
    Should Be True    ${result}

Login With Invalid Password Should Fail
    [Documentation]    Verifies that an invalid password is rejected
    ${result}=    Perform Login    ${VALID_USER}    wrong_password
    Should Not Be True    ${result}

*** Keywords ***
# Custom keywords defined directly inside the .robot file (no Python needed)
Perform Login
    [Arguments]    ${username}    ${password}
    [Documentation]    Wraps the Python keyword and adds a log line
    Log    Attempting login for user: ${username}
    ${success}=    Validate Credentials    ${username}    ${password}
    RETURN    ${success}