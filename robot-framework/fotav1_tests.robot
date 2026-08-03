*** Settings ***
Documentation       FOTA (Firmware Over-The-Air) socket protocol tests.
Library             CustomSocketLibrary.py
Library             String

*** Variables ***
${SERVER_IP}        127.0.0.1
${PORT}             8080
${VALID_KEY}        fota_pass_2026

*** Keywords ***
Open Socket Connection
    Connect To Socket Server    host=${SERVER_IP}    port=${PORT}

Close Socket Connection
    Disconnect Socket

Send And Expect
    [Documentation]    Sends a payload and asserts the server's response matches exactly.
    [Arguments]    ${payload}    ${expected}
    Send Socket Payload    ${payload}\n
    ${response}=    Receive Socket Data
    ${response}=    Strip String    ${response}
    Should Be Equal    ${response}    ${expected}

Authenticate
    [Arguments]    ${key}
    Send And Expect    AUTH ${key}    AUTH_OK

*** Test Cases ***
Successful Firmware Update Sequence
    [Documentation]    Full happy-path flash: auth -> start -> write -> finish.
    [Setup]       Open Socket Connection
    [Teardown]    Close Socket Connection

    Authenticate       ${VALID_KEY}
    Send And Expect    START_FLASH 1024          READY
    Send And Expect    WRITE_CHUNK 0xDEADBEEF    ACK
    Send And Expect    FINISH_FLASH              FLASH_SUCCESS: CRC_OK

Invalid Password Rejection
    [Documentation]    Wrong auth key must be rejected with ERR_AUTH_FAILED.
    [Setup]       Open Socket Connection
    [Teardown]    Close Socket Connection

    Send And Expect    AUTH wrong_key_123    ERR_AUTH_FAILED

Out-of-Sequence Flash Attempt
    [Documentation]    WRITE_CHUNK before START_FLASH must be rejected with ERR_SEQUENCE.
    [Setup]       Open Socket Connection
    [Teardown]    Close Socket Connection

    Authenticate        ${VALID_KEY}
    Send And Expect    WRITE_CHUNK 0x1234    ERR_SEQUENCE
