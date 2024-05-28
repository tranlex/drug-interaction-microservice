import zmq
import requests
from bs4 import BeautifulSoup

# Set up ZeroMQ server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5555")  # Set the server address and port

def get_drug_interaction_data(drug_name):
    url = f"https://www.drugs.com/drug-interactions/{drug_name}-index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags within the content section that contain drug names
    drug_links = soup.select('#content a[href^="/drug-interactions/"]')

    # Extract the text from the <a> tags excluding "Check interactions" and "Interactions" text
    drug_names = '\n'.join(link.get_text() for link in drug_links if link.get_text() not in ["Check interactions", "Interactions"])

    return drug_names

# Function to query food interaction data
def get_food_interaction_data(drug_name):
    url = f"https://www.drugs.com/food-interactions/{drug_name}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    food_section = soup.find('div', {'id': 'content'})
    food_interaction = ""
    if food_section:
        for p in food_section.find_all('p'):
            if "food" in p.text.lower():
                food_interaction += p.text + "\n"

    return food_interaction

# Main loop to handle client requests
while True:
    drug_name = socket.recv_string()

    # Check for drug interactions
    interaction_data = get_drug_interaction_data(drug_name)

    # Fetch food interactions for the drug
    drug_food_interactions = get_food_interaction_data(drug_name)

    # Combine drug interactions and food interactions into a single list
    result_list = [f"General interactions for {drug_name}:\n{interaction_data}", f"Food interactions for {drug_name}:\n{drug_food_interactions}"]

    # Prepare the response message by joining the list elements
    response_message = '\n\n'.join(result_list)

    # Display the received message
    print(f"Received message: {drug_name}")

    # Send the combined results back to the client
    socket.send_string(response_message)
