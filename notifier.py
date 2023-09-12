import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
import datetime
import pandas as pd

def e_mail(mail_dict, days_left):
    email_address = mail_dict['email']
    reminder_name = mail_dict['reminder_name']
    user_name = mail_dict['name']
    start_date = mail_dict['start_date']
    end_date = mail_dict['end_date']
    description = mail_dict['description']

    html = Template(Path('./email.html').read_text())
    email = EmailMessage()
    email['from'] = 'NoReply'
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
    email['from'] = 'NoReply'
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

database_file = './database.csv'

# Utility function to check and send reminders
def check_reminder():
    data = pd.read_csv(database_file)
    for date_str in data['end_date']:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        days_difference = period_calculator(date)
        if days_difference <= 7 and days_difference != 0:
            check = data.loc[data['end_date'] == date_str]
            selected_7 = check.loc[check['reminder_interval'] == 7]
            my_dict_list_7 = selected_7.to_dict('records')
            for main_dict in my_dict_list_7:
                e_mail(main_dict, days_difference)
        if days_difference == 1:
            check = data.loc[data['end_date'] == date_str]
            selected_1 = check.loc[check['reminder_interval'] == 1]
            my_dict_list_1 = selected_1.to_dict('records')
            for main_dict in my_dict_list_1:
                e_mail(main_dict, days_difference)
        if days_difference == 0:
            check = data.loc[data['end_date'] == date_str]
            my_dict_list_due = check.to_dict('records')
            for main_dict in my_dict_list_due:
                due_mail(main_dict)

# Remove outdated reminders from datatbase file
def delete_from_csv(data_file):
    today_date = datetime.datetime.today().date()
    dataframe = pd.read_csv(data_file, index_col=False)
    new_set = set()
    for date_str in dataframe['end_date']:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        if today_date > date:
            new_dataframe_indices = dataframe.index[dataframe['end_date'] == date_str].tolist()
            for index in new_dataframe_indices:
                new_set.add(index)
                index_list = list(new_set)
    try:
        new_database = dataframe.drop(index_list)
        new_database.to_csv(data_file, index=False)
        print(new_database)
    except UnboundLocalError:
        print ('NO outdated reminder here!!!')

if __name__ == '__main__':
    delete_from_csv(database_file)
    check_reminder()

