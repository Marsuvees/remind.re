from flask import Flask, request, render_template, redirect
from database import ReminderDetails, session as sess
from datetime import datetime
from dateutil.relativedelta import relativedelta
app = Flask(__name__)

database_file = './remind.re/database.csv'


# Define routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/<string:page_name>")
def page(page_name):
    return render_template(page_name)

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
        return redirect("/thankyou.html")
    else:
        return 'Oops something went wrong!!!'


if __name__ == '__main__':
    app.run(debug = True)
