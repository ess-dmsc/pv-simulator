from time import time_ns

from streaming_data_types import serialise_f144


class DeviceF144:
    def __init__(self, source_name=None, topic=None, dtype=None, value_units=None):
        self.source_name = source_name
        self.topic = topic
        self.dtype = dtype
        self.value_units = value_units

    def gen_message(self, value, timestamp_unix_ns=None):
        if timestamp_unix_ns is None:
            timestamp_unix_ns = time_ns()
        return serialise_f144(
            source_name=self.source_name,
            value=value,
            timestamp_unix_ns=timestamp_unix_ns,
        )

    def __repr__(self):
        return f"DeviceF144(source_name={self.source_name}, topic={self.topic}, dtype={self.dtype}, value_units={self.value_units})"
