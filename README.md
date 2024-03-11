# EPICS PVA Simulator

## Overview

This project is designed to simulate and monitor Process Variables (PVs) within an EPICS environment using Python and the P4P library. It provides a framework for configuring and simulating PVs.
The system is configurable through JSON files, allowing for customization of device behaviors and some PVA server settings.


### Concept

The idea of the program is to read the NeXus JSON and from that be able to extract all f144 modules (potentially other modules) 
and create PVs for them. The PVs will then be added to the `INSTRUMENT_targets.json` file if they are missing and in that file 
you can configure the target value, noise and update period for each PV. The program will then simulate the PVs based on the
configuration in the `INSTRUMENT_targets.json` file. 

This should make it easy to simulate PVs for testing and development purposes.


## WARNING

### Do not use this if the real PVs are in use. It might cause confusion and/or damage to the system!


## Features

- **PV Simulation:** Dynamically simulate PV behaviors based on configurable JSON templates.
- **PV Monitoring:** Includes a listener utility debugging.
- **JSON Configuration:** JSON files for easy and flexible configuration of PV target values, gaussian noise and update periods.

## Getting Started

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/ess-dmsc/pv-simulator.git
cd pv-simulator
```

2. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

It is recommended to use a virtual environment to manage the dependencies.

### Configuration Files

You will need three main configuration files in JSON format:

- **Simulation Configuration (`INSTRUMENT.json`):** The normal NeXus JSON. The program will extract all the source_names and create PVs for them and if they are missing from the `INSTRUMENT_targets.json` file, they will be added there.
- **Target Configuration (`INSTRUMENT_targets.json`):** Specifies target configurations for simulated PVs. You can specify the target value, noise, and update period for each PV.
- **Server Configuration (`server_config.json`):** Contains settings for the EPICS PVA server, mostly the pva address list.

The first time you run the program, it will create a config file if it does not exist. You can then edit the file to match your setup. You have to restart the program for the changes to take effect.

#### Server Configuration Example

```json
{
   "EPICS_PVA_AUTO_ADDR_LIST": "NO",
   "EPICS_PVA_ADDR_LIST": "10.102.10.255 10.140.1.255"
}
```

Replace these placeholders with your actual configurations based on your project's requirements.

### Running the Simulation

To start the simulation and monitoring system, use the following command:

```bash
python src/main.py --json "/path/to/your/odin.json" -t "/path/to/your/odin_targets.json" -c "/path/to/your/server_config.json" -l INFO
```

For monitoring PVs with the provided listener utility, ensure you have configured it to match your target setup. It's currently hardcoded in the `listener.py` file. Then run the listener with the following command:

```bash
python src/listener.py
```

## TODO

- [ ] Add support for other modules than f144. (TDCT, se00)
- [ ] Add proper filtering for the source_names to make sure there are no duplicates.
- [ ] Add online checks for the PVs to make sure they are not already in use, kill the thread if they are.
- [ ] Add a simple filter configuration for the PVs to make it easier to filter out already deployed real PVs.