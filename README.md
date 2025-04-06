# 🛡️ AI Threat Detector System

This project is an AI-powered cybersecurity threat detection system that analyzes Nmap scan results (either from uploaded files or live scans), detects anomalies using a trained machine learning model, and classifies each host as either a **Threat** or **Safe**.

## 📁 Project Structure

```
AI Threat Detector System/
│
├── app.py                    # Flask web app for threat analysis
├── model/
│   └── threat_model.pkl      # Pre-trained ML model for detection
├── uploads/                  # Folder for storing uploaded files
├── templates/
│   └── index.html            # Web interface
├── utils/
│   └── parse_nmap.py         # Parses Nmap XML output
├── requirements.txt          # Python dependencies
└── README.md                 # You are here
```

---

## ✅ Features

- Upload Nmap `.xml` file to detect threats
- Run live Nmap scans by entering an IP range
- Uses ML model to predict threats
- Simple and intuitive web interface

---

## ⚙️ Installation Guide

Follow these steps **exactly** to avoid errors:

### 1. 🔽 Clone the Repository

```bash
git clone https://github.com/yourusername/ai-threat-detector.git
cd "AI Threat Detector System"
```

### 2. 🐍 Set Up a Virtual Environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate   # For Windows
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. 🔍 Install Nmap (required)

You **must** have Nmap installed and added to your system's PATH.

- Download from: https://nmap.org/download.html
- After installation, test by running:
  
```bash
nmap --version
```

---

## 🚀 Running the App

Once everything is installed:

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

---

## 🧪 How to Use

### 🔹 Option 1: Upload an Nmap XML File

1. Use Nmap to scan any IP or network and save output as `.xml`:
   ```bash
   nmap -oX scan_output.xml <target>
   ```

2. Upload this `scan_output.xml` on the web interface.

---

### 🔹 Option 2: Run Live Scan

1. Enter an IP address or range (e.g., `192.168.1.1/24`)
2. Click **Scan** to perform a live Nmap scan and see threat results.

---

## 🧠 How It Works

- Parses Nmap scan results
- Extracts features (open ports, services)
- Uses a pre-trained ML model (Random Forest or Logistic Regression)
- Classifies each IP as **Threat** or **Safe**

---

## 📌 Important Notes

- Always make sure the Nmap XML files are valid and correctly formatted.
- The system **only accepts** `.xml` files exported from Nmap.
- For live scan, internet or LAN access is required depending on the IPs scanned.

---

## 🤖 Tech Stack

- **Python**
- **Flask** for web interface
- **Scikit-learn** for ML model
- **Nmap** for network scanning
- **pandas** for data handling

---

## 📬 Need Help?

If anything breaks or you need help using it, contact the project owner or check logs printed in your terminal for specific error messages.

---

Let me know if you want a PDF version, a short demo video guide, or if you're planning to host it online—I can help prep that too!
