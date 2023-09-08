import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
import datetime

def e_mail(mail_dict, days_left):
    email_address = mail_dict['email']
    reminder_name = mail_dict['reminder_name']
    user_name = mail_dict['name']  
    start_date = mail_dict['start_date'] 
    end_date = mail_dict['end_date'] 
    description = mail_dict['description'] 
    
    html = Template(Path('./email.html').read_text())
    email = EmailMessage()
    email['from'] = 'Reminder'
    email['to'] = email_address
    email['subject'] = 'Reminder Test!!!'

    email.set_content(html.substitute(name = user_name,
                                      reminder = reminder_name,
                                      start = start_date,
                                      due = end_date,
                                      purpose = description,
                                      days = days_left),
                        'html')

    with smtplib.SMTP(host='smtp.gmail.com', port = 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('kiingjay77@gmail.com', 'ioiwirwvfyiefwgf')
        smtp.send_message(email)
        print ('All done!!!')

def due_mail(mail_dict):
    email_address = mail_dict['email']
    user_name = mail_dict['name']  
    start_date = mail_dict['start_date'] 
    end_date = mail_dict['end_date'] 
    description = mail_dict['description'] 
    
    html = Template(Path('./due_email.html').read_text())
    email = EmailMessage()
    email['from'] = 'Reminder'
    email['to'] = email_address
    email['subject'] = 'Reminder Test!!!'

    email.set_content(html.substitute(name = user_name,
                                      email= email_address,
                                      start = start_date,
                                      due = end_date,
                                      purpose = description),
                        'html')

    with smtplib.SMTP(host='smtp.gmail.com', port = 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('kiingjay77@gmail.com', 'ioiwirwvfyiefwgf')
        smtp.send_message(email)
        print ('All done!!!')        

def period_calculator(due_date):
  start_date = datetime.datetime.now().date()
  difference_in_days = due_date - start_date
  return difference_in_days.days


