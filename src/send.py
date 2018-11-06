#!/usr/bin/python

# IMPORTS
import os
import json
from utils import get_db
from flask import Flask, render_template
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer


# MongoDB
db = get_db()

# FLASK
app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

app.config.update(
	#EMAIL SETTINGS
	MAIL_SERVER=os.environ["MAIL_SERVER"],
	MAIL_PORT=os.environ["MAIL_PORT"],
	MAIL_USE_TLS=os.environ["MAIL_USE_TLS"],
	MAIL_USERNAME=os.environ["MAIL_USERNAME"],
	MAIL_PASSWORD=os.environ["MAIL_PASSWORD"]
)

mail = Mail(app)
ts = URLSafeTimedSerializer(os.environ["SECRET_KEY"])

# SEND EMAIL
sender = os.environ["INV_SENDER"] 
bcc = [ os.environ["INV_BCC"] ]
# cc = [ os.environ["INV_CC"] ]
course = os.environ["INV_COURSE"]
subject = "DCU %s Whatsapp Artificial Intelligence ChatBot - Invitation" % (course.upper())
subject_encoded_emojis = '=?utf-8?Q?=F0=9F=A4=96_=F0=9F=91=BE_%s?=' % (subject)

# STUDENTS
students = db.students.find(
	{ 'status': { '$in': [ 0, 1 ] } },
	{ 'email': 1, 'token': 1 },
)

# Emails in bulk
with app.app_context():
	with mail.connect() as conn:
		for student in students:
			email = student['email']
			token = student['token']
			content = render_template(
				'mail.html',
				token=token)
			recipients = [ email ]
			msg = Message(
				subject=subject_encoded_emojis,
				sender=sender,
				#cc=cc,
				bcc=bcc,
				recipients=recipients,
				html=content)
			print ("Sending mail to %s" % (email))
			conn.send(msg)
			print ("Mail sent")
			result = db.students.update_one(
				{ 'email': email },
				{
					'$set': { 'status': 1 } # Status: "Email Sent"
				}
			)
			print("Updated, Matched count %d, Modified count %d" % (result.matched_count, result.modified_count))

# Email
#with app.app_context():
#	content = render_template(
# 		'mail.html', 
# 		subject=subject, 
# 		token="guest")
#	msg = Message(
#		subject=subject,
#		sender=sender,
#		recipients=[ my_mail ],
#		html=content)
#	print('Sending email')
#	mail.send(msg)
#	print('Mail sent')
