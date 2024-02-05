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
  
@app.route('/sms/send/<number>', methods=['POST'])
def sms_send(number):
  
  auth = request.headers.get('auth')

  if not auth or auth != AUTH:
    return "Invalid auth", 403

  client = paramiko.client.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(IP, username=USER, password=PASS)

  content_path = request.args.get('path')
  if content_path:
    json=request.get_json(force=True)
    query=jp.parse(content_path)
    body=query.find(json)[0].value
  else:
    body=request.data.decode('UTF-8')

  client.exec_command("ifconfig usb0 up")
  client.exec_command(f"ssh -y root@$(cat /var/run/topipv6) '/legato/systems/current/bin/cm sms send {number} \"{body}\"'")
  client.close()

  return "Message sent", 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8585)