from flask import Flask, request, abort, make_response, jsonify, Response
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook/<type>', methods=['POST'])
def webhook(type):
    if type == "twitch":
        print(request.json)
        headers = request.headers
        print(headers)
        if headers["Twitch-Eventsub-Message-Type"] == "webhook_callback_verification":
            challenge = request.json['challenge']
            print(challenge)
            return make_response(challenge, 201)
        elif headers["Twitch-Eventsub-Message-Type"] == "notification":
            message = headers["Twitch-Eventsub-Message-Id"] + headers["Twitch-Eventsub-Message-Timestamp"] + str(request.get_data(True, True, False))
            key = bytes("wh474r3y0ubl1nd", "utf-8")
            data = bytes(message, "utf-8")
            signature = hmac.new(key, data, digestmod=hashlib.sha256)
            expected_signature = "sha256=" + signature.hexdigest()
            print(expected_signature)
            print(headers["Twitch-Eventsub-Message-Signature"])
            if headers["Twitch-Eventsub-Message-Signature"] != expected_signature:
                print("it worked but it didn't get accepted")
                return make_response("failed", 403)
            else:
                print("it worked bitch")
                return make_response("success", 201)
    if type == "youtube":
        print(request.json)
        return make_response("success", 201)

if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True, port=443)