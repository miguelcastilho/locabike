from flask import Flask, request
import os
import smtplib
import json
import logging
import gmail

def send_email(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd

    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    gmail.send_gmail(recipient, subject, body)
#    try:
#    	server = smtplib.SMTP("smtp.gmail.com", 587)
#	server.ehlo()
#	server.starttls()
#	server.login(gmail_user, gmail_pwd)
#	server.sendmail(FROM, TO, message)
#	server.close()
#	print 'successfully sent the mail'
#    except:
#	print 'failed to send mail'



app = Flask(__name__)

port = int(os.getenv("PORT", 9000))

@app.route('/', methods=['POST'])
def root():
    data = request.get_json()

    lon = data['lon']
    lat = data['lat']
    description = data['description']
    recipient = data['recipient']
    user = os.getenv("GMAIL_USER")
    pwd = os.getenv("GMAIL_PASSWORD")

    url = "http://www.google.com/maps/place/{},{}".format(lat, lon)
    body = "Your missing bike has been seen:\n\nDescription: {}\n\nLocation: {}".format(description, url)
    subject = "Your missing bike has been seen!"

    logging.info("Sending email to {}".format(recipient))
    send_email(user, pwd, recipient, subject, body)
    logging.info("Successfully sent email to {}".format(recipient))

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=port)
