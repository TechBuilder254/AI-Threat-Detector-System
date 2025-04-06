import xml.etree.ElementTree as ET
import pandas as pd

def parse_nmap_file(file_path):
    try:
        # Parse the XML file
        print(f"Parsing Nmap file: {file_path}")  # Debugging log
        tree = ET.parse(file_path)
        root = tree.getroot()

        data = []
        for host in root.findall('host'):
            # Extract IP address
            ip_elem = host.find("address[@addrtype='ipv4']")
            ip = ip_elem.get('addr') if ip_elem is not None else None

            # Skip hosts with no IP address
            if not ip:
                continue

            # Iterate through ports
            for port in host.findall(".//port"):
                port_id = port.get('portid')
                protocol = port.get('protocol')

                # Extract port state
                state_elem = port.find('state')
                state = state_elem.get('state') if state_elem is not None else None

                # Extract service information
                service_elem = port.find('service')
                service = service_elem.get('name') if service_elem is not None else None

                # Append data to the list
                data.append({
                    "ip": ip,
                    "port": port_id,
                    "protocol": protocol,
                    "state": state,
                    "service": service
                })

        # Return as a pandas DataFrame
        if data:
            print(f"Parsed {len(data)} entries from the Nmap XML file.")  # Debugging log
            return pd.DataFrame(data)
        else:
            print("No data found in the Nmap XML file.")
            return pd.DataFrame()  # Return empty DataFrame if no data is found

    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return pd.DataFrame()  # Return empty DataFrame on XML parsing error
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return pd.DataFrame()  # Return empty DataFrame if file is not found
    except Exception as e:
        print(f"Unexpected error: {e}")
        return pd.DataFrame()  # Return empty DataFrame on any other error