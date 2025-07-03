import paho.mqtt.client as mqtt
import json
import base64

# Configuration
TTN_REGION = "nam1"  # nam1 for North America
APP_ID = "test-dal"
DEVICE_ID = "eui-DEVEUI" # Replace with your device EUI
USERNAME = f"{APP_ID}@ttn"
PASSWORD = "XXXX" # Replace with your TTN API key

# MQTT settings
MQTT_HOST = f"{TTN_REGION}.cloud.thethings.network"
MQTT_PORT = 8883  # Secure MQTT
MQTT_TOPIC = f"v3/{APP_ID}@ttn/devices/{DEVICE_ID}/up"

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to TTN MQTT broker")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Subscribed to: {MQTT_TOPIC}")
    else:
        print(f"❌ Connection failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"\n📨 Message received on topic: {msg.topic}")
    payload = json.loads(msg.payload.decode("utf-8"))
    
    frm_payload = payload["uplink_message"].get("frm_payload", "")
    decoded_bytes = base64.b64decode(frm_payload)
    try:
        decoded_str = decoded_bytes.decode("utf-8")
    except UnicodeDecodeError:
        decoded_str = str(decoded_bytes)

    print(f"📦 Base64 Payload: {frm_payload}")
    print(f"🔓 Decoded Payload: {decoded_str}")
    print("📊 Full JSON Payload:")
    print(json.dumps(payload, indent=2))

# Set up client
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set()  # Enables TLS

# Connect and loop
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()
