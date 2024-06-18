from flask import Flask, request, jsonify
import requests
from urllib.parse import quote
from json import loads,dumps

app = Flask(__name__)

# {
#     "receiver": "",
#     "status": "firing",
#     "alerts": [
#         {
#             "status": "firing",
#             "labels": {
#                 "alertname": "TestAlert",
#                 "instance": "Grafana"
#             },
#             "annotations": {
#                 "summary": "[ALERT] ABOVEABOVE"
#             },
#             "startsAt": "2023-05-24T23:22:37.405950092Z",
#             "endsAt": "0001-01-01T00:00:00Z",
#             "generatorURL": "",
#             "fingerprint": "57c6d9296de2ad39",
#             "silenceURL": "http://apollo.pajak.io:3000/alerting/silence/new?alertmanager=grafana\u0026matcher=alertname%3DTestAlert\u0026matcher=instance%3DGrafana",
#             "dashboardURL": "",
#             "panelURL": "",
#             "values": null,
#             "valueString": "[ metric='foo' labels={instance=bar} value=10 ]"
#         }
#     ],
#     "groupLabels": {},
#     "commonLabels": {
#         "alertname": "TestAlert",
#         "instance": "Grafana"
#     },
#     "commonAnnotations": {
#         "summary": "[ALERT] ABOVEABOVE"
#     },
#     "externalURL": "http://apollo.pajak.io:3000/",
#     "version": "1",
#     "groupKey": "{alertname=\"TestAlert\", instance=\"Grafana\"}2023-05-24 23:22:37.405950092 +0000 UTC m=+152.618128021",
#     "truncatedAlerts": 0,
#     "orgId": 1,
#     "title": "[FIRING:1]  (TestAlert Grafana)",
#     "state": "alerting",
#     "message": "**Firing**\n\nValue: [no value]\nLabels:\n - alertname = TestAlert\n - instance = Grafana\nAnnotations:\n - summary = [ALERT] ABOVEABOVE\nSilence: http://apollo.pajak.io:3000/alerting/silence/new?alertmanager=grafana\u0026matcher=alertname%3DTestAlert\u0026matcher=instance%3DGrafana\n"
# }

@app.route('/send-message', methods=['GET','POST'])
def send_message():
    try:
        data = request.get_json()
        message = f"""{"🔴" if data['status'] == "firing" else "🟢"} {data['title']}\n\n{data['message']}"""
        url = "http://wa.sicoding.id/send-message"
        number = request.args.get('number')
        if number is None:
            return jsonify({'message': 'number not found'})
        # payload = 'message=Download%20File%20Stopped&number=6287722086621'
        payload = 'message=' + quote(message) + '&number=' + number
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({'message': 'error'})
    
@app.route('/send-group-message', methods=['GET','POST'])
def send_group_message():
    try:
        data = request.get_json()
        # message = f"""{"🔴" if data['status'] == "firing" else "🟢"} {data['title']}\n\n{data['message']}"""
        print(data)
        group = request.args.get('group')
        percentagevalue = request.args.get('percentagevalue')
        try:
            if percentagevalue is not None and percentagevalue == "true":
                message = f"""{"🔴" if data['status'] == "firing" else "🟢"} {data['commonAnnotations']['summary']} ({"{:.2f}".format((data['alerts'][0]['values']['B'])*100)}%)"""
            else:
                message = f"""{"🔴" if data['status'] == "firing" else "🟢"} {data['commonAnnotations']['summary']} ({"{:.2f}".format(data['alerts'][0]['values']['B'])}%)"""
        except Exception as f:
            group = "My System Notification"
            message = dumps(data)

        # group = "My System Notification"
        if group is None:
            return jsonify({'message': 'group not found'})

        print(group, message)
        url = "http://wa.sicoding.id/send-group-message"
        # payload = 'message=Download%20File%20Stopped&name=6287722086621'
        payload = 'message=' + quote(message) + '&name=' + group
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        return jsonify(data)
    except Exception as e:
        print('error : '+str(e))
        return jsonify({'message': 'error : '+str(e)})

    
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000)
    # app.run(host='0.0.0.0', port=8001, debug=True)
