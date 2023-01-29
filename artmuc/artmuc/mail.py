import subprocess, sys, smtplib
import email.utils
from email.message import EmailMessage
from email.headerregistry import Address
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import Template

class Mailer:
    def __init__(self, recipient, type, token="None"):
        self.mx_records = []
        self.mx_values = {'pref' : 0, 'serv' : ''}
        self.recipient = recipient
        self.token = token
        if type == "Validate":
            self.subject = "Email validation!"
        else:
            self.subject = type
        self.htmltext, self.plaintext = Mailer.fileparser(self, type)
        Mailer.nslookup(self)
        Mailer.send(self)
    def nslookup(self):
        domain = self.recipient.split('@')[1]
        p = subprocess.Popen('nslookup -type=mx ' + domain + ' 8.8.8.8', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            line = line.decode().lower()
            if line.find("mail exchanger") != -1 :
                for char in line:
                    if str(char) in "\r\n\t":
                        line = line.replace(char, '')
                if line.find("mx preference") != -1 :
                    mx_parse = line.replace(' ', '').split(",")
                    self.mx_values['pref'] = int(mx_parse[0].split("=")[1])
                    self.mx_values['serv'] = mx_parse[1].split("=")[1]
                else:
                    mx_parse = line.split(" = ")[1].split(" ")
                    self.mx_values['pref'] = int(mx_parse[0])
                    self.mx_values['serv'] = mx_parse[1]
                self.mx_records.append(self.mx_values.copy())
        retval = p.wait()
    def fileparser(self, type):
        if type == "Validate":
            file_html = open('artmuc/templates/mail/confirm.html')
            file_plain = open('artmuc/templates/mail/confirm.txt')
            x1 = Template(file_html.read()).substitute(token=self.token)  #.format(self.token)
            x2 = Template(file_plain.read()).substitute(token=self.token)  #.format(self.token)
            return x1, x2
        #return parsed_plaintext, args.hmessage
    def mx_pref_sortvalue(record):
        return record['pref']
    def send(self):
        mx_records = []
        mx_records=sorted(self.mx_records, key=Mailer.mx_pref_sortvalue)
        server = mx_records[0]['serv']
        smtp_send = smtplib.SMTP(server, 25)
        msg = MIMEMultipart('alternative')#EmailMessage()
        msg['From'] = "Artmuc"
        msg['To'] = self.recipient
        msg['Subject'] = self.subject
        msg.add_header('Content-Type','text/html')
        part2 = MIMEText(self.htmltext, 'html')
        part1 = MIMEText(self.plaintext, 'plain')
        msg.attach(part1)
        msg.attach(part2)
        smtp_send.sendmail("no-reply@artmuc.de", self.recipient, msg.as_string())
        smtp_send.quit()
