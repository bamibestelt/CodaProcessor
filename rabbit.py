from typing import List

import pika

from constant import RABBIT_HOST, CODA_REQUEST_QUEUE, CODA_REPLY_QUEUE
from http_task import fetch_coda_links


def start_listen_request_queue():
    # need to add broker credentials
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=CODA_REQUEST_QUEUE)
    channel.basic_consume(queue=CODA_REQUEST_QUEUE, on_message_callback=listen_to_queue, auto_ack=True)
    print('Listening to request. To exit press CTRL+C')
    channel.start_consuming()


def listen_to_queue(channel, method, properties, body):
    print(f"Received command to process Coda links")
    channel.stop_consuming()
    links = fetch_coda_links()
    send_coda_links_queue(links)


def send_coda_links_queue(links: List[str]):
    # need to add broker credentials
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=CODA_REPLY_QUEUE)
    channel.basic_publish(exchange='', routing_key=CODA_REPLY_QUEUE, body=links)
    print(f"Coda links size {len(links)} sent!")
    connection.close()
