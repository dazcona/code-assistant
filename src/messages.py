#!/usr/bin/python

# IMPORTS
import string
from utils import get_prediction, get_recommendation, get_work
from gist_scrapper import gist


GREETING = '''Hi %s %s! I am CoderBot 🤖 Thanks for taking a step towards becoming a better coder. ''' + \
'''Please reply this message with the code provided to you for validation e.g. *123456*'''

VALIDATED = '''Thanks for verifying your number 🙃 We are ready to start our journey! 🚀'''

NOT_VALID = '''I am afraid that is not the code I was expecting 🙁 Type it again!'''

REPEAT_VALIDATION = '''I am afraid the code is incorrect 🙁 Go back to your email, click on the link, ''' + \
'''add your phone number, generate a new code and type it here. Thank you for your patience!'''

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

MATERIAL_LAB = '''In order to engage more with the material and make more progress on the laboratory work, ''' + \
'''please have a closer look at the labsheet: %s'''
MATERIAL_RES = '''Check out the following related material: %s 👩‍💻 👨‍💻'''
NO_MATERIAL = '''Well done to you for not having a failed submission on the system! Way to go! Check *program* for a random code snippet.'''

PROGRAM = '''Check out this code snippet regarding ```%s``` 🚀'''

REMINDER = '''This information was generated on %s and your progression might have changed since.'''
# _DATE = '''Monday the 12th November 2018'''
# _DATE = '''Monday the 20th November 2018'''
#_DATE = '''Monday the 26th November 2018'''
#_DATE = '''Monday the 3rd December 2018'''
_DATE = '''Monday the 10th December 2018'''

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

OPT_OUT = '''I am sad to see you go 🙁 I hope you were motivated to continue this journey and learned some programming skills on the way 🤖 👋 ''' + \
'''Are you sure you want to opt-out? You will not be able to talk to me again this semester. Type *yes* to confirm'''

CONFIRM_OPT_OUT = '''Thank you for your confirmation! You just opted-out. Do you want to remove all your data from our system? ''' + \
'''Remember your phone number will removed at the end of the semester anyway. Your data is only used for research purposes anonymously. ''' + \
'''Type *yes* to confirm or another word not to'''
NOT_CONFIRM_OPT_OUT = '''I am so happy you are staying 👊 Type *menu* to see the options! 😎'''

DATA_REMOVED = '''Thank you for your confirmation! Your data will be removed. '''
DATA_NOT_REMOVED = '''Thank you for your confirmation! Your data will only be used for research purposed anonymously. '''
BYE = '''Any question please reach out to us at predictcs@computing.dcu.ie. Bye now 🤖 👋 '''

NOT_ACTIVE = '''Your account is no longer active. '''

LABSHEET_URI = 'https://ca116.computing.dcu.ie%s.html'


def get_text(text):

    return text.strip().lower()


def get_greeting(db, student, _):

    # Message
    message = GREETING % (student['name'], student['surname'])
    
    return [ message ], 3


def validate_code(db, student, text):

    if student['code'] == text: # correct code
        return [ VALIDATED, OPTIONS ], 5
    else:
        return [ NOT_VALID ], 4


def repeat_validation(db, student, text):

    if student['code'] == text: # correct code
        return [ VALIDATED, OPTIONS ], 5
    else:
        return [ REPEAT_VALIDATION ], 1


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

def get_options(db, student, text):

    # Question
    text = get_text(text)
    if text == 'menu':
        return [ OPTIONS ], 5
    elif text == 'more':
        return [ MORE_OPTIONS ], 5
    elif text == 'progress':
        # Performance prediction
        prediction = get_prediction(db, student['username'])
        # Work
        work = get_work(db, student['username'])
        # Message
        grade = get_grade_message(prediction['prediction'], work['cum_programs_W11'])
        response = [ grade, REMINDER % _DATE, LAB ]
        # Coverage
        if work['coverage_W11']:
            response.append( COVERAGE_YES )
        return response, 5
    elif text == 'material':
        # Recommendation
        recommendation = get_recommendation(db, student['username'])
        # Message
        if 'labsheet' in recommendation:
            lab = LABSHEET_URI % (recommendation['labsheet']) 
            labsheet = MATERIAL_LAB % lab
            resources = MATERIAL_RES % ', '.join(LABSHEET_URI % (resource) for resource in recommendation['resources'])
            return [ labsheet, resources ], 5
        else:
            return [ NO_MATERIAL ], 5
    elif text == 'program':
        # Random gist
        snippet, desc =  gist()
        program = PROGRAM % (desc)
        return [ program, snippet ], 5
    elif text == 'terms':
        return [ TERMS ], 5
    elif text == 'help':
        return [ HELP ], 5
    elif text == 'opt-out':
        return [ OPT_OUT ], 6
    else:
        return [ NOT_FOUND ], 5


def opt_out(db, _student, _text):

    text = get_text(_text)
    if text == 'yes':
        return [ CONFIRM_OPT_OUT ], 7
    else:
        return [ NOT_CONFIRM_OPT_OUT ], 5


def delete_personal_data(db, _student, _text):

    text = get_text(_text)
    if text == 'yes':
        return [ DATA_REMOVED, BYE ], 9
    else:
        return [ DATA_NOT_REMOVED, BYE ], 8


def no_chat(db, _student, _text):

    return [ NOT_ACTIVE, BYE ], 10


# DICTIONARY OF OPTIONS
status_to_message = {
    2: get_greeting,
    3: validate_code,
    4: repeat_validation,
    5: get_options,
    6: opt_out,
    7: delete_personal_data,
    8: no_chat,
    9: no_chat,
    10: no_chat,
}