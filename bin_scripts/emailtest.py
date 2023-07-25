import smtplib
#import mail
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

s = smtplib.SMTP(host='smtp.gmail.com', port = 587)
address = 'niklundgren12@gmail.com'
passw = 'Scooter#12!'
message_text = 'job finished'
s.starttls()
s.login(address,passw)
msg = MIMEMultipart()
message = 'The lammps calculation is finished'
msg['From']= address
msg['To'] = address
msg['Subject'] = 'Job Completion'
msg.attach(MIMEText(message,'plain'))
s.send_message(msg)
