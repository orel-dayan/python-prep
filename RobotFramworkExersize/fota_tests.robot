*** Settings ***
Documentation               fota server testing
Library                     CustomSocketLibrary.py

*** Variables ***
${SERVER_IP}                127.0.0.1
${PORT}                     8080
${AUTH_KEY}                 fota_pass_2026
${INVALID_KEY}              wrong_key_123

*** Test Cases ***
Successful Firmware Update Sequence
    [Documentation]         Happy Flow Testing
    [Setup]                 Open Connection
    [Teardown]              Close Connection

    Send And Compare        AUTH ${AUTH_KEY}            AUTH_OK
    Flash                   0xDEADBEEF

Invalid Password Rejection
    [Documentation]         Verifies server rejects wrong auth key
    [Setup]                 Open Connection
    [Teardown]              Close Connection

    Send And Compare        AUTH ${INVALID_KEY}         ERR_AUTH_FAILED    

Out-of-Sequence Flash Attempt
    [Documentation]         Verifies server rejects write chunk before flash start
    [Setup]                 Open Connection
    [Teardown]              Close Connection 

    Send And Compare        AUTH ${AUTH_KEY}            AUTH_OK
    Send And Compare        WRITE_CHUNK 0x1234          ERR_SEQUENCE


*** Keywords ***
Open Connection
     Connect To Socket Server    host=${SERVER_IP}    port=${PORT}

Close Connection 
     Disconnect Socket

Flash
    [Documentation]         Perform Flashing Sequence
    [Arguments]             ${dataChunk}

    Send And Compare        START_FLASH 1024            READY    
    Send And Compare        WRITE_CHUNK ${dataChunk}    ACK
    Send And Compare        FINISH_FLASH                FLASH_SUCCESS: CRC_OK

Send And Compare
    [Documentation]         Send a payload and compare the response to a given pattern
    [Arguments]             ${payload}      ${expectedResponse}

    Send Socket Payload     ${payload}\n
    ${resWrite}=            Receive Socket Data
    Should Contain          ${resWrite}     ${expectedResponse}