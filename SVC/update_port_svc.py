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
    PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
    PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")
    credentials = {'clientId': PORT_CLIENT_ID, 'clientSecret': PORT_CLIENT_SECRET}

    token_response = requests.post(f'{PORT_API_URL}/auth/access_token', json=credentials)
    access_token = token_response.json()['accessToken']
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

