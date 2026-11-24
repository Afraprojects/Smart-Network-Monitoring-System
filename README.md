# Smart Network Monitoring and Fault Detection System

A Python-based network monitoring application that monitors device connectivity and network performance through a web dashboard.

## Features

- Monitor multiple IP addresses and devices.
- Detect ONLINE and OFFLINE device status.
- Measure network latency.
- Calculate packet loss.
- Store monitoring history using SQLite.
- Generate alerts when devices go offline or recover.
- Display network performance charts.
- View network health summary and device status.
- Visualize monitored devices through a network topology dashboard.

## Technologies Used

- **Programming Language:** Python
- **Backend:** Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Charts:** Chart.js
- **Network Monitoring:** ICMP Ping

## Project Structure

```text
SmartNetworkMonitor/
│
├── app.py
├── monitor.py
├── database.py
├── requirements.txt
├── start_project.bat
├── .gitignore
│
└── templates/
    └── index.html
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Afraprojects/Smart-Network-Monitoring-System.git
```

### 2. Open the project folder

```bash
cd Smart-Network-Monitoring-System
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Project

Open two terminals inside the project folder.

**Terminal 1 – Start Network Monitoring**

```bash
python monitor.py
```

**Terminal 2 – Start Flask Dashboard**

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000/

Alternatively, on Windows, double-click `start_project.bat` after installing the dependencies.

## How It Works

1. The monitoring script sends ping requests to configured IP addresses.
2. It collects device status, latency, and packet information.
3. Monitoring records are stored in the SQLite database.
4. Network status changes trigger fault and recovery alerts.
5. Flask retrieves the stored information and displays it on the dashboard.

## Important Note

This project uses ICMP ping to check device reachability. A device may appear offline if its network blocks ICMP requests, even when other services are working.

## Project Goal

To develop a simple network monitoring solution that helps users observe device connectivity, identify network interruptions, and understand basic network performance.

---

**Developed as a practical learning project using Python and web technologies.**