import serial

# Opening a serial port with EVERY parameter spelled out explicitly.
# In real projects you usually only override what differs from defaults,
# but seeing them all here makes the physical layer concrete.
ser = serial.Serial(
    port='COM3',                    # On Linux this would be '/dev/ttyUSB0'
    baudrate=115200,                # Both sides must agree on this exact value
    bytesize=serial.EIGHTBITS,      # 8 data bits per frame
    parity=serial.PARITY_NONE,      # No parity bit (most common for modern devices)
    stopbits=serial.STOPBITS_ONE,   # 1 stop bit
    timeout=1,                      # Read call returns after 1s even if data is incomplete
    write_timeout=1,                # Same idea, but for write() calls
    rtscts=False,                   # Hardware flow control (RTS/CTS lines) off
    dsrdtr=False,                   # Another hardware handshake line, off
    xonxoff=False                   # Software flow control off
)

# Context manager pattern — guarantees the port is closed even if an
# exception is raised inside the block. Prefer this over manual open/close.
with serial.Serial('COM3', 115200, timeout=1) as ser:
    ser.write(b'\x01\x02') # send two bytes to the device
    response = ser.read(4)
    
# pyserial ALWAYS works with raw bytes objects, never with str.
# Python 3 enforces a strict separation between the two types.

# Sending raw binary bytes directly (e.g. a custom binary protocol)
ser.write(b'\x01\x02\x03')

# Sending a human-readable command (e.g. an AT command to a modem)
# Strings must be explicitly encoded to bytes before writing.
command = "AT+CMD\r\n"
ser.write(command.encode('ascii'))

# Reading returns bytes. To get a printable string, decode explicitly.
raw_bytes = ser.read(10)
text = raw_bytes.decode('utf-8', errors='replace')
# errors='replace' swaps any invalid byte with a placeholder character
# instead of raising an exception — useful when the device might send
# raw sensor data mixed with text, where not every byte is valid UTF-8.

# If the device sent a leftover response from a previous command that
# was never read, the NEXT read() call will return that old data first,
# silently corrupting your protocol logic. Always flush before sending
# a new command in a request/response protocol.

ser.reset_input_buffer()   # Discard anything currently waiting to be read
ser.reset_output_buffer()  # Discard anything queued to be written (rarely needed)

ser.write(b'GET_STATUS\r\n')
response = ser.read(20)

import time

# in_waiting returns the number of bytes currently sitting in the OS
# receive buffer, WITHOUT blocking — safe to call in a tight loop.
while True:
    if ser.in_waiting > 0:
        chunk = ser.read(ser.in_waiting)
        print("Received:", chunk)
    time.sleep(0.05)  # Small sleep to avoid pegging the CPU at 100%