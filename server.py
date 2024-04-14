#!/usr/bin/python3
from flask import Flask, request, jsonify
import subprocess
import shlex

app = Flask(__name__)

zones_db = []


def arpa_to_ip(arpa):
    # Strip the .in-addr.arpa suffix
    if arpa.endswith(".in-addr.arpa."):
        arpa = arpa.replace(".in-addr.arpa.", "")
    # Split the remaining string by the dots and reverse the segments
    ip_parts = arpa.split(".")
    ip_parts.reverse()
    # Join the segments back into a standard IP address format
    ip_address = ".".join(ip_parts)
    return ip_address

@app.route('/api/v1/servers/localhost/zones', methods=['GET', 'POST'])
def handle_zones():
    if request.method == 'GET':
        return jsonify(zones_db), 200
    elif request.method == 'POST':
        zone_data = request.get_json()
        zones_db.append(zone_data)  # Add new zone to the database
        return jsonify({'status': 'success', 'message': 'Zone added successfully'}), 201


@app.route('/api/v1/servers/localhost/zones/<zone>', methods=['GET','PATCH'])
def update_ptr(zone):
    if request.method == 'GET':
        return jsonify([]), 200
    # Extract data from request
    data = request.get_json()
    try:
        # Process each rrset, though typically only one for PTR updates
        for rrset in data.get('rrsets', []):
            if rrset['type'] == "PTR":
                ip_address = arpa_to_ip(rrset['name'])
                record_content = rrset['records'][0]['content']  # assuming one PTR record per rrset
                # Construct the command with sanitized inputs
                command = f"/app/cloudflare-rdns --config=/app/CloudflareRDNS.yaml --ip={shlex.quote(ip_address)} --set-rdns={shlex.quote(record_content)}"
                print(command)
                # Execute the command
                output = subprocess.check_output(command, shell=True, text=True)
                return jsonify({'status': 'success', 'output': output}), 204
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 400

    return jsonify({'status': 'error', 'message': 'No valid PTR record found'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8981)

