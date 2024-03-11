import json
import os
import time

from p4p.client.thread import Context


def pv_callback(pv_name):
    """
    Creates a callback function for a specific PV.

    :param pv_name: The name of the PV.
    :return: A callback function that prints the PV's new values and timestamps.
    """

    def callback(monitor):
        # Extract the value and timestamp from the monitor update
        raw_data = monitor.raw
        value = raw_data["value"]
        seconds_past_epoch = raw_data["timeStamp"]["secondsPastEpoch"]
        nanoseconds = raw_data["timeStamp"]["nanoseconds"]
        print(
            f"PV: {pv_name:<50} | val: {str(round(value,3)):<20} | Timestamp: {seconds_past_epoch}.{nanoseconds} seconds past epoch"
        )
        # print(f"PV: {pv_name} | Value: {value} | Timestamp: {seconds_past_epoch}.{nanoseconds} seconds past epoch")

    return callback


def main(config_path):
    """
    Monitors all PVs defined in the JSON config file.

    :param config_path: Path to the JSON config file.
    """
    # Load the JSON config file
    with open(config_path, "r") as file:
        config = json.load(file)

    # Create a p4p context for monitoring
    with Context("pva") as context:
        monitors = []
        # Set up a monitor for each PV in the config
        for pv_name in config.keys():
            print(f"Monitoring PV: {pv_name}")
            # The callback function is specific to each PV
            callback = pv_callback(pv_name)
            # Start monitoring the PV
            monitor = context.monitor(pv_name, callback)
            monitors.append(monitor)

        # Keep the script running to continue monitoring
        try:
            while True:
                # The monitors are active in this loop, receiving updates.
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping PV monitoring...")


if __name__ == "__main__":
    current_path = os.path.dirname(__file__)
    config_path = os.path.join(current_path, "ioc_config", "odin_targets.json")
    main(config_path)
