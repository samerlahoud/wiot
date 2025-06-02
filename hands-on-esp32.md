# 🧪 Lab 1: ESP32-C6 Setup, Blink, and Wi-Fi Experiments

Welcome to your first Wireless IoT lab!  
In this session, you'll:
- Set up your environment for ESP32-C6 development
- Run your first sketch: Blink!
- Experiment with simple Wi-Fi features:
  - Scan nearby networks
  - Connect to Wi-Fi and get an IP
  - Turn your ESP32 into an access point

---

## 🧰 What You Need

- ESP32-C6 development board (e.g., ESP32-C6-DevKitC-1)
- USB-C cable
- Laptop with Arduino IDE
- Wi-Fi network (2.4 GHz)

---

## 🖥️ Step 1: Install Arduino IDE

1. Download and install Arduino IDE from:  
   👉 [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software)

2. Open the IDE after installation.

---

## 📦 Step 2: Install ESP32-C6 Support

1. Go to **Tools > Board > Boards Manager**

2. Search for `esp32`, and install **“esp32 by Espressif Systems”**

3. If you do not find **“esp32 by Espressif Systems”** in the list of boards, follow the [installation tutorial](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).

---

## 🔌 Step 3: Connect Your Board

1. Plug in your ESP32-C6 with the USB-C cable

2. In the IDE:
- **Tools > Board** → Choose:
  ```
  ESP32C6 Dev Module
  ```
- **Tools > Port** → Select your board's port:
  - Windows: `COMx`
  - macOS/Linux: `/dev/cu.*` or `/dev/ttyUSBx`

---

## 💡 Step 4: Blink the LED

In this step, you will upload your **first sketch** (program) to the ESP32-C6 board. This sketch turns an LED on and off at regular intervals — a simple but essential way to test that your development environment is correctly set up.

---

### 🔹 1. Open the Blink Example

1. In Arduino IDE, go to:
```

File > Examples > 01.Basics > Blink

````

2. A new window will open with the example code:
```cpp
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
````

### 🔹 2. Compile and Upload

1. Click the **checkmark button** (✓) to compile the code.

2. Click the **right arrow button** (→) to upload the code to your board.

3. Watch the output at the bottom of the IDE. You should see:

   ```
   Connecting...
   Writing at 0x00001000...
   Done uploading.
   ```

4. After uploading, the onboard LED should start **blinking once per second**.

---

### 🔹 3. Understand the Code

Let’s go line by line:

```cpp
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}
```

* This runs **once** when the board starts.
* It sets LED_BUILTIN as an **output pin**.

```cpp
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(1000);                      // wait for a second
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
  delay(1000);                      // wait for a second
}
```

* This loop runs **forever**.
* It turns the LED **on**, waits 1 second, turns it **off**, waits 1 second — repeating endlessly.

---

### 🔹 4. Modify and Re-upload

Try making the LED blink faster.

Upload the modified code and observe how the blink speed changes.

---

### ✅ Success!

You’ve just:

* Uploaded your first program
* Verified that your board is working
* Practiced editing and testing Arduino code

You're now ready to explore more — including Wi-Fi, sensors, and later, BLE.

## Step 5: Brightspace Quiz

Take the L4.Q1 quiz available on Brightspace.

## 📡 Step 6: Wi-Fi Scanner

Scan nearby networks and display their signal strength:

```cpp
#include <WiFi.h>

void setup() {
  Serial.begin(115200);
}

void loop() {
  delay(10000);
  Serial.println("🔍 Scanning for networks...");

  int n = WiFi.scanNetworks();
  for (int i = 0; i < n; ++i) {
    int rssi = WiFi.RSSI(i);
    String bars = (rssi > -60) ? "📶📶📶" :
                  (rssi > -70) ? "📶📶" :
                                 "📶";
    Serial.printf("%2d: %-20s | RSSI: %3d dBm | %s\n",
      i + 1,
      WiFi.SSID(i).c_str(),
      rssi,
      bars.c_str());
  }
  delay(10000);
}
```

✅ Use this to see Wi-Fi availability and RSSI feedback. Comment the code and analyze the result.

---

## 🌐 Step 7: Simple HTTP Server and Client Communication

To wrap up this hands-on session, we’ll build a simple **HTTP server** using one ESP32 board, and connect to it first with a **smartphone browser**, then with another **ESP32 client**.

This demonstrates how IoT devices can serve data and be queried over the network — just like tiny web servers.

---

### 🅰️ Part 1: Group A sets up an HTTP Server (SoftAP)

This code creates a Wi-Fi Access Point and starts a basic web server that responds with a short message.

```cpp
#include <WiFi.h>
#include <WebServer.h>

WebServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.softAP("GroupA-NET", "12345678", 6); // Use channel 1, 6, or 11 to reduce interference

  Serial.println("📡 Access Point started");
  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", []() {
    server.send(200, "text/html", "<h2>📨 Hello from Group A!</h2>");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
````

After uploading:

* The ESP32 becomes a Wi-Fi hotspot (`GroupA-NET`)
* The IP address is typically `192.168.4.1`

---

### 📱 Part 2: Group B connects using a smartphone

1. On a phone or laptop, go to **Wi-Fi settings**
2. Connect to the network:

   ```
   SSID: GroupA-NET
   Password: 12345678
   ```
3. Open a browser and enter:

   ```
   http://192.168.4.1
   ```

You should see the message from the ESP32 displayed in the browser.

✅ This confirms that the ESP32 is successfully serving content over HTTP.

---

### 🖥️ Part 3: Group B uses their ESP32 as an HTTP client

Now Group B uploads the following sketch to their board. It connects to Group A’s AP and sends an HTTP GET request to fetch the message.

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "GroupA-NET";
const char* password = "12345678";

void setup() {
  Serial.begin(115200);
  delay(3000)
  WiFi.begin(ssid, password);
  Serial.print("Connecting");

  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }

  Serial.println("\n✅ Connected to GroupA-NET!");
  Serial.print("My IP: ");
  Serial.println(WiFi.localIP());

  HTTPClient http;
  http.begin("http://192.168.4.1/"); // Group A’s server
  int code = http.GET();

  if (code > 0) {
    String payload = http.getString();
    Serial.println("📥 Received message:");
    Serial.println(payload);
  } else {
    Serial.printf("❌ Request failed: %s\n", http.errorToString(code).c_str());
  }

  http.end();
}

void loop() {
  // One-time request on setup
}
```

---
## ✅ Summary

In this lab, you:

* Installed Arduino IDE and ESP32 support
* Flashed a **Blink** sketch
* Scanned for Wi-Fi
* Built an HTTP client-server application over WiFi

You're now ready for BLE and more advanced networking features!

---

*CSCI-4270 / CSCI-6712 – Wireless Technologies for IoT*
*Dalhousie University*

```
