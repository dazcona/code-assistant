#!/usr/bin/python

# IMPORTS
import string


GREETING = '''Hi %s %s! I am CoderBot 🤖 Thanks for taking a step towards becoming a better coder. ''' + \
'''Please reply this message with the code provided to you for validation e.g. *123456*'''

VALIDATED = '''Thanks for verifying your number 🙃 We are ready to start our journey! 🚀'''

NOT_VALID = '''I am afraid that is not the code I was expecting 🙁 Type it again!'''

REPEAT_VALIDATION = '''I am afraid the code is incorrect 🙁 Go back to your email, click on the link, ''' + \
'''add your phone number, generate a new code and type it here. Thank you for your patience!'''

MENU = '''Type *menu* to see how I can help you! 😎'''

OPTIONS = \
'''Type *progress* for a personalized message based on your progress throughout the course 🤓,\n''' + \
'''Type *material* for recommended material tailored to your progression 📘,\n''' + \
'''Type *program* to give me a useful code snippet 👾,\n''' + \
'''Type *more* for more options'''

MORE_OPTIONS = \
'''Type *terms* for our terms & conditions 🤓,\n''' + \
'''Type *help* for further help.\n''' + \
'''Type *bye* to exit.'''

GRADE = '''For the last week our records show that you are %s with the courseware and ''' + \
'''seem to be managing module well 😎 🤓. Well done you 👊. Please keep up the good work this week for the module.'''

LAB = '''Lab attendance is generally correlated with the student's performance. ''' + \
'''Well done to you for attending last week's lab session 👩‍🔬 👨‍🔬'''

MATERIAL = '''In order to engage more with the material and make more progress on the laboratory work, ''' + \
'''please have a closer look at %s 👩‍💻 👨‍💻'''

PROGRAM = '''Check out this code snippet about %s: %s'''

TERMS = '''Our predictions and recommended programs are based on your engagement and effort with the course ''' + \
'''(the programs you develop and the course material you access); your characteristics and prior performance.  ''' + \
'''Remember, this is just our best guess as to how you have been doing and is not an indicator of how you will do  ''' + \
'''in the module, laboratory exams or written exam. However, if you need to improve, it is easy to make a change  ''' + \
'''for next week; just spend more time programming and come to the labs, submit your programs to Einstein or access  ''' + \
'''the material on non-lab days. Please use this information to help you to increase your motivation and engagement  ''' + \
'''with CA116. Contact us at predictcs@computing.dcu.ie for further details.'''

HELP = '''DCU cares about you. If you feel as though you need additional supports to help you with this, please contact your lecturer ''' + \
'''Stephen Blott at stephen.blott@dcu.ie or DCU Student Support & Services at student.support@dcu.ie. We are here for you 👩‍🏫 👨‍🏫'''

BYE = '''It was great talking to you. See ya soon 🤖 👋'''


def get_text(text):

    return text.strip().lower()


def get_greeting(student, _):

    # Message
    message = GREETING % (student['name'], student['surname'])
    
    return [ message ], 3


def validate_code(student, text):

    if student['code'] == text: # correct code
        return [ VALIDATED, MENU ], 5
    else:
        return [ NOT_VALID ], 4


def repeat_validation(student, text):

    if student['code'] == text: # correct code
        return [ VALIDATED, MENU ], 5
    else:
        return [ REPEAT_VALIDATION ], 1


def get_menu(student, text):

    text = get_text(text)
    if text == 'menu':
        return [ OPTIONS ], 6
    # return None

def get_options(student, text):

    text = get_text(text)
    print(text)
    if text == 'progress':
        # add logic for predictions
        grade = GRADE % ('engaging well')
        return [ grade, LAB ], 6
    elif text == 'material':
        # add logic for recommendations
        material = MATERIAL % ('labsheet-01')
        return [ material ], 6
    elif text == 'program':
        # add logic for random snippets
        topic = 'Selection Sort'
        uri = 'https://gist.github.com/dazcona/07c6f32675d69ed2e81b94037b789347'
        program = PROGRAM % (topic, uri)
        return [ program ], 6
    elif text == 'more':
        return [ MORE_OPTIONS ], 6
    elif text == 'terms':
        return [ TERMS ], 6
    elif text == 'help':
        return [ HELP ], 6
    elif text == 'bye':
        return [ BYE ], 6


def bye(_student, _text):

    return [ BYE ], 6


# opt-out!


# DICTIONARY OF OPTIONS
status_to_message = {
    2: get_greeting,
    3: validate_code,
    4: repeat_validation,
    5: get_menu,
    6: get_options,
    7: get_options,
}