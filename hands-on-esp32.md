# 🚀 Getting Started with ESP32-C6 and Arduino IDE

This guide helps you set up your **ESP32-C6 development board** with the **Arduino IDE** and run a basic **blink test** to verify everything is working.

---

## 🧰 Prerequisites

- A computer with internet access
- [Arduino IDE](https://www.arduino.cc/en/software) (version 2.x recommended)
- An ESP32-C6 development board (e.g., ESP32-C6 DevKit)
- USB-C cable

---

## 🔧 Step 1: Install Arduino IDE

1. Visit [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software)
2. Download and install the IDE for your operating system (Windows, macOS, or Linux)

---

## 📦 Step 2: Add ESP32 Board Support

1. Open the Arduino IDE.
2. Go to **File > Preferences**.
3. In the **“Additional Board Manager URLs”** field, paste the following:
```

[https://espressif.github.io/arduino-esp32/package\_esp32\_index.json](https://espressif.github.io/arduino-esp32/package_esp32_index.json)

```
4. Click **OK**.

5. Go to **Tools > Board > Boards Manager**.
6. Search for `esp32`, then click **Install** on **“esp32 by Espressif Systems”**.

---

## 🖥️ Step 3: Select ESP32-C6 Board

1. Go to **Tools > Board > ESP32 Arduino**.
2. Select:
```

ESP32C6 Dev Module

````

⚠️ If you don’t see this board, make sure the ESP32 package is up to date (v3.0.0+ required for ESP32-C6).

---

## 🔌 Step 4: Connect Your ESP32-C6

1. Use a USB-C cable to connect your board to the computer.
2. In the IDE, go to **Tools > Port** and select the appropriate port (e.g., `COM3` or `/dev/cu.usbmodem*`).
3. Under **Tools**, also set:
- **Upload Speed**: `115200`

---

## 💡 Step 5: Run the Blink Test

1. Go to **File > Examples > 01.Basics > Blink**.
2. Replace `LED_BUILTIN` with the appropriate GPIO pin for your board (often `2`, `8`, or `18`):

```cpp
void setup() {
pinMode(8, OUTPUT); // Change 8 to the actual LED pin on your board
}

void loop() {
digitalWrite(8, HIGH);
delay(500);
digitalWrite(8, LOW);
delay(500);
}
````

3. Click the **Upload** button (the right arrow).
4. Wait for the message: `Done uploading`.
5. The on-board LED should blink every half second.

---

## 🛠️ Troubleshooting

* **No port showing up?** Try another USB cable or port. Make sure drivers are installed.
* **Upload stuck on “Connecting...”** Press and hold the **BOOT** button on the ESP32-C6 while it tries to connect.
* **No blinking?** Try GPIO 2, 8, or 18 in the code above to match your dev board’s built-in LED.

---

## ✅ You're Ready!

Your ESP32-C6 is now running its first Arduino sketch! You're ready to explore more examples using BLE, Wi-Fi, LoRa, and sensors.

Happy hacking! 🔧💡
