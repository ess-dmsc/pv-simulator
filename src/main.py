import argparse
import json
import logging
import os
import sys
import time

from p4p.client.thread import Context

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.config_from_json import build_config
from src.module_f144 import DeviceF144
from src.pv_factory import PVFactory
from src.pva_server import EpicsPVAServer
from src.run_thread import EpicsThreadF144

logger = logging.getLogger(__name__)

context = Context("pva")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Fill this out later.")

    parser.add_argument(
        "-j", "--json", required=True, help="The path to the json file."
    )

    parser.add_argument(
        "-t", "--target-path", required=True, help="The path to the target json file."
    )

    parser.add_argument(
        "-c", "--config", required=False, help="The path to the config file."
    )

    parser.add_argument(
        "-l",
        "--log_level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level.",
    )

    return parser.parse_args()


def configure_logging(level):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    logging.basicConfig(level=numeric_level)


def read_config(path):
    with open(path, "r") as f:
        return json.load(f)


def main():
    args = parse_arguments()

    configure_logging(args.log_level)

    with open(args.json, "r") as file:
        json_data = json.load(file)

    dev_config = build_config(json_data)

    pv_factory = PVFactory(dev_config)
    devices = pv_factory.get_devices()

    if args.config is not None:
        with open(args.config, "r") as file:
            server_config = json.load(file)
    else:
        server_config = {}

    server = EpicsPVAServer(
        devices=devices, gateway_config=server_config, target_config_path=args.target_path,
    )
    server.start()

    target_config = read_config(args.target_path)

    threads = [
        EpicsThreadF144(
            dev, context=context, config=target_config.get(dev.source_name, None)
        )
        for dev in devices.values()
        if isinstance(dev, DeviceF144)
    ]

    for thread in threads:
        thread.start()


    logger.info("EPICS PVA server started")
    logger.info(f"Configuration for server: {server.get_context().conf()}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for thread in threads:
            thread.stop()
        server.join()


if __name__ == "__main__":
    main()
