This is a guide to connect TickTock to Alexa.

1: Find the EC2 IMAGE CMU_MAGNUS_V1 under our joint account.
2: Lunch an ubuntu small machine using that image, choose the exisiting securty group: Zhou (this allows machine to send message to it)
3: Follow Shrivani's guide to create a Lambda function in your EC2 console, upload the message_pass.py to it (find it in this repo). If you are not sure, look the example function I set up in our joint account: TestMagnus. Note: The only thing you need to modify is change this "amzn1.ask.skill.741b42df-ec92-4714-98d7-4446b9f871ee" to your own Application Id in your Alexa Skill that you will set up in the next step.
4: Create an Alexa Skill under Amazon Develope Console. Look the Zhou CMU Magnus V1, as an example. The only thing is you need to put your lambda function id (example id is arn:aws:lambda:us-east-1:716406664903:function:TestMagnus) in there, go back to get that in your lambda function console to retrieve it. [You only need to proceed to finsh the step test]
5: Now everything is set up. Type in python debug_online_alexa.py in the EC2 machine to start the chatbot, under the folder: zhou\Backend
6: To start your CMU Magnus, say to your Echo. "Alexa wake up CMU Magnus"
