#!/usr/bin/python3
import os
import aiml
import pyttsx3

from sys import exit
from pathlib import Path

sessionId = 12345

BRAIN_FILE="brain.brn"
path = Path(BRAIN_FILE)

k = aiml.Kernel()
sessionData = k.getSessionData(sessionId)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say("Hello, chatbot Rhino is online.")
engine.runAndWait()

if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)

# Endless loop which passes the input to the bot and prints
# its response
while True:
    input_text = input(">>> ")
    if input_text == "quit":
        engine.say("See you. Have a nice day.")
        engine.runAndWait()
        exit()
    elif input_text == "erase":
        engine.runAndWait()
        os.remove('C:/Users/Anna Reithmeir/PycharmProjects/rhinoChatbot/'+BRAIN_FILE)
        engine.say("My memory is now completely erased. Please reload my Brain to continue.")
        engine.runAndWait()
    elif input_text == "reload":
        engine.runAndWait()
        if path.is_file():
            engine.say("Parsing my Brain.")
            k.loadBrain(BRAIN_FILE)
            engine.say("Reload complete.")
            engine.runAndWait()
        else:
            engine.say("Brain not found. Please save it first and try again.")
            engine.runAndWait()
    elif input_text == "update":
        engine.say("Learning new functionalities.")
        engine.runAndWait()
        k.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
        engine.say("My functions are now up to date.")
        engine.runAndWait()
    elif input_text == "save":
        engine.say("Saving my current skills.")
        engine.runAndWait()
        k.saveBrain(BRAIN_FILE)
        engine.say("Save complete.")
        engine.runAndWait()
    elif input_text == "execute":
        print("Sphere radius is", k.getPredicate('sphereRadius'))
        print("Sphere is located at (" + k.getPredicate('xPosition') + ", " + k.getPredicate('yPosition') + ", " + k.getPredicate('zPosition') + ")")
        print("Desired rotation along x-axis: ", k.getPredicate('xRotation'))
        print("Desired rotation along y-axis: ", k.getPredicate('yRotation'))
        print("Desired rotation along z-axis: ", k.getPredicate('zRotation'))
        scaling = k.getPredicate('scaling')
        if scaling == 'smaller':
            print("Sphere is to be made " + scaling + " by a factor of " + k.getPredicate('smallScale'))
        if scaling == 'bigger':
            print("Sphere is to be made " + scaling + " by a factor of " + k.getPredicate('bigScale'))
    else:
        response = k.respond(input_text)
        if ('coordinates' in response):
            print("x is (position on x-axis) y is (position on y-axis) z is (position on z-axis)")
        engine.say(response)
        engine.runAndWait()