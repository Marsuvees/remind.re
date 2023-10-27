import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
from database import ReminderDetails, session as sess
from datetime import datetime
from dateutil.relativedelta import relativedelta

# def e_mail(mail_dict, days_left):
#     html = Template(Path('./due_email.html').read_text())
#     email = EmailMessage()
#     email['from'] = 'NoReply'
#     email['to'] = email_address
#     email['subject'] = 'Reminder Test!!!'

#     email.set_content(html.substitute(name = tenant_name,
#                                       tenant_phonenumber = tenant_phone_number,
#                                       init_payment_date = initial_date_of_payment,
#                                       rent_expirty_date = rent_expiry_date,
#                                       rent_amount =  rent_amount),
#                         'html')

#     with smtplib.SMTP(host='smtp.gmail.com', port = 587) as smtp:
#         smtp.ehlo()
#         smtp.starttls()
#         smtp.login('kiingjay77@gmail.com', 'ioiwirwvfyiefwgf')
#         smtp.send_message(email)
#         print ('All done!!!')

def due_mail(tenant_name, tenant_phone_number, initial_date_of_payment, rent_expiry_date, rent_amount):
    html = Template(Path('./due_email.html').read_text())
    email = EmailMessage()
    email['from'] = 'NoReply'
    email['to'] = "tolujed@gmail.com"
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

# Utility function to check and send reminders
def check_reminder():
    reminders = sess.query(ReminderDetails).all()
    for reminder in reminders:
        if (reminder.rent_expiry_date - datetime.today().date()).days <= 30:
            due_mail(reminder.tenant_name, reminder.tenant_phone_number, reminder.date_of_initial_payment, reminder.rent_expiry_date, reminder.rent_amount)
            

# Remove outdated reminders from datatbase file
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

