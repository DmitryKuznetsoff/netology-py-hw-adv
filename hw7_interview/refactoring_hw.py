import email
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List


class MailUser:
    def __init__(self, login: str, pwd: str):
        self.login = login
        self.pwd = pwd

    def get_message(self, recipients: List[str], subject: str, message: str):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        return msg

    def send_message(self, host: str, port: int, msg):
        # identify ourselves to smtp gmail client
        # secure our email with tls encryption
        # re-identify ourselves as an encrypted connection
        client = smtplib.SMTP(host, port)
        client.ehlo().starttls().ehlo()

        client.login(self.login, self.pwd)
        client.sendmail(self.login, self.pwd, msg.as_string())
        client.quit()

    def receive_message(self, host: str, header: str = None):
        mail = imaplib.IMAP4_SSL(host, 993)
        mail.login(self.login, self.pwd)
        mail.list()
        mail.select("inbox")

        criterion = f'(HEADER Subject {header})' if header else 'ALL'
        result, data = mail.uid('search', criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()
        return email_message


if __name__ == '__main__':
    SMTP_HOST = 'smtp.gmail.com'
    IMAP_HOST = 'imap.gmail.com'
    login = ''
    password = ''

    user = MailUser(login, password)
    message = user.get_message(['vasya@email.com', 'petya@email.com'], 'Subject', 'Message')
    user.send_message(SMTP_HOST, 587, message)
    user.receive_message(IMAP_HOST)
