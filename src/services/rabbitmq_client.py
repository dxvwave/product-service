import aio_pika
import json

from core.config import settings


class RabbitClient:
    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            "product_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def _publish_event(
        self,
        routing_key: str,
        message: dict,
        delivery_mode: aio_pika.DeliveryMode = aio_pika.DeliveryMode.PERSISTENT,
    ):
        await self.exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=delivery_mode,
                content_type="application/json"
            ),
            routing_key=routing_key,
        )

    async def publish_product_created(self, product: dict):
        await self._publish_event("product.created", product)

    async def publish_product_price_changed(self, product: dict):
        await self._publish_event("product.price_changed", product)


rabbit_client = RabbitClient(settings.rabbitmq_url)
