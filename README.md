# Readme


Below is an example of how to run the program


```bash
python src/main.py --json "/home/jonas/code/nexus-json-templates/odin/odin.json" -t "/home/jonas/code/pv_simulator/src/ioc_config/odin_targets.json" -c "/home/jonas/code/pv_simulator/src/ioc_config/server_config.json" -l INFO
```

To monitor the PVs created i've written a small listener, but you have to edit the file to match the instrument target configuration

```bash
python src/listener.py
```
