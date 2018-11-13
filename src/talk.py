#!/usr/bin/python

# IMPORTS
import os, sys, time, json
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message
from messages import status_to_message
from utils import get_db, update_status, store_message, get_student_by_phone, get_signups


# Sleep
print("Sleeping 10 seconds...")
time.sleep(10)

print("Environment", os.environ)
try:
    os.environ["SELENIUM"]
except KeyError:
    print("Please set the environment variable SELENIUM to Selenium URL")

# MongoDB
db = get_db()

# Get Profile
profiledir = os.path.join(".", "firefox_cache")
# driver = WhatsAPIDriverAsync(loadstyles=True, loop=loop)
driver = WhatsAPIDriver(
    profile=profiledir, 
    client='remote', 
    command_executor=os.environ["SELENIUM"],
    loadstyles=False)

driver.connect()
print('Wait for login...')
driver.wait_for_login()


def text(student, incoming_text=''):
    """ Text a student """

    # Data
    print('Student: {}'.format(student))
    print('Gathering data...')
    username = student['username']
    status = student['status']
    phone = student['phone']
    # Get Response
    print('Getting response...')
    response = status_to_message[status](db, student, incoming_text)
    if response:
        # Valid Response
        response_texts, status_updated = response
        # Reply
        print('Replying...')
        for response_text in response_texts:
            # Reply message
            if incoming_text == '':
                phone_number = phone.split('@')[0]
                chat = driver.get_chat_from_phone_number(phone, createIfNotFound=True)
            else:
                chat = driver.get_chat_from_id(phone)
            chat.send_message(response_text)
            # Store message
            print('Storing message...')
            store_message(db, 'coderbot', username, response_text)
        # Update Status
        print('Updaing status...')
        update_status(db, username, status_updated)
    else:
        print('Invalid Response')

# Check unread messages
while True:
    time.sleep(1)
    print('Validate signups!')
    for student in get_signups(db):
        time.sleep(1)
        text(student)

    print('Check unread!')
    for contact in driver.get_unread():
        time.sleep(1)
        print('Get phone')
        phone = contact.chat.id
        if '@g.' not in phone: # only individual chats
            print('Get student')
            student = get_student_by_phone(db, phone)
            if student: # student known
                username = student['username']
                print('Check messages:')
                for message in reversed(contact.messages):
                    print('Message: {}'.format(message))
                    if isinstance(message, Message):
                        # Message from user
                        message_text = message.safe_content[:-3].strip()
                        print('Received: {}'.format(message_text))
                        # Store message from user
                        store_message(db, username, 'coderbot', message_text)
                        # Text
                        text(student, message_text)
            else:
                print('Number %s NOT known' % (phone))


