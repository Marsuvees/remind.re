from flask import Flask, request, render_template, redirect
from database import ReminderDetails, session as sess
from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv 

app = Flask(__name__)

database_file = './remind.re/database.csv'


# Define routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/<string:page_name>")
def page(page_name):
    return render_template(page_name)

def write_to_csv(data):
    field_names = ["tenant_name","tenant_phone_number","rent_amount","rent_period_in_months","date_of_initial_payment","rent_expiry_date"]
    with open('database.csv', '+a') as database:  # You will need 'wb' mode in Python 2.x
        writer = csv.DictWriter(database, fieldnames=field_names)
        writer.writerow(data)

# Define the route to process the form
@app.route('/process_form', methods=['POST', 'GET'])
def create_reminder():
    if request.method == 'POST':
        # Get the form data
        tenant_name = request.form['tenant_name']
        tenant_phone_number = request.form['tenant_phone_number']
        rent_amount = request.form['rent_amount']
        date_of_initial_payment = datetime.strptime(request.form['date_of_initial_payment'], '%Y-%m-%d').date()
        rent_period_in_months = request.form['rent_period_in_months']
        new_reminder = ReminderDetails(tenant_name=tenant_name, tenant_phone_number=tenant_phone_number, rent_amount=rent_amount, date_of_initial_payment=date_of_initial_payment, rent_period_in_months=rent_period_in_months)
        
        # Calculate rent expiry date
        rent_expiry_date = date_of_initial_payment + relativedelta(months=int(rent_period_in_months))  
        new_reminder.rent_expiry_date = rent_expiry_date

        sess.add(new_reminder)
        sess.commit()

        # Write to csv
        info = dict()
        info['tenant_name'] =  request.form['tenant_name']
        info['tenant_phone_number'] = request.form['tenant_phone_number']
        info['rent_amount'] = request.form['rent_amount']
        info['date_of_initial_payment'] = date_of_initial_payment
        info['rent_period_in_months'] = request.form['rent_period_in_months']
        info['rent_expiry_date'] = rent_expiry_date
        print(info)
        write_to_csv(info)

        return redirect("/thankyou.html")
    else:
        return 'Oops something went wrong!!!'


if __name__ == '__main__':
    app.run(debug = True)
