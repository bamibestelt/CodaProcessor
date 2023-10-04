import os
from dotenv import load_dotenv

load_dotenv()

RABBIT_HOST = os.environ.get('RABBIT_HOST')
CODA_REQUEST_QUEUE = os.environ.get('CODA_REQUEST_QUEUE')
CODA_REPLY_QUEUE = os.environ.get('CODA_REPLY_QUEUE')

CODA_API_TOKEN = os.environ.get('CODA_API_TOKEN')
CODA_BASE_URL = os.environ.get('CODA_BASE_URL')
