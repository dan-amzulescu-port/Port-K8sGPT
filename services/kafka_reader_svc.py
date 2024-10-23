import os
import json
import logging
from typing import Dict, Any

from confluent_kafka import Consumer, KafkaError

from services.k8sgpt_svc import get_k8sgpt_insights
from services.update_port_svc import update_port
from constants import BOOTSTRAP_SERVERS, AUTO_OFFSET_RESET, SECURITY_PROTOCOL, SASL_MECHANISMS, MSG_TYPE, K8SGPT_TYPE

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')

def create_consumer_config() -> Dict[str, Any]:
    SASL_USERNAME = os.getenv("SASL_USERNAME")
    SASL_PASSWORD = os.getenv("SASL_PASSWORD")
    GROUP_ID = os.getenv("GROUP_ID")
    consumer_config =  {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': GROUP_ID,
        'auto.offset.reset': AUTO_OFFSET_RESET,
        'security.protocol': SECURITY_PROTOCOL,
        'sasl.mechanisms': SASL_MECHANISMS,
        'sasl.username':  SASL_USERNAME,
        'sasl.password': SASL_PASSWORD,
        'enable.auto.commit': False,
    }
    return consumer_config


def handle_kafka_error(msg):
    if msg.error().code() == KafkaError._PARTITION_EOF:
        logging.info(f"Reached end of partition for topic {msg.topic()} [{msg.partition()}]")
    else:
        logging.error(f"Kafka error: {msg.error()}")

def consume_messages(consumer: Consumer, topic: str):
    consumer.subscribe([topic])
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Wait for message or event/error

            if msg is None:
                continue
            if msg.error():
                handle_kafka_error(msg)
                continue
            try:
                process_message(consumer, msg)
            except json.JSONDecodeError:
                logging.error("Failed to parse message as JSON")

    except KeyboardInterrupt:
        logging.info("Interrupted by user, shutting down...")
    finally:
        consumer.close()


def process_message(consumer: Consumer, msg):
    message_data = json.loads(msg.value().decode('utf-8'))

    logging.info(f"Processing message: {message_data}")

    if MSG_TYPE in message_data and message_data[MSG_TYPE] == K8SGPT_TYPE:
        entity_identifier = message_data.get("entity_identifier")

        # If entity is not healthy, fetch k8sGPT insights
        if message_data.get("entity_health") != "Healthy":
            k8sgpt_insights = get_k8sgpt_insights(
                message_data["name"],
                message_data["namespace"]
            )
            update_port(entity_identifier, k8sgpt_insights)
            # logging.DEBUG(f"K8sGPT insights: {k8sgpt_insights}")
        else:
            update_port(entity_identifier)
            # Manually commit offset after processing the message
            consumer.commit(message=msg)
