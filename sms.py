from flask import Flask
from flask import request
import paramiko
import jsonpath_ng.ext as jp
import os
app = Flask(__name__)

IP=os.getenv("UNIFI_IP")
USER=os.getenv("UNIFI_USER")
PASS=os.getenv("UNIFI_PASSWORD")
AUTH=os.getenv("SMS_AUTH")

def build_client():
  client = paramiko.client.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(IP, username=USER, password=PASS)
  client.exec_command("ifconfig usb0 up")
  return client

def run_command(client, command):
   _stdin, _stdout,_stderr = client.exec_command(f"ssh -y root@$(cat /var/run/topipv6) '/legato/systems/current/bin/cm {command}'")
   return _stdout.read().decode(), _stderr.read().decode()

@app.route('/sms/status', methods=['GET'])
def sms_status():
  
  auth = request.headers.get('auth')

  if not auth or auth != AUTH:
    return "INVALID AUTH", 403
  
  client = build_client()

  out_info, err_info = run_command(client, "info all")
  out_sim, err_sim = run_command(client, "sim info")
  out_temp, err_temp = run_command(client, "temp all")

  client.close()

  out = f"DEVICE INFO:\n{out_info}\n\nSIM INFO:\n{out_sim}\n\nTEMPERATURES:\n{out_temp}"

  return out, 200

@app.route('/sms/retrieve', methods=['GET'])
def sms_retrieve():
  
  auth = request.headers.get('auth')

  if not auth or auth != AUTH:
    return "INVALID AUTH", 403
  
  client = build_client()

  out_count, err_count = run_command(client, "sms count")

  count = out_count.replace("\n", "")
  if count == "0":
     out = "NO STORED MESSAGES"
  else:
     out_list, err_list = run_command(client, "sms list")
     out = f"{count} STORED MESSAGES:\n{out_list}"

  client.close()

  return out, 200

@app.route('/sms/clear', methods=['DELETE'])
def sms_clear():
  
  auth = request.headers.get('auth')

  if not auth or auth != AUTH:
    return "INVALID AUTH", 403
  
  client = build_client()

  run_command(client, "sms clear")

  return "ALL STORED MESSAGES CLEARED", 200
  
@app.route('/sms/send/<number>', methods=['POST'])
def sms_send(number):
  
  auth = request.headers.get('auth')

  if not auth or auth != AUTH:
    return "INVALID AUTH", 403

  content_path = request.args.get('path')
  if content_path:
    json=request.get_json(force=True)
    query=jp.parse(content_path)
    body=query.find(json)[0].value
  else:
    body=request.data.decode('UTF-8')

  client = build_client()

  run_command(client, f"sms send {number} \"{body}\"")

  client.close()

  return "MESSAGE SENT", 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8585)