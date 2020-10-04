import Get_arduino_data

import json

# Getting all used ports:
serial_ports = Get_arduino_data.get_ports()
# Detecting the port of the arduino:
arduino_port = Get_arduino_data.find_arduino(serial_ports)
# Instantiating the arduino and connecting to it:
arduino = Get_arduino_data.connect_to_arduino(arduino_port)

# Function to parse burst data from arduino into python dicts (js objects)
def parse_data(arduino_message):
    # Spliting the message into separate balls (array of arrays of [x,y,error]):
    splitted_message = list(
        map(lambda ball: ball.split(","), current_message.split(" "))
    )
    # Parsing the numbers out of the string arrays and converting them to tuples:
    burst_coords = list(
        map(lambda ball: (float(ball[0]), float(ball[1])), splitted_message)
    )
    # Converting the tuples into dicts in order to write them to the JSON file as js objects:
    burst_coords = list(
        map(lambda coords: {"x": coords[0], "y": coords[1]}, burst_coords)
    )
    # Finally returning the array of the dicts:
    return burst_coords


# Function to take the bursts data in the form of a dict (equivalent to js object), which contains an array of bursts,
# and to write it to the coordinates file
def write_burst_to_file(data):
    with open("Coords.json", "w") as coords_file:
        json.dump(data, coords_file)


# Getting the data that is already on the file
with open("Coords.json", "r") as coordinates_file:
    previous_data = json.load(coordinates_file)
    # Getting the arrray of the bursts were already shot:
    bursts_list = previous_data["bursts"]
    # Getting the number of bursts were already shot:
    current_burst_number = len(bursts_list) + 1

# A loop that runs forever to collect data from arduino and pass it to the file
while True:
    # Getting the message from the arduino:
    current_message = Get_arduino_data.read_arduino(arduino)
    if current_message:
        # parsing the message to an array of tuples of x,y coordinates:
        burst_coords = parse_data(current_message)
        # Putting the data in a dict which will be written to the JSON as an js object:
        burst_obj = {
            "burstNumber": current_burst_number,
            "burstCoordinates": burst_coords,
        }
        # Adding the new burst dict to the list:
        bursts_list.append(burst_obj)

        # Finally updating the JSON file with the new data:
        write_burst_to_file({"bursts": bursts_list})

        # Increase the burst number for the next burst
        current_burst_number += 1
