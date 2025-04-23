# email_utils.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os

from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSKEY = os.getenv("APP_PASSKEY")
LOG_EMAIL = os.getenv("LOG_EMAIL")

def getEmailBody(body, email):
  corpo = body
  msg = MIMEMultipart("alternative")
  msg['Subject'] = '🚨 Nova vaga publicada!'
  msg['From'] = SENDER_EMAIL
  msg['To'] = email
  msg.attach(MIMEText(corpo, "html"))
  return msg

def sendEmails(titulo: str, body: str, emails: list):
  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
      smtp.login(SENDER_EMAIL, APP_PASSKEY)
      for email in emails:
        msg = getEmailBody(body, email)
        smtp.send_message(msg)
        print(f"[EMAIL ENVIADO] [{email}] - {titulo}")

def sendLogEmail(totalHiring: int, lastHiring: str):
  agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
  corpo = f"""
  <html>
    <body>
      <h3>✅ Execução do Bot - Relatório de Auditoria</h3>
      <ul>
        <li><strong>Data/Hora:</strong> {agora}</li>
        <li><strong>Total de vagas encontradas:</strong> {totalHiring}</li>
        <li><strong>Última vaga analisada:</strong> <a href="{lastHiring}">{lastHiring}</a></li>
      </ul>
      <p>Log de auditoria para check de funcionamento.</p>
    </body>
  </html>
  """
  msg = MIMEMultipart("alternative")
  msg['Subject'] = '📄 Auditoria - Nenhuma nova vaga'
  msg['From'] = SENDER_EMAIL
  msg['To'] = LOG_EMAIL
  msg.attach(MIMEText(corpo, "html"))

  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
      smtp.login(SENDER_EMAIL, APP_PASSKEY)
      smtp.send_message(msg)
      print("[EMAIL AUDITORIA ENVIADO]")
