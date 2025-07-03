# Assignment A2 – LoRaWAN Exploration

**Course:** CSCI-4270 / CSCI-6712 – Wireless Technologies for the Internet of Things  
**Deadline:** 7:00 PM on **July 14, 2025**  
**Submission:** Upload as **one zip file** on Brightspace  
**Team:** Groups of 2 students (graduate students paired with graduate students)

---

## 🌐 Platform Overview

This assignment uses a complete LoRaWAN infrastructure setup that demonstrates real-world LPWAN connectivity:

### System Architecture

```
┌─────────────────┐    LoRa RF     ┌─────────────────┐
│   TTGO ESP32    │ ◄─────────────►│ LoRaWAN Gateway │
│   LoRa Device   │   915 MHz      │ (Goldberg Bldg) │
│                 │                │                 │
└─────────────────┘                └─────────────────┘
         │                                   │
         │ USB Programming                   │ Internet
         │                                   ▼
┌─────────────────┐                ┌─────────────────┐
│ Development PC  │                │ The Things      │
│   Arduino IDE   │                │ Network (TTN)   │
│                 │                │ Cloud Server    │
└─────────────────┘                └─────────────────┘
                                             │
                                             │ MQTT Broker
                                             │
                                    ┌─────────────────┐
                                    │ Monitoring PC   │
                                    │ MQTT Explorer   │
                                    │                 │
                                    └─────────────────┘
```

### Platform Components

| Component | Role | Location |
|-----------|------|----------|
| **TTGO ESP32 LoRa32** | End device sensor node | Connected to development PC |
| **LoRaWAN Gateway** | Radio bridge (LoRa ↔ IP) | Goldberg Building rooftop |
| **TTN Network Server** | LoRaWAN protocol handling | The Things Network cloud |
| **Development PC** | Device programming & configuration | Arduino IDE workstation |
| **Monitoring PC** | Data visualization/control | MQTT Explorer client |

### Data Flow
1. **TTGO device** sends sensor data via LoRa radio (915 MHz)
2. **Gateway** receives LoRa packets and forwards via internet to TTN
3. **TTN Network Server** handles LoRaWAN protocol, security, and routing
4. **MQTT Publishing:** TTN automatically publishes device data to MQTT topics
5. **Monitoring PC** with MQTT client subscribes to device data for real-time analysis

### What is MQTT?
**MQTT (Message Queuing Telemetry Transport)** is a lightweight messaging protocol designed for IoT applications. It uses a **publish-subscribe** model:

- **Publisher:** TTN publishes your device data to specific topics (like `/devices/your-device/up`)
- **Subscriber:** Your MQTT Explorer client subscribes to these topics to receive the data
- **Broker:** TTN's MQTT broker routes messages between publishers and subscribers
- **Topics:** Organized like file paths (e.g., `v3/app-id@ttn/devices/device-id/up`)

**Why MQTT for LoRaWAN?** It provides a simple, standardized way to access your device data without needing custom APIs. You can easily integrate with databases, web applications, or analysis tools by subscribing to the relevant MQTT topics.

This setup mirrors real-world IoT deployments where devices communicate through gateways to cloud-based network servers, with separate systems for development/configuration and monitoring/analysis.

---

## 📋 Track Requirements

| Track | Requirements |
|-------|-------------|
| **Undergraduate** | Complete Parts 1 and 2 |
| **Graduate** | Complete Parts 1 and 3 |

---

## 🚀 Getting Started

### Hardware & Software Requirements

**Hardware Needed:**
- TTGO ESP32 LoRa32 board (915 MHz with antenna)
- Micro USB cable for programming

**Software Setup:**
- Arduino IDE (version 2.0 or later)
- ESP32 board package
- MCCI LoRaWAN LMIC Library

### 🔧 Initial Setup

> **Note:** Skip this section if you completed the in-class tutorial on July 3.

#### Arduino IDE Configuration
1. Open Arduino IDE
2. Navigate to **Tools → Board → Boards Manager**
3. Search for "esp32" and install **"esp32 by Espressif"** (if not from Assignment 1)
4. Select **Tools → Board → ESP32 Arduino → TTGO LoRa32-OLED** (or T-Beam)
   > **Note:** T-Beam is the longer form factor board with built-in GPS module
5. Set upload speed: **Tools → Upload Speed → 115200**

#### LMIC Library Installation
1. Go to **Sketch → Include Library → Manage Libraries**
2. Search for "LMIC" and install **"MCCI LoRaWAN LMIC Library"**

---

## 🔵 Part 1 – LoRaWAN Uplink Test

### 🎯 Objectives
- Configure TTGO ESP32 as LoRaWAN OTAA device
- Set up uplinks on US915 frequency plan
- Verify successful join and data transmission via MQTT

### 📋 Step-by-Step Instructions

#### Step 1: Configure Your Device Identifiers

You'll receive a CSV file with identifiers in this format:
```
dev_eui;app_eui;app_key
22B580C71BB8721C;A96E5C885B8163BB;670988641E69DFFF09D23098B9E049DA
```

**Important:** DevEUI and AppEUI must be converted to little-endian format:

| Identifier | Format | Example |
|------------|--------|---------|
| **DevEUI** | Little-endian (reversed) | `0x1C, 0x72, 0xB8, 0x1B, 0xC7, 0x80, 0xB5, 0x22` |
| **AppEUI** | Little-endian (reversed) | `0xBB, 0x63, 0x81, 0xB8, 0x88, 0x5C, 0x6E, 0xA9` |
| **AppKey** | Big-endian (as-is) | `0x67, 0x09, 0x88, 0x64, 0x1E, 0x69, 0xDF, 0xFF, 0x09, 0xD2, 0x30, 0x98, 0xB9, 0xE0, 0x49, 0xDA` |

#### Step 2: Configure LMIC Library
Verify these definitions are **uncommented** in the MCCI LoRaWAN LMIC library configuration:
- Navigate to your Arduino libraries folder:
  - **Windows:** `C:\Users\{username}\Documents\Arduino\libraries\`
  - **macOS:** `/Users/{username}/Documents/Arduino/libraries/`
  - **Linux:** `/home/{username}/Arduino/libraries/`
- Open `MCCI_LoRaWAN_LMIC_library/project_config/lmic_project_config.h`
- Ensure these lines are **not commented out**:
```cpp
#define CFG_us915 1
#define CFG_sx1276_radio 1
```
If they are commented (have `//` in front), remove the `//` to enable them.

#### Step 3: Program and Test
1. Insert your converted identifiers into the provided [template](a2-material/rnd-test/rnd-test.ino)
2. Connect TTGO ESP32 to your computer
3. Select correct board and port in Arduino IDE
4. Compile and upload the sketch
5. Open Serial Monitor (baud: 9600)
6. Watch for `EV_JOINED` message
7. Device will send uplinks periodically

#### Step 4: Verify via MQTT
**Download MQTT Explorer:** First, download and install MQTT Explorer from https://mqtt-explorer.com

**Connection Setup:** Use the configuration as shown in [the screenshot](a2-material/mqtt-config.jpg) with these details:
- **Broker:** `nam1.cloud.thethings.network:8883`
- **Username:** `test-dal@ttn`
- **Password:** Non-interactive API key provided for you separately

**Finding Your Device Data:** 
- Once connected, use the search button in MQTT Explorer
- Enter your DevEUI to quickly locate your device
- You'll see packets appearing under your device's topic automatically
- No need to manually subscribe to specific topics

**Verification:** Confirm receipt of at least 5 uplink packets

### ✅ Part 1 Deliverables
- [ ] Screenshot from MQTT Explorer showing ≥5 uplinks from your device
- [ ] `part1_uplink.ino` (identify these key elements with comments):
  - Sending function and transmission period
  - Join process handling
  - Event callback functions including packet reception


## 🟩 Part 2 – Payload + Downlink Command *(Undergraduate Students Only)*

### 🎯 Learning Objectives

* Transmit application-layer data in a structured JSON format
* Process and validate received payloads using a Python MQTT subscriber
* Analyze key radio parameters (frequency, RSSI, SNR) through data visualization
* Implement actuator control via MQTT-based downlink messaging

### 📋 Requirements

1. **Modify the provided Arduino sketch** to:

   * Send a JSON-encoded payload every 60 seconds containing:

     ```json
     {"t": <random_temperature>, "h": <random_humidity>}
     ```

     where temperature ∈ \[15, 30] °C and humidity ∈ \[30, 60] %

2. **Use the provided Python [template](a2-material/mqtt-template.py) script** to:

   * Connect to The Things Stack MQTT broker and subscribe to your device’s uplink topic (you may need to install the `paho-mqtt` library)
   * Decode the JSON payload and extract temperature and humidity values. A detailed documentation on data formats is provided [here](https://www.thethingsindustries.com/docs/integrations/data-formats/) 
   * Log and plot:

     * Uplink frequency (Hz)
     * RSSI (dBm)

3. **Implement downlink control via MQTT**

You can refer to the TTN [documentation](https://www.thethingsindustries.com/docs/integrations/other-integrations/mqtt/) on how to connect an MQTT client and subscribe to uplinks or publish downlinks.

   * Extend the Python script to send a downlink command:

     * `0x01` → Turn **ON** the onboard LED
     * `0x00` → Turn **OFF** the LED
   * Implement logic in the Arduino sketch to interpret and act on these commands

### ✅ Deliverables

* `part2_payload.ino`: your updated and commented Arduino code including all the requirements
* `downlink_screenshot.png`: showing LED control confirmation in Serial Monitor
* `mqtt-test.py`: your modified Python MQTT client (with clear comments and example output)
* Two plots visualizing signal quality data (frequency and RSSI)
* `code-explanation.txt`: include:

  * How the uplink message parsing was implemented and verified
  * How the downlink interaction was implemented and verified