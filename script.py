import serial
import pyautogui
import webbrowser

# Set up the serial connection
ser = serial.Serial('COM3', 115200)

cursor_speed = 25
ser.write(str(cursor_speed).encode())

# Function to move the cursor based on the received command
def move_cursor(command):
    global cursor_speed
    if command == '46':
        pyautogui.moveRel(0, -cursor_speed)
        print("Moving cursor up")
    elif command == '15':
        pyautogui.moveRel(0, cursor_speed)
        print("Moving cursor down")
    elif command == '44':
        pyautogui.moveRel(-cursor_speed, 0)
        print("Moving cursor left")
    elif command == '43':
        pyautogui.moveRel(cursor_speed, 0)
        print("Moving cursor right")
    elif command == '40':
        pyautogui.click()
        print("Clicked")
    elif command == '45':
        webbrowser.open("https://www.netflix.com")
        print("Opened Netflix")
    elif command == '9':
        cursor_speed+=5
        send_data(str(cursor_speed))
        print("Speed increased")
    elif command == '7':
        cursor_speed-=5
        send_data(str(cursor_speed))
        print("Speed decreased")
    else:
        print("Invalid command")

def send_data(data):
    ser.write(data.encode())  # Send data to Arduino
    print(f"Sent: {data}")

try:
    while True:
        # Read the command from the serial port
        command = ser.readline().decode('utf-8').strip()
        move_cursor(command)
except KeyboardInterrupt:
    print("Program terminated")
finally:
    ser.close()