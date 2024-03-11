from src.module_f144 import DeviceF144
from src.module_tdct import DeviceTDCT


class PVFactory:
    def __init__(self, config):
        self.config = config
        self.devices = self._load_devices()

    def _load_devices(self):
        devices = {}
        for path, details in self.config.items():
            class_name = f"Device{details['module'].upper()}"
            try:
                device_class = globals()[class_name]
                devices[path] = device_class(
                    details["source"],
                    details["topic"],
                    details["dtype"],
                    details["value_units"],
                )
            except KeyError:
                print(f"Unknown device class: {class_name}")
        return devices

    def get_devices(self):
        return self.devices


if __name__ == "__main__":
    import json

    from src.config_from_json import build_config

    test_json_path = "/home/jonas/code/nexus-json-templates/odin/odin.json"
    with open(test_json_path, "r") as file:
        json_data = json.load(file)

    config = build_config(json_data)

    pv_factory = PVFactory(config)
    devices = pv_factory.get_devices()

    for device in devices.values():
        print(device)
