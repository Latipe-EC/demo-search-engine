# rabbitmq_consumer.py
import json
from enum import Enum

import pika

from config.variable import PRODUCT_UPDATES_QUEUE, RABBITMQ_HOST, PRODUCT_EXCHANGE, \
    PRODUCT_ROUTING_KEY
from database.trained_repos import trained_find_by_productId, delete_trained_product
from database.untrained_repos import untrained_insert_new_product, untrained_delete_by_productId
from domain.dto import ResponseErrorModel


class Action(Enum):
    CREATE = "c"
    UPDATE = "u"
    DELETE = "d"


def setup_rabbitmq_consumer():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()

        # Declare queues for product updates and scheduled tasks
        channel.queue_declare(queue=PRODUCT_UPDATES_QUEUE)

        # Declare exchanges
        channel.exchange_declare(exchange=PRODUCT_EXCHANGE, exchange_type='topic', durable=True)
        channel.basic_consume(queue=PRODUCT_UPDATES_QUEUE, on_message_callback=handle_recive_message, auto_ack=True)

        # Product updates consumer
        channel.queue_bind(exchange=PRODUCT_EXCHANGE, queue=PRODUCT_UPDATES_QUEUE, routing_key=PRODUCT_ROUTING_KEY)

        channel.start_consuming()

    except Exception as e:
        return ResponseErrorModel(
            f"Failed to connect to RabbitMQ server at {RABBITMQ_HOST}. Please check if the server is running and "
            f"the host is correct.", "Establish product queue fail.", 400)


def handle_recive_message(ch, method, properties, body):
    message = json.loads(body)

    if message['op'] == Action.CREATE.value:
        untrained_insert_new_product({
            "product_id": message['id']
        })
    elif message['op'] == Action.UPDATE.value:
        if trained_find_by_productId(message['id']):
            untrained_insert_new_product({
                "product_id": message['id'],
                "product_name": message['name'],
                "image_urls": message['images'],
            })
            delete_trained_product(message['id'])
        else:
            untrained_insert_new_product({
                "product_id": message['id']
            })
    elif message['op'] == Action.DELETE.value:
        if trained_find_by_productId(message['id']):
            untrained_delete_by_productId(message['id'])
        else:
            delete_trained_product(message['id'])
    else:
        return ResponseErrorModel("Action not found", "Action not found", 400)
