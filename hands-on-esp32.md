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

1. Go to **File > Preferences** (or **Arduino > Settings** on macOS)

2. Paste this URL in **“Additional Board Manager URLs”**:
```

[https://espressif.github.io/arduino-esp32/package\_esp32\_index.json](https://espressif.github.io/arduino-esp32/package_esp32_index.json)

````

3. Click **OK**

4. Go to **Tools > Board > Boards Manager**

5. Search for `esp32`, and install **“esp32 by Espressif Systems”**

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

1. Open **File > Examples > 01.Basics > Blink**

2. Update to use **GPIO 8** (or 2/18 if needed):

```cpp
void setup() {
  pinMode(8, OUTPUT);
}

void loop() {
  digitalWrite(8, HIGH);
  delay(500);
  digitalWrite(8, LOW);
  delay(500);
}
````

3. Upload the code. The LED should blink!

---

## 📡 Step 5: Wi-Fi Scanner

Scan nearby networks and display their signal strength:

```cpp
#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  delay(1000);
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
}

void loop() {}
```

✅ Use this to see Wi-Fi availability and RSSI feedback.

---

## 🌐 Step 6: Wi-Fi Connect and Show IP

Modify and upload this sketch to connect your ESP32 to Wi-Fi:

```cpp
#include <WiFi.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting");

  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }

  Serial.println("\n✅ Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {}
```

✅ Once connected, your ESP32 will print its IP address.

---

## 📲 Step 7: ESP32 as Access Point + Web Page

Turn your ESP32 into a local Wi-Fi network with a web server!

```cpp
#include <WiFi.h>
#include <WebServer.h>

WebServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.softAP("ESP32-Hotspot");

  Serial.print("Hotspot IP: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", []() {
    server.send(200, "text/html", "<h2>🎉 Hello from ESP32!</h2>");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
```

1. Upload this sketch
2. Connect your laptop/phone to the **ESP32-Hotspot**
3. Open browser and go to:
   👉 `http://192.168.4.1`

You should see a web page served by the board!

---

## 🛠️ Troubleshooting

| Issue                          | Fix                                     |
| ------------------------------ | --------------------------------------- |
| No port visible                | Use a different cable or restart IDE    |
| Upload stuck on “Connecting…”  | Hold **BOOT** button during upload      |
| No LED blinking                | Try GPIO 2 or 18 instead of 8           |
| ESP32 doesn’t connect to Wi-Fi | Double-check SSID/password, use 2.4 GHz |

---

## ✅ Summary

In this lab, you:

* Installed Arduino IDE and ESP32 support
* Flashed a **Blink** sketch
* Scanned for Wi-Fi
* Connected to a Wi-Fi network and saw the IP
* Created your own access point + web server

You're now ready for BLE and more advanced networking features!

---

*CSCI-4270 / CSCI-6712 – Wireless Technologies for IoT*
*Dalhousie University*

```
