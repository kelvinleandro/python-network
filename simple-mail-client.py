import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

sender_email = "sender@example.com"
receiver_email = "receiver@example.com"
subject = "Test Email"
body = "This is a test email."
password = ""

# Connect to SMTP server
server = smtplib.SMTP('smtp.gmail.com', 25)
server.ehlo()
server.login(sender_email, password)

# Create message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

# Attaching a image
image_file = 'image.png'
attachment = open(image_file, 'rb')
payload = MIMEBase('application', 'octet-stream')
payload.set_payload(attachment.read())
encoders.encode_base64(payload)
payload.add_header('Content-Disposition', f'attachment; filename={image_file}')
attachment.close()
message.attach(payload)

server.sendmail(sender_email, receiver_email, message.as_string())
server.quit()