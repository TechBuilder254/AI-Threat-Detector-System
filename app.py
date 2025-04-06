import subprocess
import os
import pickle
import tempfile  # Import tempfile for creating temporary files
import re  # Import re for IP range validation
from flask import Flask, render_template, request
import pandas as pd
from werkzeug.utils import secure_filename
from utils.parse_nmap import parse_nmap_file

app = Flask(__name__)

# Set upload folder and allowed file types
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the trained model
with open('model/threat_model.pkl', 'rb') as f:
    model = pickle.load(f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_ip_range(ip_range):
    """Validate the IP range or target."""
    ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?$"  # Matches IP addresses and CIDR ranges
    return re.match(ip_pattern, ip_range) is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_network', methods=['POST'])
def analyze_network():
    try:
        if 'nmap_file' in request.files:
            file = request.files['nmap_file']
            if file.filename == '':
                return render_template('index.html', anomalies=[], message="No file selected.")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Parse the uploaded Nmap file
                scan_results = parse_nmap_file(file_path)

                if scan_results.empty:
                    return render_template('index.html', anomalies=[], message="No data found in the Nmap file.")

                # Process results
                anomalies = process_scan_results(scan_results)
                return render_template('index.html', anomalies=anomalies)

        elif 'ip_range' in request.form:
            ip_range = request.form['ip_range']
            if not ip_range or not validate_ip_range(ip_range):
                return render_template('index.html', anomalies=[], message="Invalid IP range or target.")

            nmap_output_path = run_nmap_scan(ip_range)

            if nmap_output_path is None:
                return render_template('index.html', anomalies=[], message="Error running Nmap scan.")

            # Parse the Nmap scan output
            scan_results = parse_nmap_file(nmap_output_path)

            if scan_results.empty:
                return render_template('index.html', anomalies=[], message="No data found in the Nmap scan.")

            # Process results
            anomalies = process_scan_results(scan_results)
            return render_template('index.html', anomalies=anomalies)

        return render_template('index.html', anomalies=[], message="Invalid request.")
    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', anomalies=[], message=f"Unexpected error: {e}")

def run_nmap_scan(ip_range):
    """Run Nmap scan on a specified IP range and return the path to the output XML file."""
    try:
        print(f"Running Nmap scan for IP range: {ip_range}")  # Debug log
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_file:
            temp_file_path = temp_file.name

        # Run the Nmap scan command and save output to the temporary file
        cmd = ["nmap", "-oX", temp_file_path, ip_range]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check for errors in the scan
        if result.stderr:
            raise Exception(f"Nmap error: {result.stderr}")

        print(f"Nmap scan completed. Output saved to: {temp_file_path}")  # Debug log
        return temp_file_path  # Return the path to the temporary file
    except Exception as e:
        print(f"Error running Nmap scan: {e}")
        return None

def process_scan_results(scan_results):
    """Process the scan results and return a list of anomalies."""
    anomalies = []
    for _, row in scan_results.iterrows():
        features = pd.DataFrame([{
            'open_ports': len(scan_results[scan_results['ip'] == row['ip']]['port']),
            'unique_services': len(scan_results[scan_results['ip'] == row['ip']]['service'].unique())
        }])
        threat = "Threat" if model.predict(features)[0] == 1 else "Safe"
        anomalies.append({
            "ip": row['ip'],
            "port": row['port'],
            "protocol": row['protocol'],
            "state": row['state'],
            "service": row['service'],
            "threat": threat
        })
    print("Processed anomalies:", anomalies)  # Debug log
    return anomalies

if __name__ == '__main__':
    app.run(debug=True)