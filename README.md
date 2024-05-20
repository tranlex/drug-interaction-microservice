# drug-interaction-microservice
This microservice provides a simple API for querying drug interaction data, including potential interactions between two drugs as well as food interactions for individual drugs. It uses ZeroMQ for messaging between the client and server.

## Prerequisites

Before you begin, ensure you have installed the following:

- Python 3.6 or higher
- `zmq` library for ZeroMQ
- `requests` library for HTTP requests
- `beautifulsoup4` library for parsing HTML

You can install the required libraries using `pip`:

```bash
pip install zmq requests beautifulsoup4
```

## Server Setup

The server script `server.py` should be running and listening for client requests. To start the server, run:

```bash
python server.py
```

The server binds to the address `tcp://127.0.0.1:5555` and waits for incoming requests from clients.

## Client Communication Contract

### Requesting Data

To request data from the microservice, a client must send a string message to the server in the format "drug1,drug2" where `drug1` and `drug2` are the names of the drugs for which you want to check interactions.

Here is an example of how to programmatically send a request to the server using the `Client.py` script:

```python
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

# Replace 'aspirin' and 'ibuprofen' with the desired drug names
message = "aspirin,ibuprofen"
socket.send_string(message)
```

### Receiving Data

After sending a request, the client should wait to receive a response from the server. The response will be a string containing information about the interaction between the two drugs and their food interactions.

Here is an example of how to programmatically receive a response from the server using the `Client.py` script:

```python
# Continue from the previous code where the request was sent
response = socket.recv_string()
print(response)
```

The response message will contain the following information:

- Whether there is an interaction between the two drugs, and if so, the severity of the interaction.
- Food interaction information for each of the two drugs.

## Example

Client sends a request:

```python
socket.send_string("warfarin,aspirin")
```

Server response might look like:
```plaintext
Interaction between warfarin and aspirin is Moderately clinically significant. Usually avoid combinations; use it only under special circumstances.

Food interactions for warfarin:
Vitamin K can affect how warfarin works in your body. Avoid drastic changes in dietary vitamin K intake while on warfarin. Also, avoid cranberry juice or cranberries while taking warfarin.

Food interactions for aspirin:
Aspirin may cause stomach bleeding. It is advised to avoid alcohol while taking aspirin as it can increase the risk of stomach bleeding. Consult your healthcare provider for personalized advice.
```

In this example, the client has programmatically requested the interaction data for "warfarin" and "aspirin" from the server. The server has processed the request, queried the interaction data, and responded with the relevant information concerning drug-drug interaction severity and food interactions for each drug.

## Notes for Developers

- Ensure that the server script `server.py` is running before sending requests from the client.
- The drug names used in the request should be in lowercase and match the names used on the website "https://www.drugs.com/" to ensure accurate results.

## UML Sequence Diagram

![IMG_707297BC48D4-1](https://github.com/tranlex/drug-interaction-microservice/assets/129806187/926c02ee-cf76-417a-a7c8-39fea51627aa)

