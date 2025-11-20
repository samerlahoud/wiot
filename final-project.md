**Course:** CSCI-4270 / CSCI-6712 – Wireless Technologies for the Internet of Things

**Deadline:** 7:00 PM on **December 10, 2025**

**Submission:** Upload as **one zip file** on Brightspace

**Project Teams:** Students must form their project groups (4 students per group) by **Friday, November 21, 2025 at 11:59 PM**. Groups not submitted by the deadline will be assigned randomly.

# Final Project – BLE-Based Luggage Cluster Detection System

## 📡 Project Overview

In this project, you will develop a BLE-based system to detect and monitor a *cluster* of tagged luggage moving together in proximity. The goal is to track whether a set of ESP32-C6 devices, each representing a piece of luggage, remain consistently within a defined short-range distance (e.g., 3 meters) of each other during transport, such as in an airport, train station, or hotel.

The system relies on decentralized BLE advertisement and scanning, where each device periodically broadcasts a randomized ID and scans for neighboring peers. The core logic determines whether the same set of peer devices are detected over time, and whether they maintain consistent relative RSSI, indicating a moving cluster.

This cluster pattern detection allows for use cases like group-based baggage tracking, anomaly alerts when an item strays too far, and possible integration with a smartphone or relay node for remote status updates.

## 🧪 Project Features and Evaluation Goals

### Core Functionality

* Each ESP32-C6 acts as both advertiser and scanner
* Devices log neighbor IDs with timestamps and RSSI
* Cluster detection logic maintains a sliding time window and checks for:

  * Consistent presence of the same device set
  * RSSI proximity threshold met for all members
* Optional LED or OLED output when cluster is broken
* Optionally simulate movement events or location transitions to test response

### Experimental Evaluation

* **Proximity calibration**:

  * Measure RSSI vs distance between ESP32-C6 devices
  * Define RSSI threshold for clustering

* **Cluster detection accuracy**:

  * Deploy 3–4 devices and move them in simulated cluster patterns
  * Introduce deviations and log detection of cluster loss events
  * Log false positive and false negative rates

* **Temporal stability**:

  * Analyze cluster detection stability over time (e.g., 5-minute intervals)

* **Energy profiling**:

  * Estimate battery life using the [Nordic Online Power Profiler](https://devzone.nordicsemi.com/power/w/opp/2/online-power-profiler-for-bluetooth-le)
  * Compare trade-offs between scan/advertise interval and detection accuracy

* **Data offloading**:

  * Store all logs locally on device
  * Upload logs in bulk over Wi-Fi at the end of the deployment window

## 📦 Required Deliverables

| Component               | Description                                                                |
| ----------------------- | -------------------------------------------------------------------------- |
| `firmware/`             | Source code for BLE scan/advertise logic and cluster detection              |
| `data/`                 | Logs of RSSI, timestamp, peer ID, cluster detection status                  |
| `plots/`                | RSSI vs distance, detection performance metrics, energy consumption curves |
| `report.pdf`            | Max 5 pages: methodology, system design, results, and discussion          |
| `demo.mp4` *(optional)* | Video showing cluster behavior and alert triggering                         |

## 📈 Evaluation Criteria

| Category                                      | Points  |
| --------------------------------------------- | ------- |
| BLE advertising and scanning functionality    | 20      |
| Cluster detection logic and stability analysis | 20      |
| RSSI calibration and proximity classification | 20      |
| Detection accuracy and false alarm analysis   | 20      |
| Energy analysis and deployment considerations | 20      |
| **Total**                                     | **100** |

