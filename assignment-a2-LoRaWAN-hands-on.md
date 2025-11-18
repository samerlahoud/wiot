# Assignment A2 – LoRaWAN Exploration

**Course:** CSCI-4270 / CSCI-6712 – Wireless Technologies for the Internet of Things  
**Deadline:** 7:00 PM on **November 27, 2025**  
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

## 📋 Assignment Structure

| Component | Requirements | Points |
|-----------|-------------|--------|
| **LoRaWAN Uplink** | All students (mostly completed in-class tutorial) | 100 points |
| **Bonus – Maximum Range Challenge** | Optional for all students | Up to 10 bonus points |

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

### 🔧 Initial Setup

#### Arduino IDE Configuration

1. Open Arduino IDE
2. Navigate to **Tools → Board → Boards Manager**
3. Search for "esp32" and install **"esp32 by Espressif"**
4. Select **Tools → Board → ESP32 Arduino → TTGO LoRa32-OLED** (or T-Beam)
   > **Note:** T-Beam is the longer form factor board with built-in GPS module
5. Set upload speed: **Tools → Upload Speed → 115200**

#### LMIC Library Installation

1. Go to **Sketch → Include Library → Manage Libraries**
2. Search for "LMIC" and install **"MCCI LoRaWAN LMIC Library"**

#### LMIC Library Configuration

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

---

## 🔵 LoRaWAN Uplink Test

### 🎯 Learning Objectives

- Configure TTGO ESP32 as LoRaWAN OTAA device
- Set up uplinks on US915 frequency plan
- Verify successful join and data transmission via MQTT
- Understand LoRaWAN network architecture

### 📋 What You Should Have From Tutorial

During the tutorial session, you:
1. Configured your device identifiers (DevEUI, AppEUI, AppKey)
2. Programmed your TTGO ESP32 device
3. Verified successful network join (saw `EV_JOINED` message)
4. Set up MQTT Explorer and observed uplink packets
5. Understood the LoRaWAN architecture and data flow

### 🔑 Device Identifiers Reference

You received a CSV file with identifiers in this format:
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

### 📡 MQTT Explorer Connection Details

**Connection Setup:**
- **Broker:** `nam1.cloud.thethings.network`
- **Port:** `8883`
- **Protocol:** `mqtt://`
- **Username:** `test-dal@ttn`
- **Password:** Non-interactive API key (provided in class)

**Finding Your Device Data:** 
- Once connected, use the search button in MQTT Explorer
- Enter your DevEUI to quickly locate your device
- You'll see packets appearing under your device's topic automatically
- MQTT Explorer shows RSSI values and generates charts automatically

### 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Device not joining (`EV_JOINED` never appears) | Check DevEUI/AppEUI are in little-endian format, verify AppKey |
| No data in MQTT Explorer | Ensure connection settings match exactly, check password |
| Compilation errors | Verify LMIC library is installed, check board selection |
| `FAILURE` messages in Serial Monitor | Usually indicates join failure - double-check all identifiers |
| Device joins but no uplinks | Check if `do_send()` is being called in your code |

### ✅ Deliverables

Submit the following files documenting your work:

- [ ] **`part1_uplink.ino`** - Your Arduino sketch with detailed comments identifying:
  - Your device identifiers (DevEUI, AppEUI, AppKey) in the code
  - The sending function (`do_send()`) and where it's called
  - Transmission period (TX_INTERVAL)
  - Join process handling code
  - Event callback functions (`onEvent()`)
  - Code that handles packet transmission acknowledgments

- [ ] **`mqtt_screenshot.png`** - Screenshot from MQTT Explorer showing:
  - At least 5 uplink packets from your device
  - Timestamps visible for the packets
  - Your device's topic path clearly shown
  - RSSI values visible in the packet data

- [ ] **`part1_report.txt`** - Brief report (1 page) including:
  - Your device's DevEUI (for reference)
  - Description of how you verified successful join
  - Summary of uplink behavior (transmission interval, success rate)
  - Any challenges you encountered and how you resolved them
  - 2-3 *personal* observations about LoRaWAN behavior you noticed

---

## 🏆 Bonus Challenge – Maximum Range Competition (Optional)

### 🎯 Objective

Find the **farthest outdoor location** where you can still successfully receive packets from the LoRaWAN gateway!

This is an entirely **optional** bonus challenge that can earn you up to **10 additional points** beyond the base assignment.

### 📋 How It Works

**Your Task:**
1. Take your programmed TTGO device to progressively farther outdoor locations
2. Use **MQTT Explorer** to monitor incoming packets in real-time
3. Move farther away until you reach your maximum range
4. Document your achievement!

**What to Monitor in MQTT Explorer:**
- MQTT Explorer automatically shows you RSSI values in the packet data
- It also displays a chart showing RSSI over time
- Watch for packets appearing under your device's topic

### 📸 What to Submit (For Bonus Points)

Create a simple report with:

**1. Location Information:**
- Where you reached maximum range (description, address, or GPS coordinates)
- Distance from gateway (use Google Maps: right-click → "Measure distance")
- Brief description of the environment (open field, residential area, etc.)
- Photo of the location (optional but encouraged!)

**2. MQTT Explorer Screenshot showing:**
- Your device receiving packets at maximum range location
- RSSI chart showing signal strength over time
- Clear timestamp showing when test was conducted
- At least 3-5 successful packets received at that location

**3. Brief Analysis (one paragraph of 4-5 sentences):**
- What you learned about LoRa's range capabilities
- What factors helped or limited your range (terrain, buildings, elevation, etc.)
- Any interesting observations during your testing
- Comparison to what you expected

### 🎓 Graduate Student Extension

**Path Loss Analysis:**

Calculate the theoretical expected received signal strength at your maximum range location using an appropriate path loss model.

**Include in your report:**
- Show your path loss calculation step-by-step
- Calculate expected RSSI
- Compare to your measured average RSSI from MQTT Explorer
- Write one paragraph (4-5 sentences) discussing:
  - How close was theory to reality?
  - What real-world factors does path loss not account for?
  - Why might there be differences between predicted and measured values?

### 💡 Tips for Maximum Range

**Location Strategy:**
- Start outdoors with clear line-of-sight to Goldberg Building
- Higher elevation generally = better range
- Open areas (parking lots, athletic fields, parks) work best
- Keep antenna vertical for best performance

**Device Tips:**
- Ensure device is fully charged/powered
- Antenna must be properly connected
- Consider reducing `TX_INTERVAL` in your code (e.g., from 60s to 30s) to send more frequently for easier monitoring
- Keep Serial Monitor running on a laptop to verify device is transmitting

**Safety First:**
- Stay in safe, accessible public areas
- Don't trespass on private property
- Go with a partner, especially if venturing far from campus
- Bring fully charged phone and laptop
- Test during daylight hours

### 📦 Bonus Submission Format

If attempting the bonus challenge, add these files to your submission:

```
A2_GroupXX/
├── Part1_Uplink/
│   ├── part1_uplink.ino
│   ├── mqtt_screenshot.png
│   └── part1_report.txt
├── Bonus_MaxRange/
│   ├── location_info.txt
│   ├── max_range_screenshot.png
│   ├── location_photo.jpg (optional)
│   └── range_analysis.txt (or .pdf)
│   └── path_loss_calculations.txt (graduate students only)
└── README.txt
```

### 🤔 Bonus Challenge FAQ

**Q: How do I know if I'm still connected?**  
A: Watch MQTT Explorer - if you see new packets appearing with recent timestamps, you're connected. The RSSI chart will also update in real-time.

**Q: What's a good RSSI value?**  
A: LoRa works down to -120 dBm or even lower. Don't worry if values seem very negative - that's normal! Typical ranges:
- -50 to -80 dBm: Excellent signal
- -80 to -100 dBm: Good signal
- -100 to -120 dBm: Weak but usable
- Below -120 dBm: May start losing packets

**Q: How long should I stay at my maximum range location?**  
A: Stay long enough to see at least 3-5 packets arrive successfully (check both MQTT Explorer and Serial Monitor), then take your screenshot.

---

## 📦 Final Submission Requirements

Submit all required materials as **one zip file** on Brightspace by **7:00 PM on November 27, 2025**.

### File Structure

**All Students (Required):**
```
A2_GroupXX/
├── Part1_Uplink/
│   ├── part1_uplink.ino
│   ├── mqtt_screenshot.png
│   └── part1_report.txt
└── README.txt
```

**If Attempting Bonus Challenge (Optional):**
```
A2_GroupXX/
├── Part1_Uplink/
│   ├── part1_uplink.ino
│   ├── mqtt_screenshot.png
│   └── part1_report.txt
├── Bonus_MaxRange/
│   ├── location_info.txt
│   ├── max_range_screenshot.png
│   ├── location_photo.jpg (optional)
│   ├── range_analysis.txt
│   └── path_loss_calculations.txt (graduate students only)
└── README.txt
```

### README.txt Template
```
Assignment A2 - LoRaWAN Exploration
Group XX: [Your Group Number]

Team Members:
- Student 1 Name (ID: xxxxxxx) - [Undergraduate/Graduate]
- Student 2 Name (ID: xxxxxxx) - [Undergraduate/Graduate]

Work Distribution:
- LoRaWAN Uplink: [Who did what]
- Bonus Challenge (if attempted): [Who did what]

Project Summary:
Device Identifiers Used: [Your DevEUI]
Gateway Location: Goldberg Building Rooftop
Bonus Challenge Attempted: [Yes/No]
Maximum Range Achieved: [If applicable: distance in meters/km]

Additional Notes:
- [Challenges faced and solutions]
- [Interesting observations about LoRaWAN behavior]
- [Any questions or suggestions]

Testing Environment:
- Testing Location: [Where you verified your device works]
- Testing Date/Time: [When you completed setup]
- Bonus Testing Date/Time: [If applicable]
- Weather Conditions: [If relevant for bonus challenge]
- Software Versions: [Arduino IDE version, library versions]

Special Instructions:
- [Any special setup needed to run your code]
- [Known limitations or issues]
- [Additional dependencies if any]
```

---

## 📚 Resources

### LoRaWAN References
- [LoRa Alliance Technical Resources](https://lora-alliance.org/technical-resources/)
- [The Things Network Documentation](https://www.thethingsindustries.com/docs/)
- [MCCI LMIC Library Documentation](https://github.com/mcci-catena/arduino-lmic)

### MQTT Tools and Guides
- [MQTT Explorer](https://mqtt-explorer.com/) - MQTT client with visualization
- [TTN MQTT Integration Guide](https://www.thethingsindustries.com/docs/integrations/mqtt/)

### RF Propagation Resources (For Bonus Challenge)
- [RF Link Budget Basics](https://www.everythingrf.com/community/what-is-link-budget)

### Distance Measurement Tools
- Google Maps: Right-click anywhere → "Measure distance"
- Many smartphone map apps have built-in distance measurement

---

## 🆘 Getting Help

### Where to Get Help
- **Teams Discussion Forum:** Post general questions and discuss with peers
- **Office Hours:** Bring specific technical problems
- **In-Class Q&A:** Ask questions during class time

### Common Issues and Solutions

**"EV_JOIN_FAILED" or device won't join:**
- Double-check DevEUI and AppEUI are little-endian (reversed byte order)
- Verify AppKey is correct and big-endian (not reversed)
- Ensure antenna is properly connected
- Check that gateway is online and in range
- Verify frequency configuration (US915)

**No data in MQTT Explorer:**
- Verify broker address: `nam1.cloud.thethings.network`
- Check port is set to 8883
- Ensure username includes `@ttn` suffix: `test-dal@ttn`
- Verify password (API key) is correct
- Look for connection status indicator in MQTT Explorer
- Try disconnecting and reconnecting

**Compilation errors:**
- Verify LMIC library is installed correctly
- Check board selection matches your hardware
- Ensure ESP32 board package is installed
- Try updating to latest library versions

**Poor RSSI or no signal:**
- Check antenna is properly connected (tight connection)
- Ensure device antenna is oriented vertically
- Move to location with better line-of-sight to Goldberg Building
- Verify your device is actually transmitting (check Serial Monitor)
- Make sure you're outdoors if possible

**Device joins but no uplinks appear:**
- Check if `do_send()` is being called in your code
- Verify `TX_INTERVAL` is set to a reasonable value (30-60 seconds)
- Look for "Packet queued" message in Serial Monitor
- Ensure `LMIC_setTxData2()` is being called properly

**Bonus Challenge - Can't get very far:**
- Remember that LoRa is designed for long range - you should be able to reach at least 500m-1km in open areas
- Try different directions from campus
- Higher elevation helps significantly
- Make sure antenna is vertical and properly connected
- Check that TX power is set correctly in code

---

**Questions?** Post on the Teams discussion forum with error messages, screenshots, and code snippets for fastest help!

**Good luck, and happy exploring the world of LoRaWAN! 📡**