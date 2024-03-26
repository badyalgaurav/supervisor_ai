import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Get the absolute path of the directory containing the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the name of the directory containing the model file
BASE_ADDRESS = "HTML_TEMPLATE"

# Construct the absolute path to the model file
html_template_path = os.path.join(script_dir, BASE_ADDRESS, "email_template.html")


def send_video_email(receiver_emails, video_file_path):
    sender_email = 'servicegemmiz@gmail.com'
    app_password = 'nbtdwgfsarrzzybk'
    # receiver_emails = ['badyalgaurav0@gmail.com', 'sahilloria34@gmail.com']
    subject = 'ALERT from Safety eye pro, suspicious activity recorded'
    # video_file_path = 'D:\\var\\www\\output_camera_1\\20240218\\output_camera_1_20240218183448.mp4'
    # Read the HTML template file
    with open(html_template_path, 'r') as file:
        html_content = file.read()

    # Compose the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_emails)
    msg['Subject'] = subject

    # Add message body
    # msg.attach(MIMEText(message, 'plain'))

    # Attach video file
    with open(video_file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    # part.add_header('Content-Disposition', f'attachment; filename= {video_file_path}')
    part.add_header('Content-Disposition', f'attachment; filename= SAFETEYEPRO.mp4')
    msg.attach(part)
    # Attach HTML content to the email
    msg.attach(MIMEText(html_content, 'html'))
    # Set up SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Log in to SMTP server with app password
    server.login(sender_email, app_password)

    # Send email
    server.sendmail(sender_email, receiver_emails, msg.as_string())

    # Close SMTP connection
    server.quit()

# send_video_email(sender_email, app_password, receiver_emails, subject, video_file_path, html_content)
