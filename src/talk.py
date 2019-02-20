#!/usr/bin/python3

import os, time
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message
from demo import get_response

def run():

    try:
        os.environ["SELENIUM"]
        print('Connecting...')
        profiledir = os.path.join("/coderbot","config", "firefox_cache")
        driver = WhatsAPIDriver(
            profile=profiledir, 
            client='remote', 
            command_executor=os.environ["SELENIUM"],
            loadstyles=False)
        driver.connect()
        print('Wait for login...')
        driver.wait_for_login()
        driver.subscribe_new_messages(NewMessageObserver(driver))
        print("Waiting for new messages...")

        while True:
            time.sleep(60)

    except Exception as e:
        print('Error connecting to Whatsapp, stopping...')
        print(e)
        raise

class NewMessageObserver:
    def __init__(self, driver):
        self.driver = driver
    def on_message_received(self, new_messages):
        try:
            print('Processing {} messages...'.format(len(new_messages)))
            send_msg_sleep = 0.5
            for message in reversed(new_messages):
                id = message.sender.id
                if len(message.chat_id['user'])>19:
                    break
                response = get_response(message.safe_content[:-3].lower())
                self.driver.send_message_to_id(id, response)
                time.sleep(send_msg_sleep)
        except Exception as e:
            print('Error in the main loop, starting agin...')
            print(e)

if __name__ == '__main__':
    run()