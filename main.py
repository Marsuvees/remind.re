import csv
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

database_file = './remind.re/database.csv'


# Define routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/<string:page_name>")
def page(page_name):
    return render_template(page_name)

# Utility function to write data to CSV
def write_to_csv(data):
    global database_file
    headerlist = list(data.keys())
    with open(database_file, 'a', newline='') as database:
        writer = csv.DictWriter(database, fieldnames=headerlist)
        if database.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

# Define the route to process the form
@app.route('/process_form', methods=['POST', 'GET'])
def create_reminder():
    if request.method == 'POST':
        info = request.form.to_dict()
        print(info)
        write_to_csv(info)
        return redirect("/thankyou.html")
    else:
        return 'Oops something went wrong!!!'

if __name__ == '__main__':
    app.run()
