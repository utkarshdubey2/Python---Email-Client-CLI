import sys, csv, getpass, signal
from random import randint
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import system, name
from termcolor import colored, cprint

# GLOBAL VARIABLES
file_name = 'data_mail.csv'

# functions

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# Other stuff

print("""
    Welcome to CLI Email Client.
    Here is a list of common hosts and their information.
""")
print(colored("""
    Gmail:
    Host => "smtp.gmail.com"
    Port => 587""", "yellow"))
print(colored("""
NOTE: Please don't forget to allow less secure apps from the Google Panel,
or else this CLI Client will not work.
""", "red"))

while True:
    print("""
    1) Enter 1 to configure your email client.
    2) Enter 2 to send an email.

    3) Enter 0 to exit.
    """)
    inp = input("Please enter an option: ")
    if int(inp) == 1:
         host_name = (input("Please enter the host url: "))
         port_name = input("Please enter the port: ")
         user_name = input("Please enter your email address: ")
         user_pass = getpass.getpass("Please enter your password: ")
         user_data = [["host", "port", "email", "password"], [host_name, port_name, user_name, user_pass]]
         data_file_name = open(file_name, 'w')
         with data_file_name:
             writer = csv.writer(data_file_name)
             writer.writerows(user_data)
         clear()

    if int(inp) == 2:

        # Reading the CSV file
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file)
            count = 0
            for row in csv_reader:
                if count == 0:
                    count += 1
                else:
                    host_name = row[0]
                    port_name = row[1]
                    user_name = row[2]
                    user_pass = row[3]
                    count += 1

        # More information

        host = host_name
        port = port_name
        username = user_name
        password = user_pass
        to_mail = input("Please enter the receivers email address: ")

        # EMAIL INFORMATION
        msg = MIMEMultipart("alternative")
        subject = input("Please enter the subject of the email: ")
        from_name = input("Please enter the from name: ")
        to_name = input("Please enter the to name: ")
        msg['Subject'] = subject
        msg['From'] = from_name
        msg['To'] = to_name

        msg_info = input("Please enter the message(HTML Supported): \n")
        part = MIMEText(msg_info, 'html')


        msg.attach(part)

        # EMAIL SENDING PART
        try:
            email_conn = SMTP(host, port)
            email_conn.ehlo()
            email_conn.starttls()
            try:
                email_conn.login(username, password)
            except SMTPAuthenticationError:
                print(colored("The credentials are wrong.", "blue"))
            email_conn.sendmail(from_name, to_mail, msg.as_string())
            email_conn.quit()
        except SMTPException:
            print("Sorry an error occured.")

        clear()

    if int(inp) == 0:
        sys.exit()
