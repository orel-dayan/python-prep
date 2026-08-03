*** Settings ***
Library    board_library.py
Suite Setup       Connect To Board    /dev/ttyUSB0
Suite Teardown    Close Connection

*** Variables ***
${EXPECTED_STATUS}    OK

*** Test Cases ***
Board Responds To Ping
    Send Command    PING
    ${response}=    Read Response
    Should Be Equal    ${response}    PONG

Board Reports Correct Status
    Send Command    GET_STATUS
    ${status}=    Read Response
    Should Be Equal    ${status}    ${EXPECTED_STATUS}

Temperature Sensor Within Range
    Send Command    READ_TEMP
    ${temp}=    Read Response
    ${temp}=    Convert To Number    ${temp}
    Should Be True    15 < ${temp} < 40
