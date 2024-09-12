import os

from confluent_kafka import Consumer
from dotenv import load_dotenv
from SVC.kafka_reader_svc import create_consumer_config, consume_messages


def main():
    load_dotenv(dotenv_path=".env", override=True, encoding="utf-8")
    config = create_consumer_config()
    consumer = Consumer(config)
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
    consume_messages(consumer, KAFKA_TOPIC)

if __name__ == "__main__":
    main()