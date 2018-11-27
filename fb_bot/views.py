from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pprint import pprint
import requests
from .models import TargetUser

access_token = ''

def post_facebook_message(fbid, recevied_message):           
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(access_token) 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

def send_reminder(recevied_message):
    for user in TargetUser.objects.all():
        fbid = user.fbid
        post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(access_token) 
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        pprint(status.json())

# Create your views here.
class NTUBotView(generic.View):
    ask_user = []
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '1234567890':
            print("in get")
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("in post")
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    print("This is a message")
                    pprint(message)
                    if message['sender']['id'] in self.ask_user:
                        print("Saving user info")
                        tmp = TargetUser(fbid = message['sender']['id'],\
                                         name = message['message']['text'])
                        tmp.save()
                        self.ask_user.remove(message['sender']['id'])
                        post_facebook_message(message['sender']['id'], "Got it, save your name")
                        post_facebook_message(message['sender']['id'], "hi, %s" %(message['message']['text']))
                    elif not TargetUser.objects.filter(fbid = message['sender']['id']):
                        post_facebook_message(message['sender']['id'], "What is your name?")
                        self.ask_user.append(message['sender']['id'])
                        print("No this User:", self.ask_user)
                    else:
                        name = TargetUser.objects.get(fbid = message['sender']['id']).name
                        try:
                            post_facebook_message(message['sender']['id'], "hi %s, %s" %(name, message['message']['text']))
                        except:    
                            post_facebook_message(message['sender']['id'], "hi %s, %s" %(name, 'I cannot reply this.'))
        return HttpResponse()

