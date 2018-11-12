#!/usr/bin/python

# IMPORTS
import os, sys, time, json
from asyncio import Task, ensure_future, get_event_loop, sleep, wait
from signal import SIGINT
from webwhatsapi.async_driver import WhatsAPIDriverAsync
from webwhatsapi.objects.message import Message
from messages import status_to_message
from utils import get_db, update_status, store_message, get_student_by_phone, get_signups

prod = True

if prod:

    # Sleep
    time.sleep(10)

    print("Environment", os.environ)
    try:
        os.environ["SELENIUM"]
    except KeyError:
        print("Please set the environment variable SELENIUM to Selenium URL")

    # MongoDB
    db = get_db()

    # asyncio loop
    loop = get_event_loop()
    # Get Profile
    profiledir = os.path.join(".", "firefox_cache")
    # driver = WhatsAPIDriverAsync(loadstyles=True, loop=loop)
    driver = WhatsAPIDriverAsync(
        profile=profiledir, 
        client='remote', 
        command_executor=os.environ["SELENIUM"],
        loadstyles=False,
        loop=loop)

    async def run():
        
        async def text(student, incoming_text=''):
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
                    chat = await driver.get_chat_from_id(phone)
                    chat.send_message(response_text)
                    # Store message
                    print('Storing message...')
                    store_message(db, 'coderbot', username, response_text)
                # Update Status
                print('Updaing status...')
                update_status(db, username, status_updated)
            else:
                print('Invalid Response')

        # Starting
        await sleep(10, loop=loop)
        print('Connecting...')
        await driver.connect()
        print('Wait for login...')
        await driver.wait_for_login()
            
        # Do something!
        while not Task.current_task().cancelled():

            # Validation for signups
            print('Validate signups!')
            for student in get_signups(db):
                await text(student)

            # Check unread messages
            print('Check unread!')
            for contact in await driver.get_unread():
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
                                await text(student, message_text)
                    else:
                        print('Number not known')

            # Wait for a bit
            print('wait!')
            await sleep(0.5, loop=loop)


    async def start():
        
        async def heartbeat():
            print('Starting heartbeat...')
            while not Task.current_task().cancelled():
                print('beat!')
                await sleep(5, loop=loop)

        fut_heartbeat = ensure_future(heartbeat(), loop=loop)
        fut_runner = ensure_future(run(), loop=loop)

        def stop(*args, **kwargs):
            fut_heartbeat.cancel()
            fut_runner.cancel()

        loop.add_signal_handler(SIGINT, stop)

        await wait([fut_heartbeat, fut_runner], loop=loop)

    # START
    loop.run_until_complete(start())

else:
    print('Debug mode enabled')
    db = get_db()
    input_student = input("Student ID: ")
    student = get_student_by_phone(db, input_student)
    if student is None:
        print("Student not found, goodbye!!!")
        exit(1)
    input_text = input("Text: ")

    print('Student: {}'.format(student))
    print('Gathering data...')
    username = student['username']
    status = student['status']
    phone = student['phone']
    # Get Response
    print('Getting response...')
    response = status_to_message[status](db, student, input_text)
    print(response)