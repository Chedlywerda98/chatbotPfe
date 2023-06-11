from flask import Flask, render_template, request, jsonify
from chat import get_response
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
app = Flask(__name__)
CORS(app)

def train():
    subprocess.run(["python", "train.py"])

def chat():
    subprocess.run(["python", "chat.py"])

# Email Configuration
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "chedlywerda6@gmail.com"
SENDER_PASSWORD = "kronceishwojpcvx"
RECIPIENT_EMAIL = "chedly.werda@esprit.tn"

def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print("Error sending email:", str(e))

@app.route("/", methods=['GET'])
def index_get():
    return render_template("base.html")

@app.route('/runapp', methods=['POST'])
def run_app_handler():
    train()
    return jsonify({'message': 'App.py code executed successfully!'})


@app.route("/predict", methods=['POST'])
def predict():
    text = request.json.get("message")
    response = get_response(text)
    message = {"answer": response}

    if response == "Je ne comprends pas...":
        subject = "Bot Response - Je ne comprends pas..."
        email_message = f"The bot responded with 'Je ne comprends pas...' for the user input: '{text}'"
        send_email(subject, email_message)

    return jsonify(message)

if __name__ == "__main__":
    train()
    app.run(debug=True)
