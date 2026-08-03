*** Settings ***
Documentation       FOTA Server Integration Tests
Library             CustomSocketLibrary.py

*** Variables ***
${SERVER_IP}        127.0.0.1
${PORT}             8080
${VALID_KEY}        fota_pass_2026
${INVALID_KEY}      wrong_key_123

*** Test Cases ***
Test 1: Successful Firmware Update Sequence
    [Documentation]    Verifies the happy flow of authenticating and flashing firmware successfully.
    [Setup]            Connect To Socket Server    host=${SERVER_IP}    port=${PORT}
    [Teardown]         Disconnect Socket

    Send And Compare    AUTH ${VALID_KEY}            AUTH_OK
    Send And Compare    START_FLASH 1024             READY
    Send And Compare    WRITE_CHUNK 0xDEADBEEF       ACK
    Send And Compare    FINISH_FLASH                 FLASH_SUCCESS: CRC_OK

Test 2: Invalid Password Rejection
    [Documentation]    Verifies that the server rejects authentication with an invalid key.
    [Setup]            Connect To Socket Server    host=${SERVER_IP}    port=${PORT}
    [Teardown]         Disconnect Socket

    Send And Compare    AUTH ${INVALID_KEY}          ERR_AUTH_FAILED

Test 3: Out-of-Sequence Flash Attempt (Negative Test)
    [Documentation]    Verifies that sending data chunks without starting the flash sequence returns an error.
    [Setup]            Connect To Socket Server    host=${SERVER_IP}    port=${PORT}
    [Teardown]         Disconnect Socket

    Send And Compare    AUTH ${VALID_KEY}            AUTH_OK
    Send And Compare    WRITE_CHUNK 0x1234           ERR_SEQUENCE

*** Keywords ***
Send And Compare
    [Documentation]    Sends a command to the server and asserts the expected response.
    [Arguments]        ${payload}    ${expectedResponse}

    Send Socket Payload     ${payload}\n
    ${res}=                 Receive Socket Data
    Should Contain          ${res}    ${expectedResponse}