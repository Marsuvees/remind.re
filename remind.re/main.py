import datetime
import csv
from flask import Flask, request, render_template, redirect
from notifier import e_mail, due_mail, period_calculator   # Import necessary functions
import pandas as pd
import threading
import time

app = Flask(__name__)

database_file = './database.csv'


# Define routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/<string:page_name>")
def page(page_name):
    return render_template(page_name)

# Utility function to write data to CSV
def write_to_csv(data):
    headerlist = list(data.keys())
    with open('./database.csv', 'a', newline='') as database:
        writer = csv.DictWriter(database, fieldnames=headerlist)
        if database.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

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

# Utility function to check and send reminders
def check_reminder():
    global database_file
    data = pd.read_csv(database_file)
    for date_str in data['end_date']:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        while True:
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
            time.sleep(86400)
        


def start_background_task():
    # Check if the background task thread is already running
    global background_thread
    if 'background_thread' not in globals() or not background_thread.is_alive():
        background_thread = threading.Thread(target=check_reminder)
        background_thread.start()
        return "Background task started."
    else:
        return "Background task is already running."                

# Define the route to process the form
@app.route('/process_form', methods=['POST', 'GET'])
def create_reminder():
    global database_file
    
    delete_from_csv(database_file)
    if request.method == 'POST':
        info = request.form.to_dict()
        print(info)
        write_to_csv(info)
        print(start_background_task())
        return redirect("/thankyou.html")
    else:
        return 'Oops something went wrong!!!'

if __name__ == '__main__':
    app.run(debug=True)
