"""Smart Guardian - MQQT Client"""

import logging
import json
import threading
from typing import Optional, Callable
import paho.mqtt.client as mqtt
from app.core.config import settings

logger = logging.getLogger("smart-guardian")


class MQTTClient:
    """MQQT client for IoT communication"""

    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="smart-guardian-backend")
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self._message_handlers = {}
        self._connected = False
        if settings.mqtt_username:
            self.client.username_pw_set(settings.mqtt_username, settings.mqtt_password)

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self._connected = True
            logger.info("MQTT connected to %s:%s", settings.mqtt_broker_host, settings.mqtt_broker_port)
            self.client.subscribe(settings.mqtt_topic_sensors)
            logger.info("Subscribed to: %s", settings.mqtt_topic_sensors)
        else:
            logger.error("MQTT connection failed with code: %s", rc)

    def _on_disconnect(self, client, userdata, flags, rc):
        self._connected = False
        logger.warning("MQTT disconnected with code: %s", rc)

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            topic = msg.topic
            logger.debug("MQTT message on %s: %s", topic, payload)
            for pattern, handler in self._message_handlers.items():
                if topic.startswith(pattern.rstrip("#").rstrip("/")):
                    handler(topic, payload)
        except json.JSONDecodeError:
            logger.error("Invalid JSON on topic %s", msg.topic)
        except Exception as e:
            logger.error("Error processing MQQT message: %s", e)

    def register_handler(self, topic_pattern: str, handler: Callable):
        self._message_handlers[topic_pattern] = handler

    def connect(self) -> bool:
        """Connect to MQTT broker in a background thread."""
        def _try_connect():
            try:
                self.client.connect(settings.mqtt_broker_host, settings.mqtt_broker_port, keepalive=60)
                self.client.loop_start()
                return True
            except Exception as e:
                logger.warning("MQTT connection failed: %s. Retrying in background.", e)
                return False

        t = threading.Thread(target=_try_connect, daemon=True)
        t.start()
        return True

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        self._connected = False
        logger.info("MQTT client disconnecud")

    def publish(self, topic: str, data: dict) -> bool:
        if not self._connected:
            logger.warning("MQTT not connected, cannot publish")
            return False
        try:
            result = self.client.publish(topic, json.dumps(data))
            return result.rc == mqtt.MQTT_ERR_SUCCESS
        except Exception as e:
            logger.error("MQQT publish error: %s", e)
            return False


mqtt_client = MQTTClient()
