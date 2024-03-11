import logging
import threading
import time

import numpy as np

logger = logging.getLogger(__name__)


class RunThread:
    def __init__(self, update_period=1., *args, **kwargs):
        self.update_period = update_period
        self.thread = None
        self._run_event = threading.Event()

    def start(self):
        self._run_event.set()
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def stop(self):
        self._run_event.clear()
        if self.thread is not None:
            if self.thread.is_alive():
                self.thread.join()
                self.thread = None

    def set_update_period(self, update_period):
        if update_period < 0.01:
            logger.warning(f"Received update period: {update_period}")
            logger.warning("Update period is too low, setting to 0.01")
            update_period = 0.01
        logger.debug(f"Setting update period to {update_period}")
        self.update_period = update_period

    def is_alive(self):
        return self.thread.is_alive() if self.thread is not None else False

    def _run(self):
        while self._run_event.is_set():
            self._inner_run()
            time.sleep(self.update_period)
        return True

    def _inner_run(self):
        raise NotImplementedError("Subclasses must implement _inner_run method")


class KafkaThreadF144(RunThread):
    def __init__(self, device, producer, config=None, update_period=1):
        super().__init__(update_period=update_period)
        self.device = device
        self.config = config
        self.producer = producer
        self.value = None
        self.std_dev = None
        if config is not None:
            self.set_config(config)

    def set_config(self, config):
        self.config = config
        self.value = config.get("target_value", None)
        self.std_dev = config.get("std_dev", None)

    def _inner_run(self):
        if self.std_dev is None:
            value = self.value
        else:
            value = self.value + np.random.normal(0, self.std_dev)
        f144_msg = self.device.gen_message(value)
        self.producer.produce(self.device.topic, f144_msg)
        self.producer.flush()
        logger.debug(
            f"Produced message with value: {value} to topic: {self.device.topic}"
        )


class EpicsThreadF144(RunThread):
    def __init__(self, device, context, config=None, update_period=1):
        super().__init__(update_period=update_period)
        self.device = device
        self.context = context
        self.config = config
        self.pv_name = device.source_name
        self.value = None
        self.std_dev = None
        if config is not None:
            self.set_config(config)

    def set_config(self, config):
        self.config = config
        self.value = config.get("target_value", None)
        self.std_dev = config.get("std_dev", None)

        update_period = config.get("update_period", None)
        if update_period is not None:
            logger.info(f"Setting custom update period to {update_period}")
            self.set_update_period(update_period)

    def _inner_run(self):
        if self.value is None:
            logger.debug(f"Skipping PV {self.pv_name} update, no target value in config")
            return

        if self.std_dev is None:
            value = self.value
        else:
            value = self.value + np.random.normal(0, self.std_dev)

        try:
            self.context.put(self.pv_name, value)
            logger.debug(f"Updated PV {self.pv_name} with value: {value}")
        except Exception as e:
            logger.error(f"Failed to update PV {self.pv_name} with value {value}: {e}")


if __name__ == "__main__":
    from src.module_f144 import DeviceF144
    from tests.doubles.producer import ProducerSpy

    device = DeviceF144(
        source_name="some_source",
        topic="some_topic",
        dtype="doubles",
        value_units="mm",
    )

    config = {
        "target_value": 1,
        "std_dev": 0.1,
    }

    thread = KafkaThreadF144(device, ProducerSpy({}), config=config)
    thread.start()
    print(thread.is_alive())

    time.sleep(1)
    thread.stop()
