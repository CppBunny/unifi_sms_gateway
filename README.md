# Unifi SMS Gateway

This is a simple Python API that allows you to send SMS messages using a Unifi LTE Pro.


# Usage

Docker and a reverse proxy are recommended.

## Environment variables

* UNIFI_IP: IP of your LTE Pro
* UNIFI_USER: your Unifi Network SSH username, can be found in 'Network/System/Advanced'
* UNIFI_PASSWORD: your Unifi Network SSH password, can be found in 'Network/System/Advanced'
* SMS_AUTH: API token

## Headers

### auth

Put your API token here when making requests.

## Requests

### GET /sms/status

Gets the device info, sim info and temperatures.

### GET /sms/retrieve

Retrieves all stored SMS messages.

### DELETE /sms/clear

Clears all stored SMS messages.

### POST /sms/send/<number>

Sends the request body to the specified number, a query parameter named 'path' can be specified to select a key from a JSON string using JSONPATH.