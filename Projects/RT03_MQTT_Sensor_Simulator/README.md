# MQTT Sensor Simulator (RT03)

Simulate IoT sensor readings and publish to an MQTT broker. Demo mode writes `simulated_sensor.json` locally.

## Setup
```
pip install -r requirements.txt
```

## Run (demo)
```
python main.py --demo
```

Screenshot: `screenshots/screenshot.png`
# RT03 — MQTT Sensor Simulator

Simulates sensor readings. In demo mode it writes `simulated_sensor.json`. Optionally publishes to an MQTT broker if `--broker` is provided.

Demo:

```bash
python main.py --demo
```

Publish to broker:

```bash
python main.py --broker test.mosquitto.org --topic sensors/demo
```

Requirements:

```bash
pip install paho-mqtt
```

Screenshots: `screenshots/screenshot.png`
