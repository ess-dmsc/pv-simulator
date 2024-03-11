from confluent_kafka import KafkaException, Producer


class ProducerFactory:
    def __init__(self):
        pass

    def create_producer(self, config: dict) -> Producer:
        try:
            producer = Producer(config)
            return producer
        except KafkaException as e:
            print(
                f"Failed to create producer on broker {config['bootstrap.servers']}: {e}"
            )
            raise e
