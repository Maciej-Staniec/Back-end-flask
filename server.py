from flask import Flask, render_template, request, redirect
from markupsafe import escape
import csv
import os
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_data_if_file_doesnot_exists(data, path):
    with open(path, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Email', 'Subject', 'Message'])
        writer.writerow([data['email'], data['subject'], data['message']])


def write_data_if_file_exists(data, path):
    with open(path, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data['email'], data['subject'], data['message']])


def write_to_csv(data):
    data_to_write = data
    file_name = rf'database.csv'
    folder_name = rf'submitted_form_data'
    path = rf'{folder_name}/{file_name}'
    print(bool(os.path.exists(path)))
    # check whether the folder exists
    if os.path.exists(folder_name):
        if os.path.isfile(path):
            write_data_if_file_exists(data_to_write, path)
        else:
            write_data_if_file_doesnot_exists(data_to_write, path)
    else:
        # create a new folder
        os.makedirs(folder_name)
        write_data_if_file_doesnot_exists(data_to_write, path)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if (request.method == 'POST'):
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return('Did not save to database')
    else:
        return 'something went wrong, try again!'


if __name__ == '__main__':
    app.run()
