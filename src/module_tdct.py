from streaming_data_types import serialise_tdct


class DeviceTDCT:
    def __init__(self, source_name=None, topic=None, dtype=None, value_units=None):
        self.source_name = source_name
        self.topic = topic
        self.dtype = dtype
        self.value_units = value_units
        self._counter = 0

    def gen_message(self, values):
        self._counter += 1
        return serialise_tdct(
            name=self.source_name, timestamps=values, sequence_counter=self._counter
        )

    def __repr__(self):
        return f"DeviceTDCT(source_name={self.source_name}, topic={self.topic}, dtype={self.dtype}, value_units={self.value_units})"
