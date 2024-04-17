import random
import ssl
import smtplib
from email.mime.text import MIMEText

# generate otp for creating the otp
def generate_otp(length=4):
    return ''.join(random.choices('0123456789', k=length))

def createotpforuser(email):
    otp = generate_otp()
    subject = 'Your OTP for Registration with Socialmedia'
    message = f'Your OTP is: {otp}'
    from_email = 'hirexjobs66@gmail.com'
    recipient_list = [email]
    # Create the email body
    email_body = f"{message}\n\nThank you for registering!"
    mailresponse=send_mail(subject, from_email, recipient_list,email_body)
    if mailresponse == (True, 'Email sent successfully.'):
        return {"otp":otp}
    else:
        # If the email sending failed, return the response from the send_mail function
        return mailresponse



def send_mail(subject, from_email, recipient_list,email_body):
    # Create a secure SSL context without certificate verification
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = 'hirexjobs66@gmail.com'
    smtp_password = 'ikujfsgwgmlgetsn'

     # Create the message
    msg = MIMEText(email_body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(recipient_list)


    try:
        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=ssl_context)
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, recipient_list, msg.as_string())
        return True, 'Email sent successfully.'
    except Exception as e:
        # Handle any exceptions or errors here
        print(f"Error sending email: {e}")
        return False, f"Failed to send email: {e}"



    