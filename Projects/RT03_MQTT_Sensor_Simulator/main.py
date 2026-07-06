"""MQTT Sensor Simulator: publishes fake sensor readings to a broker or writes to local JSON for demo."""
import argparse
import json
from pathlib import Path
import random
import time

try:
    import paho.mqtt.client as mqtt
except Exception:
    mqtt = None


def demo_publish(path: Path):
    readings = []
    for i in range(3):
        r = {"sensor_id": i + 1, "value": round(random.uniform(20, 30), 2), "ts": int(time.time())}
        readings.append(r)
    path.write_text(json.dumps(readings, indent=2), encoding='utf-8')
    print(f'Wrote {path}')


def publish_to_broker(broker, topic):
    if mqtt is None:
        print('paho-mqtt not installed')
        return
    client = mqtt.Client()
    client.connect(broker, 1883, 60)
    for i in range(3):
        payload = json.dumps({"sensor": i+1, "value": round(random.uniform(20,30),2)})
        client.publish(topic, payload)
        print('Published', payload)
    client.disconnect()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--broker', default=None, help='MQTT broker host')
    parser.add_argument('--topic', default='sensors/demo')
    args = parser.parse_args()

    out = Path(__file__).parent / 'simulated_sensor.json'
    if args.demo and not args.broker:
        demo_publish(out)
    elif args.broker:
        publish_to_broker(args.broker, args.topic)
    else:
        print('Run with --demo or provide --broker HOST to publish to a broker')


if __name__ == '__main__':
    main()
