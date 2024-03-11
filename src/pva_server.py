import json
import logging
import os
import threading
import time

from p4p import Value
from p4p.server import Server
from p4p.server.thread import SharedPV

from src.pv_types import DTYPE_MAP, INITIAL_VALUES

logger = logging.getLogger(__name__)


class EpicsPVAServer(threading.Thread):
    def __init__(self, devices, gateway_config, target_config_path=None):
        super().__init__()
        self.devices = devices
        self.gateway_config = gateway_config
        self.target_config_path = target_config_path
        self.provider = None
        self.pvs = {}
        self.context = None

    def run(self):
        config = self.read_config()

        self.pvs = {}
        for device in self.devices.values():
            if device.dtype in DTYPE_MAP:
                initial_structure = {
                    "value": config[device.source_name]["target_value"]
                    if config.get(device.source_name, {}).get("target_value", None) is not None
                    else INITIAL_VALUES[device.dtype],
                    "timeStamp": {
                        "secondsPastEpoch": time.time(),
                        "nanoseconds": time.time_ns() - int(time.time()) * 1e9,
                        "userTag": 0,
                    },
                }
                handler = self.PVHandler(device)
                self.pvs[device.source_name] = SharedPV(
                    initial=Value(DTYPE_MAP[device.dtype], initial_structure),
                    handler=handler,
                )
                handler.set_pv(self.pvs[device.source_name])

        self.update_config()

        self.provider = {pv_name: self.pvs[pv_name] for pv_name in self.pvs}

        self.context = Server(providers=[self.provider], conf=self.gateway_config)

    def get_context(self):
        return self.context

    def read_config(self):
        if self.target_config_path is None:
            logger.warning("No target config path provided, skipping read")
            return {}

        if not os.path.exists(self.target_config_path):
            logger.warning(f"Target config path {self.target_config_path} does not exist, creating empty file")
            with open(self.target_config_path, "w") as file:
                json.dump({}, file, indent=2)

        with open(self.target_config_path, "r") as file:
            config = json.load(file)
        return config

    def update_config(self):
        if self.target_config_path is None:
            logger.warning("No target config path provided, skipping update")

        if not os.path.exists(self.target_config_path):
            logger.warning(f"Target config path {self.target_config_path} does not exist, creating empty file")
            with open(self.target_config_path, "w") as file:
                json.dump({}, file, indent=2)

        with open(self.target_config_path, "r") as file:
            config = json.load(file)

        for pv_name in self.pvs.keys():
            if pv_name not in config:
                config[pv_name] = {
                    "target_value": None,
                    "std_dev": None,
                }

        with open(self.target_config_path, "w") as file:
            json.dump(config, file, indent=2)

    def stop(self):
        if self.context:
            self.context.stop()
            self.context = None

    class PVHandler:
        def __init__(self, device):
            self.device = device
            self.pv = None

        def set_pv(self, pv):
            self.pv = pv

        def put(self, pv_name, op):
            new_value = op.value()
            new_value["timeStamp"] = {
                "secondsPastEpoch": time.time(),
                "nanoseconds": time.time_ns() - int(time.time()) * 1e9,
                "userTag": 0,
            }
            self.pv.post(new_value)
            op.done()

    def get_context(self):
        return self.context


if __name__ == "__main__":
    from p4p.client.thread import Context

    from src.config_from_json import build_config
    from src.pv_factory import PVFactory

    # Load your configuration and initialize devices
    json_path = "/home/jonas/code/nexus-json-templates/odin/odin.json"
    with open(json_path, "r") as file:
        json_data = json.load(file)
    config = build_config(json_data)
    pv_factory = PVFactory(config)
    devices = pv_factory.get_devices()

    # Define gateway configuration, for example, which networks to broadcast on
    gateway_config = {
        # 'EPICS_PVAS_INTF_ADDR_LIST': 'xxx.xxx.xxx.xxx',
        # 'EPICS_PVAS_BEACON_ADDR_LIST': 'xxx.xxx.xxx.xxx',
        # More gateway configuration as needed
    }

    # Initialize and start the EPICS PVA server
    server = EpicsPVAServer(devices, gateway_config)
    server.start()

    time.sleep(1)

    values = {}

    with Context("pva") as context:
        for pv_name in server.pvs.keys():
            try:
                value = context.get(pv_name)
                values[pv_name] = value
                print(f"PV {pv_name}: {value}")
            except Exception as e:
                print(f"Error reading PV {pv_name}: {e}")

    with Context("pva") as context:
        for pv_name in server.pvs.keys():
            try:
                context.put(pv_name, values=values[pv_name] + 100)
                # print(f"Updated PV {pv_name} with value: {values[pv_name] + 1}")
            except Exception as e:
                print(f"Error writing PV {pv_name}: {e}")

    with Context("pva") as context:
        for pv_name in server.pvs.keys():
            try:
                value = context.get(pv_name)
                print(f"PV {pv_name}: {value}")
            except Exception as e:
                print(f"Error reading PV {pv_name}: {e}")

    time.sleep(1)

    server.join()  # Wait for the server thread to finish

