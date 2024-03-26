import datetime as dt
import pandas as pd
import random
import smtplib
# we want to hide private date variables, by having them as ENVVIRONMENT VARIABLES
# We'll set them later, but in order to access these ENVIRONMENT VARIABLES so we have to import OS:
import os

# 1. set variables & methods
now = dt.datetime.now()
today = now.day
current_month = now.month

# We need email & access password variables:
# Once have the variables as ENVIRONMENT VARIABLES, let's access the in the code:
## DEV_EMAIL & DEV_EMAIL_ACCESS_PASSWORD are our email & password variables saved as environment variables in Windows
## - so they are not hard written in the code. That way when you share the code they remain secret.
## - you have to update these with your own email & password either directly in code, or by saving them as ENVIRONMENT VARIALES
## - to see how to set ENVIRONMENT VARIABLES in Windows, watch the Youtube video below:
## https://www.youtube.com/watch?v=IolxqkL7cD8
my_email = os.environ.get("DEV_EMAIL")
password = os.environ.get("DEV_EMAIL_ACCESS_PASSWORD")


# 2. Check if today matches a birthday in the birthdays.csv & add recipients in a dictionary
today_recipients = {}
df = pd.read_csv("birthdays.csv", index_col=0)
data = df.to_dict(orient="index")
for key in data:
	if current_month == data[key]["month"] and today == data[key]["day"]:
		recipient_name = key
		recipient_email = data[key]["email"]
		today_recipients[recipient_name] = recipient_email

# 3. If step 2 is true, pick a random letter from letter templates and
# replace the [NAME] with the person's actual name from birthdays.csv
letter_1 = "letter_templates/letter_1.txt"
letter_2 = "letter_templates/letter_2.txt"
letter_3 = "letter_templates/letter_3.txt"
letters_list = [letter_1, letter_2, letter_3]

for key in today_recipients:
	with open(random.choice(letters_list)) as text_file:
		email_content = text_file.read().replace("[NAME]", key)

	# 4. Send the letter generated in step 3 to that person's email address.
	### create a connection with your email provider's sever (search online for the right smtp address for your provider)
	with smtplib.SMTP("smtp.gmail.com") as connection:
		### TLS = Transport Layer Security, a way of securing our connection to our email server
		### that way if someone intercepts the email somewhere down the line,-
		### - if this is ON the message is encrypted and they can't read it
		connection.starttls()
		### Once the connection is secure, we log in: (The password is generated from your email account -
		### -when you have to allow a 3rd party app to access your email acc -and that setting will generate a password.
		connection.login(user=my_email, password=password)
		### Then we can send our mail:
		connection.sendmail(from_addr=my_email, to_addrs=today_recipients[key],
							msg=f"Subject: HAPPY BIRTHDAY !!!\n\n{email_content}")





