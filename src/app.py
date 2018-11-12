#!/usr/bin/python

import os
from utils import get_db
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import PhoneForm
from itsdangerous import URLSafeTimedSerializer
import random

# APP
app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
Bootstrap(app)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

# Static path
static_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"))

# MongoDB
db = get_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/privacy')
def privacy():
	return render_template('privacy.html')


@app.route('/join/<token>', methods=['GET', 'POST'])
@app.route('/join/<token>/', methods=['GET', 'POST'])
def join(token):
	form = PhoneForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		student = db.students.find_one(
			{ 'token': token, 'status': { '$in': [ 1, 2 ] } },
			{ '_id': 1 },
		)
		if student:
			# Retrieve phone
			phone = request.form['phone'].strip()
			if phone.startswith('0'):
				phone = '+353' + phone[1:]
			if phone.startswith('+'):
				phone = phone[1:] + '@c.us'
			# Create code
			code = ''.join([ str(random.randint(0, 9)) for _ in range(6) ])
			result = db.students.update_one(
				{ 'token': token },
				{
					'$set': { 
						'phone': phone,
						'code': code,
						'status': 2, # Status: "Code Shown"
					}
				}
			)
			if result.matched_count == 1:
				# Show Code
				return redirect(url_for('success', code=code))
		# Student not found or update could not be made
		return redirect(url_for('fail'))
	return render_template('join.html', token=token, form=form)


@app.route('/success')
def success():
	code = request.args['code']
	flash(dict(
		alert_type = 'alert-info',
		text = 'CoderBot will talk to you now on WhatsApp, insert the following code to verify it is you: ',
		text_bold = code,
		)
	)
	return render_template('base.html')


@app.route('/fail')
def fail():
	flash(dict(
		alert_type = 'alert-danger',
		text = 'There was an issue with your request, please email our admin at ',
		text_bold = 'predictcs@computing.dcu.ie',
		)
	)
	return render_template('base.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')