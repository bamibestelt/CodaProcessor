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
    delimiter = " "
    combined_string = delimiter.join(links)
    list_in_bytes = combined_string.encode("utf-8")
    send_coda_links_queue(list_in_bytes)
    print(f"Coda links size {len(links)} sent!")


def send_coda_links_queue(links_in_bytes: bytes):
    # need to add broker credentials
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=CODA_REPLY_QUEUE)
    channel.basic_publish(exchange='', routing_key=CODA_REPLY_QUEUE, body=links_in_bytes)
    connection.close()
