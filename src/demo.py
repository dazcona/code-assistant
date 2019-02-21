#!/usr/bin/python

# IMPORTS
import string
from gist_scrapper import gist
import random


GREETING = '''Hi guest! I am CoderBot 🤖 Thanks for taking a step towards becoming a better coder 🙃. ''' + \
'''We are ready to start our journey! 🚀'''

CODE = '''This project's code has been made publicly available on Github: https://github.com/dazcona/code-assistant'''

VIDEO = '''We also made a demostration video: https://www.youtube.com/watch?v=9HSLwvVzN8E'''

MENU = '''At any time, type *menu* to see these options! 😎'''

OPTIONS = \
'''Type *progress* for a personalized message based on your progress throughout the course 🤓,\n''' + \
'''Type *material* for recommended material tailored to your progression 📘,\n''' + \
'''Type *program* to give me a random code snippet 👾,\n''' + \
'''Type *more* for more options'''

MORE_OPTIONS = \
'''Type *terms* for our terms & conditions 🤓,\n''' + \
'''Type *help* for further help.\n''' + \
'''Type *opt-out* to opt-out from this project.'''

GRADE_BEFORE = '''For the last week our records show that %s'''
GRADE_100 = '''you are engaging really well with the courseware and are well on top of the module 😎 🤓. Well done you 👊. Please keep up the good work this week for the module 👏'''
GRADE_90 = '''you are engaging well with the courseware and seem to be managing the module well 😉. Well done you 👊. Please keep up the good work this week for the module 🙌'''
GRADE_80 = '''you are engaging OK with the courseware and seem to be managing the module well 😉. Well done you 👊. Please keep up the good work this week for the module 💪'''
GRADE_70 = '''you seem to be engaging OK with the courseware and seem to be managing the module OK 👌. Please keep up the good work this week for the module 💪'''
GRADE_60 = '''you are engaging just about OK with the courseware and are probably managing the module OK 👍. Please keep up the good work this week for the module 💪'''
GRADE_50 = '''you may not be engaging enough with the courseware but might be managing the module OK 👍. Please try to make more effort to keep up this week for the module 💪'''
GRADE_40 = '''you don't seem to be engaging enough with the courseware for the module. Please try to make more effort to keep up this week for the module 👍'''
GRADE_30 = '''you are not engaging enough with the courseware for the module. Please try to make more effort to keep up this week for the module 👍'''
GRADE_20 = '''you are not engaging enough with the courseware for the module and you might need to work harder. Please try to make more effort to keep up this week and if you are finding this difficult then do contact the lecturer 👨‍🏫 👩‍🏫'''
GRADE_10 = '''you are not engaging enough with the courseware for the module and you really need to work harder. Please try to make more effort to keep up this week and if you are finding this difficult then do contact the lecturer 👨‍🏫 👩‍🏫'''

LAB = '''Lab attendance is generally correlated with the student's performance 👩‍🔬 👨‍🔬'''
COVERAGE_YES = '''Well done to you for looking at the notes last week! 😎'''

MATERIAL = '''In order to engage more with the material and make more progress on the laboratory work, ''' + \
'''check out the following related material regarding ```%s```: %s 👩‍💻 👨‍💻'''
NO_MATERIAL = '''Well done to you for not having a failed submission on the system! Way to go! Check *program* for a random code snippet.'''

RESOURCES = [
    ('Mutable and immutable types in Python', 'https://docs.python-guide.org/writing/structure/#mutable-and-immutable-types'),
    ('Decorators in Python', 'https://www.geeksforgeeks.org/decorators-in-python/'),
    ('Regular Expression in Python', 'https://docs.python.org/3/howto/regex.html'),
    ('Python Lambda', 'https://www.w3schools.com/python/python_lambda.asp'),
    ('Exceptions Handling in Python', 'https://www.tutorialspoint.com/python/python_exceptions.htm'),
]

PROGRAM = '''Check out this code snippet regarding ```%s``` 🚀'''

REMINDER = '''This information was generated yesterday and your progression might have changed since.'''

TERMS = '''Our predictions and recommended programs are based on your engagement and effort with the course ''' + \
'''(the programs you develop and the course material you access); your characteristics and prior performance. ''' + \
'''Remember, this is just our best guess as to how you have been doing and is not an indicator of how you will do ''' + \
'''in the module, laboratory exams or written exam. However, if you need to improve, it is easy to make a change ''' + \
'''for next week; just spend more time programming and come to the labs, submit your programs to Einstein or access ''' + \
'''the material on non-lab days. Please use this information to help you to increase your motivation and engagement ''' + \
'''with the module. Contact us at predictcs@computing.dcu.ie for further details.'''

HELP = '''DCU cares about you. If you feel as though you need additional supports to help you with this, please contact your lecturer ''' + \
'''Stephen Blott at stephen.blott@dcu.ie or DCU Student Support & Services at student.support@dcu.ie. We are here for you 👩‍🏫 👨‍🏫'''

NOT_FOUND = '''Sorry I could not understand that command 🙁 Type *menu* to see the options! 😎'''

OPT_OUT = '''You just opted-out. I am sad to see you go 🙁 I hope you were motivated to continue this journey and learned some programming skills on the way 🤖 👋 ''' + \
'''Your data will be removed. Any question please reach out to us at predictcs@computing.dcu.ie. Bye now 🤖 👋 '''

NOT_ACTIVE = '''Your account is no longer active. '''


def get_text(text):

    return text.strip().lower()


def get_grade_message(prediction, work):

    if prediction and work > 0.9:
        return GRADE_BEFORE % GRADE_100
    elif prediction and work > 0.8:
        return GRADE_BEFORE % GRADE_90
    elif prediction and work > 0.7:
        return GRADE_BEFORE % GRADE_80
    elif prediction and work > 0.6:
        return GRADE_BEFORE % GRADE_70
    elif prediction and work > 0.5:
        return GRADE_BEFORE % GRADE_60
    elif prediction or work > 0.4:
        return GRADE_BEFORE % GRADE_50
    elif prediction or work > 0.3:
        return GRADE_BEFORE % GRADE_40
    elif prediction or work > 0.2:
        return GRADE_BEFORE % GRADE_30
    elif prediction or work > 0.1:
        return GRADE_BEFORE % GRADE_20
    else:
        return GRADE_BEFORE % GRADE_10

def get_response(text):

    # Question
    text = get_text(text)

    if text in ['hi', 'hello', 'hey', 'howdy']:
        return [ GREETING, CODE, VIDEO, MENU ]

    elif text == 'menu':
        return [ OPTIONS ]

    elif text == 'more':
        return [ MORE_OPTIONS ]

    elif text == 'progress':
        # Performance prediction
        prediction = random.random() < 0.5 # True or False
        # Work
        work = random.random()
        # Message
        grade = get_grade_message(prediction, work)
        # Image
        image_path = '/coderbot/img/{}/{}.png'.format('positive' if prediction else 'negative', random.randint(0, 11))
        return [ grade, REMINDER, LAB, COVERAGE_YES, image_path ]

    elif text == 'material':
        # Recommendation
        recommendation = random.random() < 0.1
        # Message
        if recommendation:
            resource_desc, resource_uri = RESOURCES[random.randint(0, len(RESOURCES))]
            material = MATERIAL % (resource_desc, resource_uri)
            return [ material ]
        else:
            return [ NO_MATERIAL ]

    elif text == 'program':
        # Random gist
        snippet, desc =  gist()
        program = PROGRAM % (desc)
        return [ program, snippet ]

    elif text == 'terms':
        return [ TERMS ]

    elif text == 'help':
        return [ HELP ]

    elif text == 'opt-out':
        return [ OPT_OUT ]

    return [ NOT_FOUND ]


if __name__ == "__main__":
    
    text = input("Hi human, say *hi* to me!: ").strip().lower()
    while text != 'bye':
        # Text
        print('You: {}'.format(text))
        response = get_response(text)
        # Response
        print('CoderBot: {}'.format('\n'.join(response)))
        text = input("Your response: ").strip().lower()
