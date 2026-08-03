*** Settings ***
Documentation    Advanced suite testing persistent sessions, security checks, and streaming over TCP.
Library          CustomSocketLibrary.py
Library          String

*** Variables ***
${SERVER_IP}     127.0.0.1
${PORT}          8080
${AUTH_KEY}      secret123

*** Test Cases ***
Verify Authenticated Session Workflow
    [Documentation]    Ensures protected commands (READ_SENSORS) fail until valid authentication occurs.
    [Setup]       Connect To Socket Server    host=${SERVER_IP}    port=${PORT}
    [Teardown]    Disconnect Socket

    # 1. Attempt protected action before login -> Should fail
    Send Socket Payload      READ_SENSORS\n
    ${unauth_resp}=          Receive Socket Data
    Should Contain           ${unauth_resp}    ERR_UNAUTHORIZED

    # 2. Authenticate
    Send Socket Payload      AUTH ${AUTH_KEY}\n
    ${auth_resp}=            Receive Socket Data
    Should Contain           ${auth_resp}      AUTH_OK

    # 3. Attempt protected action again -> Should succeed
    Send Socket Payload      READ_SENSORS\n
    ${sensor_resp}=          Receive Socket Data
    Should Contain           ${sensor_resp}    TEMP=
    Should Contain           ${sensor_resp}    VOLT=

Verify Invalid Command Error Recovery
    [Documentation]    Verifies that sending corrupted or unknown commands returns proper error without crashing session.
    [Setup]       Connect To Socket Server    host=${SERVER_IP}    port=${PORT}
    [Teardown]    Disconnect Socket

    Send Socket Payload      BAD_CMD_123\n
    ${err_resp}=             Receive Socket Data
    Should Contain           ${err_resp}       ERR_UNKNOWN_CMD: BAD_CMD_123

    # Ensure device connection is still healthy after error
    Send Socket Payload      GET_SYS_STATUS\n
    ${ok_resp}=              Receive Socket Data
    Should Contain           ${ok_resp}        STATUS=OK

Verify Multi-line Log Dump Stream
    [Documentation]    Tests reading multi-line logs from the device and counting output lines.
    [Setup]       Connect To Socket Server    host=${SERVER_IP}    port=${PORT}
    [Teardown]    Disconnect Socket

    Send Socket Payload      DUMP_LOGS\n
    ${logs}=                 Receive Socket Data    buffer_size=4096
    
    # Split string by lines and verify count
    @{log_lines}=            Split To Lines    ${logs}
    Length Should Be         ${log_lines}      3
    Should Contain           ${log_lines}[0]   BOOT OK

Verify Idle Timeout Handling
    [Documentation]    Ensures device remains silent and client catches the read timeout properly.
    [Setup]       Connect To Socket Server    host=${SERVER_IP}    port=${PORT}    timeout=1.5
    [Teardown]    Disconnect Socket

    Send Socket Payload    IDLE\n
    
    # Robot Framework expects the read operation to fail specifically with a timeout error
    Run Keyword And Expect Error    *TimeoutError*    Receive Socket Data    buffer_size=1024