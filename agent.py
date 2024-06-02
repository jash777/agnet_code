# agent.py

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from rules import *
import logging
import process_monitor

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def agent_status():
    return "<h1>Agent is running</h1>"

@app.route('/apply-rules', methods=['POST'])
def apply_rules():
    rules = request.json.get('rules', [])
    for rule in rules:
        add_iptables_rule(rule['protocol'], rule['destination_port'], rule['action'])
    return jsonify({'status': 'success'})


@app.route('/inbound_rule', methods=['POST'])
def inbound_rules():
    try:
        inbound_rule_data = request.json.get('inbound_rule')
        if inbound_rule_data:
            logging.info("Received inbound rule data: %s", inbound_rule_data)
            if inbound_rule(inbound_rule_data):
                return jsonify({'status': 'success'})
            else:
                return jsonify({'error': 'Failed to add inbound rule'}), 500
        else:
            return jsonify({'error': 'No inbound rule data provided'}), 400
    except Exception as e:
        logging.error("An error occurred while processing inbound rule: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/outbound_rule', methods=['POST'])
def outbound_rules():
    try:
        outbound_rule_data = request.json.get('outbound_rule')
        if outbound_rule_data:
            logging.info("Received inbound rule data: %s", outbound_rule_data)
            if outbound_rule(outbound_rule_data):
                return jsonify({'status': 'success'})
            else:
                return jsonify({'error': 'Failed to add outbound rule'}), 500
        else:
            return jsonify({'error': 'No outbound rule data provided'}), 400
    except Exception as e:
        logging.error("An error occurred while processing outbound rule: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/block_port', methods=['POST'])
def block_port_route():
    port = request.json.get('port')
    if not port:
        return jsonify({"error": "port is required"}), 400
    try:
        port = int(port)
    except ValueError:
        return jsonify({"error": "port must be a number"}), 400
    block_port(port)
    return jsonify({"message": f"port {port} blocked"}), 200

@app.route('/process_results')
def process_results():
    logging.debug(process_monitor.results)
    return jsonify(process_monitor.get_process_data())
    
@app.route('/show_rules', methods=['GET'])
def show_rules_route():
    rules = get_rules()
    return jsonify(rules), 200

@app.route('/flush', methods=['GET','POST'])
def flush_rules_route():
    success = flush_rules()
    if success:
        return jsonify({"message": "Firewall rules flushed successfully"}), 200
    else:
        return jsonify({"error": "Failed to flush firewall rules"}), 500

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
