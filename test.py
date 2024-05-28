# Test program to demonstrate calling the drug interaction microservice

import zmq

# Set up ZeroMQ client
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")  # Connect to the server address and port

# Sample drug name for testing
drug = "acetaminophen"

# Send the sample drug name to the server
socket.send_string(drug)

# Receive and print the response from the server
response = socket.recv_string()
print(response)