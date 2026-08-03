*** Settings ***
Documentation    Testing embedded device server via TCP socket.
Library          CustomSocketLibrary.py

*** Variables ***
${SERVER_IP}     127.0.0.1
${PORT}          8080

*** Test Cases ***
Verify Hardware Responds Over TCP Socket
    [Setup]       Connect To Socket Server    host=${SERVER_IP}    port=${PORT}
    [Teardown]    Disconnect Socket

    Send Socket Payload      GET_SYS_STATUS\n
    ${response}=             Receive Socket Data    buffer_size=1024
    Should Contain           ${response}            STATUS=OK

Verify Hardware Returns Temperature Reading
    [Setup]       Connect To Socket Server    host=${SERVER_IP}    port=${PORT}
    [Teardown]    Disconnect Socket

    Send Socket Payload      GET_TEMPERATURE\n
    ${response}=             Receive Socket Data    buffer_size=1024
    Should Contain           ${response}            TEMP=

Verify Hardware Returns Version Info
    [Setup]       Connect To Socket Server    host=${SERVER_IP}    port=${PORT}
    [Teardown]    Disconnect Socket

    Send Socket Payload      GET_VERSION\n
    ${response}=             Receive Socket Data    buffer_size=1024
    Should Contain           ${response}            VERSION=

Verify Hardware Responds To Ping
    [Setup]       Connect To Socket Server    host=${SERVER_IP}    port=${PORT}
    [Teardown]    Disconnect Socket

    Send Socket Payload      PING\n
    ${response}=             Receive Socket Data    buffer_size=1024
    Should Contain           ${response}            PONG

Verify Hardware Handles Reset Command
    [Setup]       Connect To Socket Server    host=${SERVER_IP}    port=${PORT}
    [Teardown]    Disconnect Socket

    Send Socket Payload      RESET\n
    ${response}=             Receive Socket Data    buffer_size=1024
    Should Contain           ${response}            STATUS=RESETTING

Verify Hardware Rejects Unknown Command
    [Setup]       Connect To Socket Server    host=${SERVER_IP}    port=${PORT}
    [Teardown]    Disconnect Socket

    Send Socket Payload      FOO_BAR\n
    ${response}=             Receive Socket Data    buffer_size=1024
    Should Contain           ${response}            ERROR=UNKNOWN_COMMAND
