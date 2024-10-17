import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to get the IP address of the Raspberry Pi
def get_ip_address():
    try:
        # This will get the IP address of the device by connecting to an external host
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        # Google DNS server used to find the IP
        s.connect(('8.8.8.8', 1))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return f"Unable to get IP address: {e}"

# Function to send an email with the IP address
def send_email(ip_address, to_email):
    try:
        # Email details
        from_email = "effd250@gmail.com"
        password = "flashthedog"
        subject = "Raspberry Pi IP Address"

        # Create the message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add the IP address as the message body
        body = f"The IP address of your Raspberry Pi is: {ip_address}"
        msg.attach(MIMEText(body, 'plain'))

        # Setup the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)

        # Send the email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)

        # Close the connection to the server
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main function
if __name__ == "__main__":
    ip_address = get_ip_address()
    recipient_email = "vsds970@uowmail.edu.au"  
    send_email(ip_address, recipient_email)