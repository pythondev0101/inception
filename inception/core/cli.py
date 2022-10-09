from hashlib import new
import os
from flask import current_app
from inception import MONGO
from inception.auth.models import User



@current_app.cli.command('create_superuser')
def create_superuser():
    new_user = User()
    new_user.fname = 'Superuser'
    new_user.lname = 'Administrator'
    new_user.username = input("Enter username: ")
    new_user.set_password(input("Enter password: "))
    MONGO.db.auth_users.insert_one({
        'fname': new_user.fname,
        'lname': new_user.lname,
        'username': new_user.username,
        'password_hash': new_user.password_hash,
        'type': 'member'
    })
    print("Superuser Created!")
    
    
@current_app.cli.command('upload')
def upload():
    import csv

    basedir = os.path.abspath(os.path.dirname(__file__))

    with open(basedir + "/upec.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                tfoe_no = row[1]
                club_designation = row[2]
                lname = row[3]
                fname = row[4]
                mname = row[5]
                phone = row[6]
                spouse_name = row[7]
                email_address = row[8]
                batch = row[9]
                occupation = row[10]
                address = row[11]
                city = row[12]
                
                MONGO.db.auth_users.insert_one({
                    'tfoe_no': tfoe_no,
                    'club_designation': club_designation,
                    'lname': lname,
                    'fname': fname,
                    'mname': mname,
                    'phone': phone,
                    'spouse_name': spouse_name,
                    'email_address': email_address,
                    'batch': batch,
                    'occupation': occupation,
                    'address': address,
                    'city': city
                })
                
                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')