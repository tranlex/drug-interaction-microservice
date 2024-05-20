import zmq

# Set up ZeroMQ client
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")  # Connect to the server address and port

# User input for two drug names
drug1 = input("Enter the first drug name: ")
drug2 = input("Enter the second drug name: ")

# Send the user input to the server
message = f"{drug1},{drug2}"
socket.send_string(message)

# Receive and print the response from the server
response = socket.recv_string()
print(response)