import zmq
import requests
from bs4 import BeautifulSoup

# Set up ZeroMQ server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5555")  # Set the server address and port

# Function to query drug interaction data
def get_drug_interaction_data(drug_name, filter_val):
    url = f"https://www.drugs.com/drug-interactions/{drug_name}-index.html?filter={filter_val}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract drug interaction data
    interactions = soup.find('div', {'id': 'content'}).text
    return interactions

# Function to query food interaction data
def get_food_interaction_data(drug_name):
    url = f"https://www.drugs.com/food-interactions/{drug_name}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the section with the food interactions
    food_section = soup.find('div', {'id': 'content'})

    # Extract the paragraph section/text when "food" is mentioned
    food_interaction = ""
    if food_section:
        for p in food_section.find_all('p'):
            if "food" in p.text.lower():
                food_interaction += p.text + "\n"

    return food_interaction

# Main loop to handle client requests
while True:
    message = socket.recv_string()
    drug1, drug2 = message.split(",")

    # Check for drug interactions
    severity = None
    for filter_val in range(1, 4):
        interaction_data = get_drug_interaction_data(drug1, filter_val)
        if drug2 in interaction_data:
            if filter_val == 3:
                severity = "Highly clinically significant. Avoid combinations; the risk of the interaction outweighs the benefit."
            elif filter_val == 2:
                severity = "Moderately clinically significant. Usually avoid combinations; use it only under special circumstances."
            elif filter_val == 1:
                severity = "Minimally clinically significant. Minimize risk; assess risk and consider an alternative drug, take steps to circumvent the interaction risk and/or institute a monitoring plan. "
            break

    # Fetch food interactions for drug1 and drug2
    drug1_food_interactions = get_food_interaction_data(drug1)
    drug2_food_interactions = get_food_interaction_data(drug2)

    # Display the received message
    # This line prints the message received from the client
    print(f"Received message: {message}")

    # Prepare the response message
    response_message = ""
    if severity:
        response_message += f"Interaction between {drug1} and {drug2} is {severity}\n\n"
    else:
        response_message += f"No interaction between {drug1} and {drug2}\n"

    response_message += f"Food interactions for {drug1}:\n{drug1_food_interactions}\n\nFood interactions for {drug2}:\n{drug2_food_interactions}"

    # Send the combined results back to the client
    socket.send_string(response_message)
