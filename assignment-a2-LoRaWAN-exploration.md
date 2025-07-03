# Assignment A2 – LoRaWAN Exploration

**Course:** CSCI-4270 / CSCI-6712 – Wireless Technologies for the Internet of Things  
**Deadline:** 7:00 PM on **July 14, 2025**  
**Submission:** Upload as **one zip file** on Brightspace  
**Team:** Groups of 2 students (graduate students paired with graduate students)

---

## 🌐 Platform Overview

This assignment uses a complete LoRaWAN infrastructure setup that demonstrates real-world LPWAN connectivity.

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
- TTGO ESP32 LoRa32 board or TTGO T-Beam (915 MHz with antenna)
- Micro USB cable for programming

**Software Setup:**
- Arduino IDE (version 2.0 or later)
- ESP32 board package
- MCCI LoRaWAN LMIC Library
- MQTT Explorer (download from https://mqtt-explorer.com)
- Python 3.x with paho-mqtt library

### 🔧 Initial Setup

> **Note:** Skip this section if you completed the in-class tutorial on July 3.

#### Arduino IDE Configuration

1. Open Arduino IDE
2. Navigate to **Tools → Board → Boards Manager**
3. Search for "esp32" and install **"esp32 by Espressif"** if not done during Assignment 1
4. Select **Tools → Board → ESP32 Arduino → TTGO LoRa32-OLED** (or T-Beam)
   > **Note:** T-Beam is the longer form factor board with built-in GPS module
5. Set upload speed: **Tools → Upload Speed → 115200**

#### LMIC Library Installation

1. Go to **Sketch → Include Library → Manage Libraries**
2. Search for "LMIC" and install **"MCCI LoRaWAN LMIC Library"**

---

## 🔵 Part 1 – LoRaWAN Uplink Test

### 🎯 Learning Objectives

- Configure TTGO ESP32 as LoRaWAN OTAA device
- Set up uplinks on US915 frequency plan
- Verify successful join and data transmission via MQTT
- Understand LoRaWAN network architecture

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
6. Watch for `EV_JOINED` message (this confirms successful network join)
7. Device will send uplinks periodically after joining

#### Step 4: Verify via MQTT

**Download MQTT Explorer:** First, download and install MQTT Explorer from https://mqtt-explorer.com

**Connection Setup:** Use the configuration as shown in [the screenshot](a2-material/mqtt-config.jpg) with these details:
- **Broker:** `nam1.cloud.thethings.network`
- **Port:** `8883`
- **Protocol:** `mqtt://`
- **Username:** `test-dal@ttn`
- **Password:** Non-interactive API key (provided separately)

**Finding Your Device Data:** 
- Once connected, use the search button in MQTT Explorer
- Enter your DevEUI to quickly locate your device
- You'll see packets appearing under your device's topic automatically
- No need to manually subscribe to specific topics

**Verification:** Confirm receipt of at least 5 uplink packets with timestamps

### 🔧 Troubleshooting Part 1

| Problem | Solution |
|---------|----------|
| Device not joining (`EV_JOINED` never appears) | Check DevEUI/AppEUI are in little-endian format, verify AppKey |
| No data in MQTT Explorer | Ensure connection settings match exactly, check password |
| Compilation errors | Verify LMIC library is installed, check board selection |
| `FAILURE` messages in Serial Monitor | Usually indicates join failure - double-check all identifiers |
| Device joins but no uplinks | Check if `do_send()` is being called in your code |

### ✅ Part 1 Deliverables

- [ ] Screenshot from MQTT Explorer showing ≥5 uplinks from your device
- [ ] `part1_uplink.ino` with comments identifying:
  - Sending function and transmission period
  - Join process handling code
  - Event callback functions including packet reception
  - Your device identifiers (DevEUI, AppEUI, AppKey)

---

## 🟩 Part 2 – Payload + Downlink Command *(Undergraduate Students Only)*

### 🎯 Learning Objectives

- Transmit application-layer data in a structured JSON format
- Process and validate received payloads using a Python MQTT subscriber
- Analyze key radio parameters (frequency, RSSI, SNR) through data visualization
- Implement actuator control via MQTT-based downlink messaging

### 📋 Requirements

#### 1. Modify the Arduino Sketch

Update the provided Arduino sketch to:

- Send a JSON-encoded payload every 60 seconds containing:

```json
{"t": <random_temperature>, "h": <random_humidity>}
```

where temperature ∈ [15, 30] °C and humidity ∈ [30, 60] %

**Implementation hints:**
- Use Arduino's `String` class or character arrays to build JSON
- Ensure proper JSON formatting with quotes and commas
- Convert the JSON string to bytes before transmission

#### 2. Implement Python MQTT Subscriber

Install required python library: `paho-mqtt`, then use the provided Python [template](a2-material/mqtt-template.py) script to:

- Connect to The Things Stack MQTT broker and subscribe to your device's uplink topic
- Decode the JSON payload and extract temperature and humidity values
- Log and plot:
  - Uplink frequency (Hz)
  - RSSI (dBm) - signal strength indicator
- Save RSSI data to CSV file for analysis

**Data format documentation:** Refer to [TTN data formats](https://www.thethingsindustries.com/docs/integrations/data-formats/)

#### 3. Implement Downlink Control via MQTT

Extend the Python script to send downlink commands:
- `0x01` → Turn **ON** the onboard LED
- `0x00` → Turn **OFF** the LED

Implement logic in the Arduino sketch to:
- Check for received downlink data in callbacks
- Parse the command byte
- Control the LED accordingly
- Print confirmation to Serial Monitor

**Reference:** [TTN MQTT Integration](https://www.thethingsindustries.com/docs/integrations/other-integrations/mqtt/)


### ✅ Part 2 Deliverables

- [ ] `part2_payload.ino`: Updated Arduino code with JSON payload and LED control
- [ ] `downlink_screenshot.png`: Serial Monitor showing LED control confirmation
- [ ] `mqtt-test.py`: Python MQTT client with clear comments
- [ ] Two plots: Frequency vs Time and RSSI vs Time
- [ ] `rssi_data.csv`: Logged RSSI samples with columns: `timestamp`, `rssi`
- [ ] `code-explanation.txt`: 
  - How uplink message parsing was implemented and verified
  - How downlink interaction was implemented and verified
  - Challenges faced and solutions

---

## 🟠 Part 3 – Link Budget and RF Propagation Analysis *(Graduate Students Only)*

### 🎯 Learning Objectives

- Conduct empirical signal strength measurements in a real LoRaWAN deployment
- Model urban RF propagation using the COST Hata model
- Compare theoretical predictions to empirical data
- Understand factors affecting long-range wireless communication

### 📋 Requirements

#### 1. RSSI Measurement Campaign

Install required python library: `paho-mqtt`, then use the provided Python [template](a2-material/mqtt-template.py) script to:

- Connect to The Things Stack MQTT broker and subscribe to your device's uplink topic
- Decode and automatically log **RSSI values** and **timestamps** for each received packet

**Reference:** [TTN data formats](https://www.thethingsindustries.com/docs/integrations/data-formats/)

#### 2. Associate RSSI Samples with Device Locations

Conduct measurements from at least **three distinct physical locations** on or near campus with different propagation conditions.

**Each location must include:**

- An estimated distance (in meters) to the gateway (Goldberg Building rooftop)
- A brief description of the propagation environment
- At least **ten RSSI samples**

**Location selection guidelines:**
- **Location 1:** Line-of-sight (e.g., open area with clear view of Goldberg Building)
- **Location 2:** Partially obstructed (e.g., behind buildings, trees)
- **Location 3:** Heavily obstructed or indoor location

**Tracking methodology:** You must devise your own method to associate RSSI measurements with locations. You can consider any solution from the following:
- Manual logging with timestamps
- GPS coordinates from smartphone
- Automated location tags in your Python script

#### 3. Theoretical Propagation Modeling

Implement the [COST Hata urban path loss model](https://en.wikipedia.org/wiki/COST_Hata_model) to estimate expected received power. You must determine *all the elements of the Link budget* and the *path loss* and provide referenced explanation.

#### 4. Data Analysis and Comparison

- Compare **measured RSSI** with **predicted received power**
- Plot received power vs. distance (measured and theoretical)
- Calculate mean absolute error (MAE) for each location
- Analyze deviations and discuss possible causes

### ✅ Part 3 Deliverables

- [ ] `rssi_logger.py`: Python script for collecting RSSI measurements
- [ ] `rssi_data.csv`: Columns: `timestamp`, `rssi`, `location_label`, `distance_m`, `environment`
- [ ] `link_budget_model.py`: COST Hata implementation and comparison logic
- [ ] `comparison_plot.png`: Measured RSSI vs. distance with theoretical overlay
- [ ] `analysis_notes.txt`: Technical report (1-2 pages) including:
  - Location tracking methodology
  - Link budget parameter justification
  - Key findings from comparison
  - Real-world deviation analysis
  - Suggestions for improving coverage

---

## 📦 Final Submission Requirements

Submit all required materials as **one zip file** on Brightspace.

### File Structure

#### Undergraduate Students:
```
A2_GroupXX_Undergraduate/
├── Part1_Uplink/
│   ├── part1_uplink.ino
│   └── mqtt_screenshot.png
├── Part2_Payload/
│   ├── part2_payload.ino
│   ├── downlink_screenshot.png
│   ├── mqtt-test.py
│   ├── frequency_plot.png
│   ├── rssi_plot.png
│   ├── rssi_data.csv
│   └── code-explanation.txt
└── README.txt
```

#### Graduate Students:
```
A2_GroupXX_Graduate/
├── Part1_Uplink/
│   ├── part1_uplink.ino
│   └── mqtt_screenshot.png
├── Part3_Propagation/
│   ├── rssi_logger.py
│   ├── rssi_data.csv
│   ├── link_budget_model.py
│   ├── comparison_plot.png
│   └── analysis_notes.txt
└── README.txt
```

### README.txt Template
```
Assignment A2 - LoRaWAN Exploration
Group XX: [Your Group Number]
Track: [Undergraduate / Graduate]

Team Members:
- Student 1 Name (ID: xxxxxxx) - [Undergraduate/Graduate]
- Student 2 Name (ID: xxxxxxx) - [Undergraduate/Graduate]

Work Distribution:
- Part 1 (LoRaWAN Uplink): [Who did what]
- Part 2 (Payload + Downlink): [Undergraduate only - who did what]
- Part 3 (Propagation Analysis): [Graduate only - who did what]

Project Summary:
Device Identifiers Used: [DevEUI from your assignment]
Gateway Location: Goldberg Building Rooftop
Part 2 Implementation: [Undergraduate: Brief description of JSON payload format]
Part 3 Locations: [Graduate: List of measurement locations chosen]

Additional Notes:
- [Challenges faced and solutions]
- [Interesting observations about LoRaWAN behavior]
- [Questions or suggestions]

Testing Environment:
- Location: [Where you conducted testing]
- Date/Time: [When measurements were taken]
- Weather conditions: [If relevant for Part 3]
- Software versions: [Arduino IDE, Python version, libraries]

Special Instructions:
- [Any special setup needed]
- [Known limitations or issues]
- [Additional dependencies]
```

---

## 📊 Grading Rubric

### Undergraduate Track
| Component | Points | Description |
|-----------|--------|-------------|
| Part 1 - LoRaWAN Uplink | 40 | Successful join and uplink transmission with documentation |
| Part 2 - Payload & Downlink | 50 | JSON payload, MQTT analysis, and bidirectional communication |
| Code Quality & Documentation | 10 | Clean code, proper comments, professional submission |
| **Total** | **100** | |

### Graduate Track
| Component | Points | Description |
|-----------|--------|-------------|
| Part 1 - LoRaWAN Uplink | 30 | Successful join and uplink transmission with documentation |
| Part 3 - Propagation Analysis | 60 | Rigorous measurement campaign and theoretical comparison |
| Code Quality & Documentation | 10 | Clean code, proper analysis, professional submission |
| **Total** | **100** | |

---

## 📚 Extended Resources

### LoRaWAN References
- [LoRa Alliance Technical Resources](https://lora-alliance.org/technical-resources/)
- [The Things Network Documentation](https://www.thethingsindustries.com/docs/)
- [MCCI LMIC Library Documentation](https://github.com/mcci-catena/arduino-lmic)

### MQTT Tools and Guides
- [MQTT Explorer](https://mqtt-explorer.com/) - Recommended MQTT client
- [Paho MQTT Python Client](https://pypi.org/project/paho-mqtt/) - Python library
- [MQTT Essentials](https://www.hivemq.com/mqtt-essentials/) - Protocol guide

### RF Propagation Resources
- [COST Hata Model Calculator](https://www.pasternack.com/t-calculator-hata-urban-propagation-loss.aspx)
- [RF Link Budget Guide](https://www.everythingrf.com/rf-calculators/rf-link-budget-calculator)

---

## 🆘 Getting Help

### Where to Get Help
- **Teams Discussion Forum:** Post general questions
- **Office Hours:** Bring specific technical problems
- **Lab Sessions:** Get hands-on assistance with hardware

### Common Issues and Solutions

**"EV_JOIN_FAILED" or device won't join:**
- Double-check DevEUI and AppEUI are little-endian
- Verify AppKey is correct and big-endian
- Ensure gateway is online and in range
- Check regional frequency configuration

**No data in MQTT Explorer:**
- Verify broker address and port (8883)
- Check username includes @ttn suffix
- Ensure password (API key) is correct
- Look for connection status in MQTT Explorer

**Python script connection issues:**
- Install paho-mqtt: `pip install paho-mqtt`
- Use port 8883 for secure connection
- Include full topic path with v3 prefix

**Poor RSSI or no signal:**
- Check antenna is properly connected
- Ensure device is oriented correctly
- Move to location with better line-of-sight
- Verify transmit power settings

---

**Questions?** Post on Teams with error messages, screenshots, and code snippets for fastest help!