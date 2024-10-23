import json
import logging
import os
import requests

from constants import PORT_API_URL, WORKLOAD_BLUEPRINT_ID


def update_port(entity_identifier: str, insights: str = None):
    try:
        if insights:
            response = update_port_entity(entity_identifier, insights)
        else:
            response = update_port_entity(entity_identifier)

        logging.info(f"Response from Port API: {response}")
    except Exception as e:
        logging.error(f"Failed to update Port entity: {e}")


def update_port_entity(entity_identifier: str, insights: str = "") -> int:
    access_token = get_access_token()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    url = f"https://api.getport.io/v1/blueprints/{WORKLOAD_BLUEPRINT_ID}/entities/{entity_identifier}"

    payload = json.dumps({
        "properties": {
            "insights": insights
        }
    })
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return response.status_code


def get_access_token():
    try:
        # Get environment variables
        PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
        PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")

        # Ensure the required environment variables are provided
        if not PORT_CLIENT_ID or not PORT_CLIENT_SECRET:
            logging.error("Missing environment variables: PORT_CLIENT_ID or PORT_CLIENT_SECRET.")
            raise ValueError("Environment variables PORT_CLIENT_ID or PORT_CLIENT_SECRET are not set")

        logging.info("Environment variables loaded successfully.")

        # Construct the credentials and make the request
        credentials = {'clientId': PORT_CLIENT_ID, 'clientSecret': PORT_CLIENT_SECRET}
        logging.info("Sending authentication request to obtain access token...")

        token_response = requests.post(f'{PORT_API_URL}/auth/access_token', json=credentials)

        # Check the status code of the response
        if token_response.status_code != 200:
            logging.error(
                f"Failed to obtain access token. Status code: {token_response.status_code}. Response: {token_response.text}")
            token_response.raise_for_status()  # Raise an HTTP error if the response code is not 200

        # Parse the JSON to extract the access token
        access_token = token_response.json().get('accessToken')

        # Check if the access token was properly retrieved
        if not access_token:
            logging.error("Access token not found in the response.")
            raise ValueError("Access token not present in the API response.")

        logging.info("Access token successfully retrieved.")
        return access_token

    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException occurred while fetching the access token: {str(e)}")
        raise  # Re-raise the exception after logging so it can be handled further up the stack

    except ValueError as ve:
        logging.error(f"ValueError: {str(ve)}")
        raise  # Re-raise the exception after logging

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise  # Re-raise the general exception after logging

