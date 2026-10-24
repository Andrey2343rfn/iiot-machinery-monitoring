import time
import json
import random
import argparse
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
USER = "machine_01"
PASS = "machine123"
TOPIC_BASE = "iiotequip/machinery/machine_01"

state_data = {
    "status": "RUN",
    "vibration": 1.2,
    "temperature": 45.0,
    "current": 12.5,
    "parts_count": 0,
    "alarm": False
}

def on_connect(client, userdata, flags, rc):
    client.publish(f"{TOPIC_BASE}/status", "online", qos=1, retain=True)
    client.subscribe(f"{TOPIC_BASE}/set")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        if "command" in payload:
            cmd = payload["command"]
            if cmd == "EMERGENCY_STOP":
                state_data["status"] = "FAULT"
                state_data["alarm"] = True
            elif cmd == "START":
                state_data["status"] = "RUN"
                state_data["alarm"] = False
            client.publish(f"{TOPIC_BASE}/state", json.dumps(state_data), qos=1)
    except:
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", type=str, default="normal")
    args = parser.parse_args()

    client = mqtt.Client()
    client.username_pw_set(USER, PASS)
    client.will_set(f"{TOPIC_BASE}/status", "offline", qos=1, retain=True)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    try:
        while True:
            if args.scenario == "vibration":
                state_data["vibration"] = random.uniform(5.5, 7.5)
                state_data["status"] = "FAULT"
            elif args.scenario == "temp":
                state_data["temperature"] += random.uniform(0.5, 1.5)
            else:
                state_data["vibration"] = round(random.uniform(1.0, 2.5), 2)
                state_data["temperature"] = round(random.uniform(42.0, 48.0), 2)
                state_data["current"] = round(random.uniform(10.0, 15.0), 2)
                if state_data["status"] == "RUN":
                    state_data["parts_count"] += 1

            telemetry = {
                "value": state_data["vibration"],
                "unit": "mm/s",
                "ts": int(time.time()),
                "temperature": state_data["temperature"],
                "current": state_data["current"],
                "parts": state_data["parts_count"],
                "status": state_data["status"]
            }

            client.publish(f"{TOPIC_BASE}/telemetry", json.dumps(telemetry), qos=1)
            time.sleep(5)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()