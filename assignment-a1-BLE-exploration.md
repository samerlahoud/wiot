# Assignment A1 – BLE Exploration

**Course:** CSCI-4270 / CSCI-6712 – Wireless Technologies for the Internet of Things  
**Deadline:** June 20, 2025  
**Team:** Groups of 2 students (graduate students with graduate students)

## Track-Specific Requirements
- **Undergraduate Students:** Complete Parts 1, 2, and optionally Part 4
- **Graduate Students:** Complete Parts 1, 3, and optionally Part 4

---

## 🚀 Getting Started

### Prerequisites Checklist
Before you begin, ensure you have:
- [ ] ESP32-C6 development board
- [ ] USB cable for programming
- [ ] Arduino IDE installed (version 2.0 or later recommended)
- [ ] ESP32 board package installed in Arduino IDE
- [ ] BLE scanner app on your smartphone (nRF Connect, BLE Scanner, or similar)
- [ ] Basic understanding of Arduino programming

### Initial Setup Instructions
You may skip this section if you followed the hands-on tutorial session on June 3.

#### 1. Arduino IDE Configuration
```
1. Open Arduino IDE
2. Go to File → Preferences
3. Add this URL to "Additional Board Manager URLs":
   https://espressif.github.io/arduino-esp32/package_esp32_index.json
4. Go to Tools → Board → Boards Manager
5. Search for "esp32" and install "esp32 by Espressif Systems"
6. Select your board: Tools → Board → ESP32 Arduino → ESP32C6 Dev Module
```

#### 2. Test Your Setup
Upload this simple test code to verify everything works:
```cpp
void setup() {
  Serial.begin(115200);
  Serial.println("ESP32-C6 BLE Assignment Ready!");
}

void loop() {
  delay(1000);
}
```

---

## 🔍 Understanding BLE Basics

### Key BLE Concepts You'll Use

**Advertisement:** Broadcasting data that other devices can discover without connecting  
**GATT (Generic Attribute Profile):** Protocol for connected BLE communication  
**Service:** Collection of related functionality (like "Temperature Sensor")  
**Characteristic:** Individual data point within a service (like "Temperature Value")  
**UUID:** Unique identifier for services and characteristics

---

## 🟦 Part 1 – BLE Broadcaster with Randomized Data

### 🎯 Learning Objectives
- Understand BLE advertisement packets
- Learn how to broadcast data without connections
- Practice generating and transmitting random data
- Observe dynamic advertisement data updates

### 📋 Step-by-Step Instructions

#### 🔌 Step 1: Connect Your ESP32-C6 Board

1. **Plug in your ESP32-C6** using a USB-C cable.
   Make sure you are connected to the correct UART port on your board.

2. **In the Arduino IDE:**

   * Go to **Tools > Board** and select:

     ```
     ESP32C6 Dev Module
     ```

   * Go to **Tools > Port** and select the correct serial port:

     * On **Windows**: it will appear as `COMx`
     * On **macOS/Linux**: look for something like `/dev/cu.usbmodem*` or `/dev/ttyUSBx`

3. **If no port appears on Windows:**
   You may need to install the USB-to-UART driver.

   * Download and install the **CP210x VCP driver** from Silicon Labs:
     👉 [https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers](https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads)

   * After installation, restart the Arduino IDE and check **Tools > Port** again.


#### Step 2: Complete Code Template
```cpp
#include "BLEDevice.h"
#include "BLEUtils.h"
#include "BLEServer.h"
#include "BLEAdvertising.h"

void setup() {
  Serial.begin(115200);
  Serial.println("Starting BLE Broadcaster...");
  
  // Generate random suffix for device name (00-99)
  int randomSuffix = random(0, 100);
  String deviceName = "BLE-Random-" + String(randomSuffix);
  
  // Initialize BLE
  BLEDevice::init(deviceName.c_str());
  
  // Create BLE Server (required even for advertising)
  BLEServer* pServer = BLEDevice::createServer();
  
  // Get advertising object
  BLEAdvertising* pAdvertising = BLEDevice::getAdvertising();
  
  // Set service UUID (16-bit)
  BLEUUID serviceUUID((uint16_t)0x1234);
  pAdvertising->addServiceUUID(serviceUUID);
  
  // Generate random manufacturer data (2 bytes)
  uint8_t manufacturerData[2];
  manufacturerData[0] = random(0, 256);
  manufacturerData[1] = random(0, 256);
  
  // Create manufacturer data string
  String mfgData = "";
  mfgData += (char)manufacturerData[0];
  mfgData += (char)manufacturerData[1];
  
  // Set manufacturer data (0x4C00 is Apple's company ID - use for testing)
  BLEAdvertisementData adData = BLEAdvertisementData();
  adData.setManufacturerData(mfgData);
  pAdvertising->setAdvertisementData(adData);
  
  // Start advertising
  pAdvertising->start();
  
  Serial.println("Device Name: " + deviceName);
  Serial.println("Service UUID: 0x1234");
  Serial.printf("Manufacturer Data: 0x%02X%02X\n", manufacturerData[0], manufacturerData[1]);
  Serial.println("BLE Advertisement started!");
}

void loop() {
  delay(1000);
  // Advertising continues automatically
}
```

#### Step 3: Upload and Test
1. Upload the code to your ESP32-C6
2. Open Serial Monitor (Tools → Serial Monitor) to see output
3. Open your BLE scanner app on your phone
4. Look for your device name (e.g., "BLE-Random-42")

#### Step 4: Analyze Results
When you find your device, look for:
- **Device Name:** Should match what's printed in Serial Monitor
- **Service UUID:** Should show 0x1234
- **Manufacturer Data:** Two random bytes (may be shown as hex values)

#### Step 5: Implement Dynamic Manufacturer Data
Modify the code from Step 2 to make the manufacturer data change every 10 seconds:

**Implementation Hints:**
1. **Move the advertising pointer to global scope** so you can access it from both setup() and loop()
2. **Use `millis()` for timing** instead of `delay()` to check if 10 seconds have passed
3. **Create a separate function** to handle updating the manufacturer data
4. **Remember the update sequence**: Stop advertising → Update data → Restart advertising
5. **Print updates to Serial Monitor** so you can verify the timing works correctly

**Testing Process:**
1. Upload your modified code to ESP32-C6
2. Open Serial Monitor to see update messages every 10 seconds
3. Keep your BLE scanner open and observe the changing manufacturer data
4. **Document timing**: Record how quickly your phone detects the changes
5. **Note any patterns**: Does every update show up? Are there any delays?

### 🔧 Troubleshooting Part 1

| Problem | Solution |
|---------|----------|
| Device not appearing | Check if BLE is enabled on phone, restart ESP32 |
| No manufacturer data visible | Some apps don't show manufacturer data clearly - try nRF Connect |
| Compilation errors | Verify ESP32 board package is installed correctly |
| Random values same each time | ESP32 random() needs seed - add `randomSeed(analogRead(0));` in setup |
| Data not updating every 10 seconds (Step 5) | Check Serial Monitor for update messages, ensure you're stopping/restarting advertising |
| Phone doesn't show data changes (Step 5) | Try refreshing BLE scanner, some apps cache old data |

### ✅ Part 1 Deliverables
- [ ] Screenshot from smartphone showing your device
- [ ] **Two Arduino code files:**
  - Static version (Steps 2-4): `Part1_Static.ino`
  - Dynamic version (Step 5): `Part1_Dynamic.ino`
- [ ] Text explanation (2-3 sentences each):
  - What the device name represents
  - Purpose of the UUID
  - How manufacturer data could be used
  - Observations about the 10-second update behavior and timing

---

## 🟩 Part 2 – BLE Peripheral with Custom GATT Service _(Undergraduate Students Only)_

### 🎯 Learning Objectives
- Design and implement a custom GATT service profile
- Create readable/writable characteristics with appropriate properties
- Handle BLE server callbacks and connection management
- Understand GATT service discovery process

### 📋 Requirements & Design Constraints

#### Your Custom Service Must Include:
1. **Custom 128-bit service UUID** (generate using online UUID generator)
2. **At least 2 characteristics** with different properties:
   - One **readable** characteristic (simulated sensor data)
   - One **writable** characteristic (configuration or control)
3. **Proper connection handling** (connect/disconnect callbacks)
4. **Data updates** - readable characteristic should change over time
5. **Meaningful device name** reflecting your service purpose

#### Suggested Service Ideas:
- **Smart Thermostat**: Temperature reading + target temperature setting
- **Smart Light**: Brightness level + color/mode control  
- **Environmental Monitor**: Humidity reading + sampling rate control
- **Fitness Tracker**: Step count + user weight setting
- **IoT Sensor Hub**: Sensor reading + calibration offset

### 🔧 Technical Implementation Guide

#### Essential BLE Components You'll Need:
```cpp
#include "BLEDevice.h"
#include "BLEServer.h"
#include "BLEUtils.h"
#include "BLE2902.h"  // For descriptors

// Your UUIDs here
#define SERVICE_UUID        "your-service-uuid-here"
#define CHAR1_UUID          "your-characteristic-1-uuid"  
#define CHAR2_UUID          "your-characteristic-2-uuid"
```

#### Key BLE Methods to Research:
- `BLEDevice::init(deviceName)`
- `createServer()` and `setCallbacks()`
- `createService(uuid)` 
- `createCharacteristic(uuid, properties)`
- `setValue()` and `getValue()`
- `startAdvertising()`

#### Characteristic Properties to Consider:
- `PROPERTY_READ` - Client can read value
- `PROPERTY_WRITE` - Client can write value  
- `PROPERTY_NOTIFY` - Server can push updates
- `PROPERTY_INDICATE` - Server can push updates with acknowledgment

### 📚 Essential References

#### Official Documentation:
- [ESP32 BLE Arduino Library](https://github.com/espressif/arduino-esp32/tree/master/libraries/BLE) - Main library docs
- [ESP32 BLE Server Tutorial](https://randomnerdtutorials.com/esp32-ble-server/) - Basic server setup
- [BLE Tutorial Videos](https://www.youtube.com/@Ellisys) - Official BLE specs

#### Code Examples to Study:
- [Basic BLE Server Example](https://github.com/espressif/arduino-esp32/blob/master/libraries/BLE/examples/Server/Server.ino)
- [BLE Notify Example](https://github.com/espressif/arduino-esp32/blob/master/libraries/BLE/examples/Notify/Notify.ino)
- [BLE Write Example](https://github.com/espressif/arduino-esp32/blob/master/libraries/BLE/examples/Write/Write.ino)

#### UUID Generation:
- [Online UUID Generator](https://www.uuidgenerator.net/) - Generate your custom UUIDs
- [Standard BLE Services](https://www.bluetooth.com/specifications/assigned-numbers/16-bit-uuids-for-sdos/) - If using standard services

### 🧪 Testing Process

#### Phase 1: Basic Connection
1. Implement service with one readable characteristic
2. Test device discovery and connection
3. Verify characteristic can be read

#### Phase 2: Add Functionality  
1. Add second characteristic with write capability
2. Implement connection callbacks
3. Test bidirectional communication

#### Phase 3: Validation
1. Test with multiple BLE scanner apps
2. Verify data updates work correctly  
3. Test connection/disconnection behavior

### 🔧 Common Challenges & Hints

| Challenge | Hint |
|-----------|------|
| UUIDs not working | Ensure 128-bit UUIDs are properly formatted with dashes |
| Can't write to characteristic | Check PROPERTY_WRITE is set and callbacks implemented |
| Values not updating | Verify setValue() is called and consider using notify() |
| Connection issues | Implement proper server callbacks for connect/disconnect |
| Service not discoverable | Ensure service is started and added to advertising |

### ✅ Part 2 Deliverables
- [ ] Screenshot showing successful connection and both characteristics
- [ ] Well-commented Arduino code (.ino file) showing your implementation
- [ ] Design document (1-2 pages) explaining:
  - Your service concept and purpose
  - Service/characteristic architecture 
  - How each characteristic works
  - Testing methodology used
  - Any challenges faced and solutions

---

# 🎓 Part 3 – BLE Performance Analysis
***(Graduate Students Only)***

## Environment Selection

Choose **ONE** of the following environments for your testing:

- **Option A:** Indoor Laboratory/Classroom (Large open room with minimal obstacles)
- **Option B:** Outdoor Open Area (Park, courtyard, or large parking area)  
- **Option C:** Indoor Obstructed Environment (Hallway with people, cafeteria, or furnished room)

## 🎯 Learning Objectives

- Conduct rigorous RF performance analysis
- Apply statistical methods to wireless measurements
- Understand environmental impact on BLE propagation
- Create publication-quality data visualizations

## 📊 Comprehensive Testing Protocol

### Experimental Design Requirements

- **Minimum 30 measurements** per test condition for statistical validity
- **Document all environmental variables:** Temperature, humidity, time of day, interference sources
- **Controlled methodology:** Same device orientation, same measurement procedure

### Step 1: Comprehensive RSSI Analysis

For your chosen environment, collect data at the following distances:
- **Test distances:** 1m, 2m, 3m, 5m, 7m, 10m, 15m (extend if possible)
- **Sample size:** 30 RSSI measurements per distance

### Step 2: Advertising Parameter Impact Study

Test different transmit powers at **multiple distances**:

```cpp
BLEDevice::setPower(ESP_PWR_LVL_N12); // -12dBm
BLEDevice::setPower(ESP_PWR_LVL_N0);  // 0dBm  
BLEDevice::setPower(ESP_PWR_LVL_P9);  // +9dBm
```

**For each power configuration:**
- Collect 30 RSSI measurements per distance
- Calculate RSSI stability (standard deviation)
- Analyze signal consistency

## 📊 Statistical Analysis Requirements

### Required Statistical Measures

- **Mean and Standard Deviation** for all RSSI measurements
- **95% Confidence Intervals** for distance vs RSSI relationships
- **Correlation Coefficients** between distance and RSSI
- **Path Loss Exponent** calculation using linear regression

### Path Loss Model Fitting

Fit your data to the log-distance path loss model:

```
RSSI(d) = RSSI₀ - 10n·log₁₀(d/d₀) + Xσ
```

**Where:**
- `RSSI₀` = reference RSSI at distance d₀ (typically 1m)
- `n` = path loss exponent
- `Xσ` = zero-mean Gaussian random variable (dB)

**Compare your calculated path loss exponent to theoretical values:**
- Free space: n = 2
- Indoor environments: n = 2-4
- Obstructed environments: n = 3-5

## 📈 Data Visualization Requirements

Create the following plots using Python, MATLAB, R, or advanced Excel:

1. **RSSI vs Distance** scatter plot with fitted path loss model and confidence intervals
2. **Box plots** showing RSSI distribution at each distance
3. **Error bar plots** with 95% confidence intervals
4. **Residual plot** for path loss model validation
5. **Configuration comparison** showing RSSI vs advertising parameters

## 📋 Deliverables

Submit the following components:

- [ ] **Raw data files** (CSV format with metadata)
- [ ] **Analysis scripts/code** used for statistics and plotting
- [ ] **All required statistical plots** and model fitting results
- [ ] **Path loss model comparison** with theoretical values
- [ ] **Technical report (1-2 pages)** including:
  - Experimental methodology
  - Statistical analysis results
  - Path loss model evaluation
  - Discussion of findings and implications

---

## 🥚 Part 4 – BLE Egg Hunt _(Bonus for Everyone)_

### 🎯 Learning Objectives
- Practice real-world BLE scanning
- Analyze unknown BLE devices
- Apply signal strength for location finding

### 📋 Hunt Strategy

#### Step 1: Systematic Scanning
- Use your BLE scanner app in "scan" mode
- Look for devices with names starting with "Egg-"
- Check manufacturer data and service UUIDs for clues

#### Step 2: Signal Strength Triangulation
- Use RSSI values to estimate distance
- Walk around to find strongest signal location
- Document approximate location

#### Step 3: Data Analysis
For each found beacon, record:
- Device name
- RSSI at closest approach
- Approximate location
- Any special data in advertisements
- Time of discovery

### ✅ Part 4 Deliverables
- [ ] Screenshots of each discovered beacon
- [ ] Location map or description
- [ ] Analysis of any patterns in the data

---

## 📦 Final Submission Requirements

### File Structure

#### Undergraduate Students:
```
A1_GroupXX_Undergraduate/
├── Part1_Broadcaster/
│   ├── Part1_Static.ino
│   ├── Part1_Dynamic.ino
│   ├── Part1_Screenshot.jpg (or .png)
│   └── Part1_Explanation.txt
├── Part2_Service/
│   ├── Part2_Implementation.ino
│   ├── Part2_Screenshots.jpg (or .png)
│   └── Part2_Design_Document.pdf
├── Part4_Egghunt.pdf         # (Optional bonus)
└── README.txt
```

#### Graduate Students:
```
A1_GroupXX_Graduate/
├── Part1_Broadcaster/
│   ├── Part1_Static.ino
│   ├── Part1_Dynamic.ino
│   ├── Part1_Screenshot.jpg (or .png)
│   └── Part1_Explanation.txt
├── Part3_Performance/
│   ├── Technical_Report.pdf
│   ├── Raw_Data.csv
│   ├── Analysis_Scripts/
│   └── Plots/
├── Part4_Egghunt.pdf         # (Optional bonus)
└── README.txt
```

### README.txt Template
```
Assignment A1 - BLE Exploration
Group XX: [Your Group Number]
Track: [Undergraduate / Graduate]

Team Members:
- Student 1 Name (ID: xxxxxxx) - [Undergraduate/Graduate]
- Student 2 Name (ID: xxxxxxx) - [Undergraduate/Graduate]

Work Distribution:
- Part 1 (BLE Broadcaster): [Who did what]
- Part 2 (Custom GATT Service): [Undergraduate only - who did what]  
- Part 3 (Performance Analysis): [Graduate only - who did what]
- Part 4 (Egg Hunt): [If attempted - who did what]

Project Summary:
Part 2 Service Description: [Undergraduate: Brief description of your custom service]
Part 3 Environment: [Graduate: Testing environment chosen and why]

Additional Notes:
- [Challenges faced and how you solved them]
- [Interesting observations or discoveries]
- [Questions for grader or suggestions for improvement]

Testing Environment:
- Location: [Where you conducted testing]
- Phone/Device model: [Your BLE scanner device]
- Software versions: [Arduino IDE, BLE apps used]
- Date completed: [When you finished each part]

Special Instructions:
- [Any special setup needed to test your code]
- [Known limitations or issues]
- [Additional files or dependencies]
```

### Grading Rubric

#### Undergraduate Track
| Component | Points | Description |
|-----------|--------|-------------|
| Part 1 - Implementation & Documentation | 40 | Working broadcaster with clear documentation (static + dynamic) |
| Part 2 - Custom Service Design | 50 | Well-designed GATT service with multiple characteristics |
| Code Quality & Professional Presentation | 10 | Clean code, proper documentation, professional submission |
| **Total** | **100** | |
| Part 4 - Bonus Egg Hunt | +5 | Additional points for beacon discovery |

#### Graduate Track  
| Component | Points | Description |
|-----------|--------|-------------|
| Part 1 - Implementation & Documentation | 30 | Working broadcaster with clear documentation (static + dynamic) |
| Part 3 - Performance Analysis | 60 | Rigorous statistical analysis with publication-quality report |
| Code Quality & Professional Presentation | 10 | Clean code, proper documentation, professional submission |
| **Total** | **100** | |
| Part 4 - Bonus Egg Hunt | +5 | Additional points for beacon discovery |

---

## 📚 Extended Resources

### Recommended BLE Scanner Apps
- **nRF Connect** (Nordic Semiconductor) - Most detailed
- **BLE Scanner** (Bluepixel Technologies) - Simple interface  
- **LightBlue Explorer** (Punch Through) - iOS users

---

## 🆘 Getting Help

### Where to Get Help
- **Teams Discussion Forum:** Post general questions
- **Office Hours:** Bring specific technical problems
- **Lab Sessions:** Get hands-on assistance

### Common Issues and Solutions

**"Library not found" errors:**
- Check library includes are correct

**"Device not found" on phone:**
- Restart ESP32
- Clear Bluetooth cache on phone (Android: Settings → Apps → Bluetooth)
- Try different BLE scanner app

**Connection fails immediately:**
- Ensure only one device tries to connect
- Restart both devices
- Check if ESP32 is already connected to another device

---

**Questions?** Post on Teams with your specific error messages and code snippets for fastest help!