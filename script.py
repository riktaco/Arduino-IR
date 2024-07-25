import serial
import pyautogui
import webbrowser

# Set up the serial connection
ser = serial.Serial('COM3', 115200)

# Function to move the cursor based on the received command
def move_cursor(command):
    if command == '46':
        pyautogui.moveRel(0, -25)
        print("Moving cursor up")
    elif command == '15':
        pyautogui.moveRel(0, 25)
        print("Moving cursor down")
    elif command == '44':
        pyautogui.moveRel(-25, 0)
        print("Moving cursor left")
    elif command == '43':
        pyautogui.moveRel(25, 0)
        print("Moving cursor right")
    elif command == '40':
        pyautogui.click()
        print("Clicked")
    elif command == '45':
        webbrowser.open("https://www.netflix.com")
        print("Opened Netflix")
    else:
        print("Invalid command")

try:
    while True:
        # Read the command from the serial port
        command = ser.readline().decode('utf-8').strip()
        move_cursor(command)
except KeyboardInterrupt:
    print("Program terminated")
finally:
    ser.close()