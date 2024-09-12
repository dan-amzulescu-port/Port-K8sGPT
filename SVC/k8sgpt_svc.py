import json
import logging
import requests

from SVC.pretify_svc import prettify_markdown
from constants import K8SGPT_URL, BACKEND_LLM


def get_k8sgpt_insights(k8sgpt_workload_name:str, k8sgpt_namespace:str) -> str:
    params = {
        "explain": "true",
        "backend": BACKEND_LLM,
        "namespace": k8sgpt_namespace
    }

    response = requests.post(K8SGPT_URL, params=params)
    if response.status_code != 200:
        logging.error(f"Error fetching K8sGPT: {response.status_code}")
        return ""

    json_data = json.loads(response.content.decode('utf-8'))
    k8s_insights = ""
    if json_data['problems'] is not None:
        for result in json_data['results']:
            if result['name'].split('/')[1].startswith(k8sgpt_workload_name):
                k8s_insights += "\n".join(result['details'].splitlines())+'\n'
                k8s_insights = prettify_markdown(k8s_insights)
    return k8s_insights
