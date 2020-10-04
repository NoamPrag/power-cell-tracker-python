import serial.tools.list_ports
import serial

# Get a list of all computer ports that are currently in use
def get_ports():
    return serial.tools.list_ports.comports()


# A function that takes a list of ports and returns the arduino port
def find_arduino(portsFound):
    comPort = "none"
    numConnections = len(portsFound)
    for i in range(0, numConnections):
        port = portsFound[i]
        strPort = str(port)

        if "Generic CDC" in strPort:
            splitPort = strPort.split(" ")
            comPort = splitPort[0]

    return comPort


# Start the communication with the arduino
def connect_to_arduino(port):
    if port != "none":
        ser = serial.Serial(port=port, baudrate=115200, timeout=None)
        print("Connected to " + port)
        return ser
    else:
        print("Arduino Not Found!")


# Get the arduino message decoded in a single line
def read_arduino(arduino):
    return arduino.readline().decode()