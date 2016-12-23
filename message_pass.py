from __future__ import print_function
import socket
# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------
def say_hello():
    session_attributes = {}
    card_title = "Hi, I'm CMU Magnus"
    speech_output = "Hi, I'm CMU Magnus, let's chat"
    reprompt_text = "What do you want to talk about?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def stop():
    card_title = "Have a nice day!"
    speech_output = "Have a nice day!"
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def help():
    card_title = "What do you want to talk about?"
    speech_output = "Let's have a conversation. What do you want to talk about?"
    reprompt_text = "What do you want to talk about?"
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_chat(intent_request):
    session_attributes = {}
## zhou edits
    # Debug line
    rawtext = intent_request['intent']['slots']['RawText']['value']
    #speech_output = "You are now in chatmode, and you said " + rawtext
    #rawtext = 'hello world'
    hostip = '54.211.21.1'
    port = 35
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.connect((hostip,port))
    serversocket.send('user0|'+rawtext)
    response_raw = serversocket.recv(1024)
    response, strategy = response_raw.split('|')
    reprompt_text = response
    card_title = 'chat mode'
    speech_output = response
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
## --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return say_hello()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("*** Intent Name: " + intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "HelloIntent":
        return say_hello()
    elif intent_name == "StopIntent":
        return stop()
    elif intent_name == "HelpIntent":
        return help()
    elif intent_name == "ChatIntent":
        return handle_chat(intent_request)
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


	

# --------------- Main handler ------------------

def lambda_handler(event, context):
	
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.741b42df-ec92-4714-98d7-4446b9f871ee"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
