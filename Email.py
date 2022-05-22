from email.mime.text import MIMEText
from email.header import Header
import datetime
import smtplib
from datetime import datetime
from pytz import timezone
from json import load

class Email():
    def __init__(self):
        self._smtp_server="smtp.exmail.qq.com"

    @property
    def sender(self):
        return self._sender
    
    @sender.setter
    def sender(self, value):
        self._sender = value
    
    @property
    def receivers(self):
        return self._receivers
    
    @receivers.setter
    def receivers(self, value):
        if(len(value)>1):
            self._receivers = '; '.join(value)
        else:
            self._receivers = value[0]

    @property
    def password():
        raise ValueError("Password Not Accessable.")

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def server(self):
        return self._smtp_server

    @server.setter
    def server(self, value):
        self._smtp_server = value

    def load_config(self, path):
        with open(path) as f:
            payload = load(f)
        for key,val in payload.items():
            setattr(self, key, val)

    def send(self, subject, message):
        try:
            time = datetime.now(timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")
            msg = MIMEText(message + f"\n{time}", "plain")
            msg['From'] = self._sender
            msg['To'] = self._receivers
            msg['Subject']=Header(f'{subject} Notification','utf-8')
            server=smtplib.SMTP_SSL(self._smtp_server,465)		
            server.login(self._sender,self._password)
            server.sendmail(self._sender,self._receivers,msg.as_string())
            server.quit()
            return 0
        except:
            return 1