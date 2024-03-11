import pytest
import time

from streaming_data_types import deserialise_f144

from tests.doubles.producer import ProducerSpy

from src.run_thread import KafkaThreadF144
from src.module_f144 import DeviceF144


@pytest.fixture
def thread_f144():
    device = DeviceF144(
        source_name="some_source",
        topic="some_topic",
        dtype="doubles",
        value_units="mm",
    )

    producer = ProducerSpy({})

    config = {
        "target_value": 1,
        "std_dev": None,
    }

    thread = KafkaThreadF144(device, producer, config=config, update_period=0.01)

    yield thread, producer

    thread.stop()


def test_can_init_thread(thread_f144):
    thread, producer = thread_f144

    assert thread.device.source_name == "some_source"
    assert thread.device.topic == "some_topic"
    assert thread.device.dtype == "doubles"
    assert thread.device.value_units == "mm"
    assert thread.producer == producer
    assert thread.is_alive() is False
    assert thread.thread is None
    assert thread.update_period == 0.01


def test_can_start_thread(thread_f144):
    thread, producer = thread_f144

    thread.start()

    assert thread.is_alive() is True
    assert thread.thread is not None


def test_can_stop_thread(thread_f144):
    thread, producer = thread_f144

    thread.start()
    time.sleep(0.01)
    thread.stop()

    assert thread.is_alive() is False
    assert thread.thread is None


def test_can_run_thread(thread_f144):
    thread, producer = thread_f144

    expected_last_value = 1.0
    start_ts = time.time_ns()

    thread.start()
    time.sleep(0.1)
    thread.stop()

    end_ts = time.time_ns()

    last_msg = producer.data[-1]
    topic = last_msg['topic']
    deserialised_msg = deserialise_f144(last_msg['value'])
    source_name = deserialised_msg.source_name
    value = deserialised_msg.value
    timestamp = deserialised_msg.timestamp_unix_ns

    assert topic == "some_topic"
    assert source_name == "some_source"
    assert value == expected_last_value
    assert start_ts <= timestamp <= end_ts


