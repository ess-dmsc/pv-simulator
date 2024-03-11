import logging

import numpy as np
import pytest
import time

from src.run_thread import RunThread
from src.module_f144 import DeviceF144


logger = logging.getLogger(__name__)


class TestThreadF144(RunThread):
    def __init__(self, device, config, update_period=1.):
        super().__init__(update_period=update_period)
        self.device = device
        self.config = config
        self.run_data = []
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
            self.set_update_period(update_period)

    def _inner_run(self):
        if self.value is None:
            return
        if self.std_dev is None:
            value = self.value
        else:
            value = self.value + np.random.normal(0, self.std_dev)
        self.run_data.append(value)


@pytest.fixture
def thread_f144():
    device = DeviceF144(
        source_name="some_source",
        topic="some_topic",
        dtype="doubles",
        value_units="mm",
    )

    config = {
        "target_value": 1,
        "std_dev": None,
    }

    thread = TestThreadF144(device, config=config, update_period=0.01)

    yield thread

    thread.stop()


def test_can_init_thread(thread_f144):
    thread = thread_f144

    assert thread.device.source_name == "some_source"
    assert thread.device.topic == "some_topic"
    assert thread.device.dtype == "doubles"
    assert thread.device.value_units == "mm"
    assert thread.is_alive() is False
    assert thread.thread is None
    assert thread.update_period == 0.01


def test_can_start_thread(thread_f144):
    thread = thread_f144

    thread.start()

    assert thread.is_alive() is True
    assert thread.thread is not None


def test_can_stop_thread(thread_f144):
    thread = thread_f144

    thread.start()
    time.sleep(0.01)
    thread.stop()

    assert thread.is_alive() is False
    assert thread.thread is None


def test_can_run_thread(thread_f144):
    thread = thread_f144

    expected_last_value = 1.0

    thread.start()
    time.sleep(0.1)
    thread.stop()

    assert len(thread.run_data) > 0
    last_value = thread.run_data[-1]
    assert last_value == expected_last_value


def test_set_update_period_too_low(thread_f144):
    thread = thread_f144

    thread.set_update_period(0.0001)

    assert thread.update_period == 0.01


def test_set_update_period(thread_f144):
    thread = thread_f144

    thread.set_update_period(0.1)

    assert thread.update_period == 0.1
