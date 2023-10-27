import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
from database import ReminderDetails, session as sess
from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv

def e_mail_with_dict(mail_dict):
    tenant_name = mail_dict['tenant_name']
    tenant_phone_number = mail_dict['tenant_phone_number']
    rent_amount = mail_dict['rent_amount']
    initial_date_of_payment = mail_dict['date_of_initial_payment']
    rent_expiry_date = mail_dict['rent_expiry_date']

    html = Template(Path('./due_email.html').read_text())
    email = EmailMessage()
    email['from'] = 'NoReply'
    email['to'] = 'tolujed@gmail.com'
    email['subject'] = 'Reminder Test!!!'

    email.set_content(html.substitute(name = tenant_name,
                                      tenant_phonenumber = tenant_phone_number,
                                      init_payment_date = initial_date_of_payment,
                                      rent_expirty_date = rent_expiry_date,
                                      rent_amount =  rent_amount),
                        'html')

    with smtplib.SMTP(host='smtp.gmail.com', port = 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('kiingjay77@gmail.com', 'ioiwirwvfyiefwgf')
        smtp.send_message(email)
        print ('All done!!!')

def e_mail_database(tenant_name, tenant_phone_number, initial_date_of_payment, rent_expiry_date, rent_amount):
    html = Template(Path('./email.html').read_text())
    email = EmailMessage()
    email['from'] = 'NoReply'
    email['to'] = "tolujed@gmail.com"
    email['subject'] = 'Reminder Test!!!'

    email.set_content(html.substitute(tenant_name = tenant_name,
                                      tenant_phonenumber = tenant_phone_number,
                                      init_payment_date = initial_date_of_payment,
                                      rent_expiry_date = rent_expiry_date,
                                      rent_amount =  rent_amount),
                        'html')

    with smtplib.SMTP(host='smtp.gmail.com', port = 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('kiingjay77@gmail.com', 'ioiwirwvfyiefwgf')
        smtp.send_message(email)
        print ('All done!!!')

# Utility function to check and send reminders
def check_reminder():
    try:
        reminders = sess.query(ReminderDetails).all()
        for reminder in reminders:
            if (reminder.rent_expiry_date - datetime.today().date()).days <= 30:
                e_mail_with_dict(reminder.tenant_name, reminder.tenant_phone_number, reminder.date_of_initial_payment, reminder.rent_expiry_date, reminder.rent_amount)
    except:
        # Open the CSV file for reading
        with open('database.csv', mode='r') as file:
            # Create a CSV reader using DictReader
            csv_reader = csv.DictReader('database.csv')

            # Loop through each row in the CSV file
            for row in csv_reader:
                if (datetime.strptime(row['rent_expiry_date'], "%Y-%m-%d").date() - datetime.today().date()).days <= 30:
                    e_mail_with_dict(row)

                # Each row is already a dictionary

    

# # Remove outdated reminders from datatbase file
# def delete_data():
#     today_date = datetime.datetime.today().date()
#     dataframe = pd.read_csv(data_file, index_col=False)
#     new_set = set()
#     for date_str in dataframe['end_date']:
#         date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
#         if today_date > date:
#             new_dataframe_indices = dataframe.index[dataframe['end_date'] == date_str].tolist()
#             for index in new_dataframe_indices:
#                 new_set.add(index)
#                 index_list = list(new_set)
#     try:
#         new_database = dataframe.drop(index_list)
#         new_database.to_csv(data_file, index=False)
#         print(new_database)
#     except UnboundLocalError:
#         print ('NO outdated reminder here!!!')

if __name__ == '__main__':

    check_reminder()

