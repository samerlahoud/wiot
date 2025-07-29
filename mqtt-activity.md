# 🏗️ Classroom MQTT Activity: Publish, Subscribe, and Explore

**Broker:**
- URL: `broker.hivemq.com`
- Port: `1883` (TCP)
- Authentication: None required

---

## 🔧 Setup: Install Mosquitto Command-Line Tools

Install **Mosquitto clients** on your computer:

### Windows:
- Download: [https://mosquitto.org/download/](https://mosquitto.org/download/)
- During installation, select **"Install command-line clients"**.

### macOS (Homebrew):
```bash
brew install mosquitto
````

### Linux (Debian/Ubuntu):

```bash
sudo apt update
sudo apt install mosquitto-clients
```

Verify installation:

```bash
mosquitto_pub --help
mosquitto_sub --help
```

---

## 🔑 Personalized Topics

Each student or group uses **their name** in the topic to keep messages organized.

Format:

```
wiot/<yourname>/...
```

Example:

* Student 1 (Alice): `wiot/alice/temp`
* Student 2 (Bob): `wiot/bob/status`

---

## 🖼️ Publisher-Subscriber Diagram (Plain Text)

```
[ Student 1 (Publisher) ] ---> ( Publishes to topic ) ---> [ MQTT Broker ] ---> ( Forwards ) ---> [ Student 2 (Subscriber) ]
```

All messages pass through the **MQTT Broker**. The publisher does not send directly to the subscriber.

---

## Phase 1: Basic Publish/Subscribe

1. **Student 2 (Subscriber):**

   ```bash
   mosquitto_sub -h broker.hivemq.com -t wiot/alice/basic -v
   ```
2. **Student 1 (Publisher):**

   ```bash
   mosquitto_pub -h broker.hivemq.com -t wiot/alice/basic -m "Hello MQTT World!"
   ```

### ✅ Observation:

* The subscriber sees the message instantly after it is published.
* Communication is asynchronous: Publisher and Subscriber are decoupled.

### 📝 Questions:

* Did Student 2 receive the message without delay?
* What happens if the publisher sends multiple messages quickly?
* Does the publisher know if anyone received its message?

---

## Phase 2: Topics and Wildcards

1. **Publisher (Alice):**

   ```bash
   mosquitto_pub -h broker.hivemq.com -t wiot/alice/sensor1/temp -m "22.5°C"
   mosquitto_pub -h broker.hivemq.com -t wiot/alice/sensor2/temp -m "23.1°C"
   mosquitto_pub -h broker.hivemq.com -t wiot/alice/sensor2/humidity -m "45%"
   ```
2. **Subscriber (Bob):**

   ```bash
   mosquitto_sub -h broker.hivemq.com -t wiot/alice/sensor1/# -v
   mosquitto_sub -h broker.hivemq.com -t wiot/alice/+/temp -v
   mosquitto_sub -h broker.hivemq.com -t wiot/alice/# -v
   ```

### ✅ Observation:

* `+` matches one level (e.g., any `sensorX/temp`).
* `#` matches all deeper levels, including multiple devices.

### 📝 Questions:

* What messages did you see with `wiot/alice/+/temp`?
* What extra messages appeared with `wiot/alice/#`?
* How would wildcards help in managing many sensors?

---

## Phase 3: Retained Messages

1. **Publisher (Alice):**

   ```bash
   mosquitto_pub -h broker.hivemq.com -t wiot/alice/status -m "System OK" -r
   ```
2. **Subscriber (Bob):**

   ```bash
   mosquitto_sub -h broker.hivemq.com -t wiot/alice/status -v
   ```

### ✅ Observation:

* The subscriber receives the "System OK" message immediately, even if published earlier.

3. **Publisher updates retained value:**

   ```bash
   mosquitto_pub -h broker.hivemq.com -t wiot/alice/status -m "Warning: High Temp" -r
   ```

### 📝 Questions:

* What happens if a new subscriber joins after the retained message was published?
* How is this feature useful for dashboards or monitoring?

---

## Phase 4: Quality of Service (QoS)

1. **Subscriber (Bob):**

   ```bash
   mosquitto_sub -h broker.hivemq.com -t wiot/alice/qos -q 1 -v
   ```
2. **Publisher (Alice):**

   ```bash
   mosquitto_pub -h broker.hivemq.com -t wiot/alice/qos -m "Test QoS 0" -q 0
   mosquitto_pub -h broker.hivemq.com -t wiot/alice/qos -m "Test QoS 1" -q 1
   ```

### ✅ Observation:

* QoS 0: "Fire-and-forget" (no confirmation).
* QoS 1: Delivery is confirmed and retried if needed.

### 📝 Questions:

* Did you notice any visible difference in message behavior?
* In what IoT scenarios would QoS 1 or QoS 2 be preferred?

---

## Phase 5: Last Will and Testament (LWT)

**Goal:** Detect when a publisher disconnects unexpectedly.

1. **Subscriber (Bob):**

   ```bash
   mosquitto_sub -h broker.hivemq.com -t wiot/alice/device1/status -v
   ```

2. **Publisher (Alice):**

   ```bash
   mosquitto_pub -h broker.hivemq.com \
     --will-topic wiot/alice/device1/status \
     --will-payload "Device 1 Offline" \
     --will-qos 1 \
     -t wiot/alice/device1/status -l
   ```

   * The `-l` option keeps the connection open and allows typing messages.

3. **Publisher types messages:**

   ```
   Device 1 Online
   Temperature: 21°C
   Humidity: 40%
   ```

4. **Close publisher terminal abruptly (simulate disconnect).**

### ✅ Observation:

* The subscriber sees "Device 1 Offline" published automatically by the broker.

### 📝 Questions:

* Why is LWT important in monitoring devices?
* What would happen if the publisher disconnected normally?

---

## Phase 6: Integrated Smart Home Simulation

* **Publisher (Alice):**

  ```bash
  mosquitto_pub -h broker.hivemq.com -t wiot/alice/home/temp -m "21°C" -q 1 -r
  mosquitto_pub -h broker.hivemq.com -t wiot/alice/home/humidity -m "40%" -q 1 -r
  mosquitto_pub -h broker.hivemq.com \
    --will-topic wiot/alice/home/door \
    --will-payload "Door Sensor Offline" \
    --will-qos 1 \
    -t wiot/alice/home/door -l
  ```

  (Type `Door Closed`, then close terminal abruptly.)

* **Subscriber (Bob):**

  ```bash
  mosquitto_sub -h broker.hivemq.com -t wiot/alice/home/# -v
  ```

### ✅ Observation:

* Dashboard subscriber sees live updates for temperature, humidity, and door status.
* Retained messages provide immediate state, and LWT reports offline devices.

### 📝 Questions:

* How do retained messages and LWT complement each other in real deployments?
* What other smart home devices could follow this pattern?
* How would you extend this for multiple rooms or buildings?

---