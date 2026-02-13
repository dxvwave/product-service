import logging
import aio_pika
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)

from services.rabbitmq_client import rabbit_client

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((ConnectionError, aio_pika.exceptions.AMQPConnectionError)),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
async def connect_to_rabbitmq():
    """Connect to RabbitMQ server."""
    await rabbit_client.connect()
