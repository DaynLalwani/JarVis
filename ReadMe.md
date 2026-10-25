# JarVis (get it?)

This app is inspired by Iron Man's Jarvis Ai assistant but for your computer
It uses any AI API that can work with a custom endpoint on OpenAI

The AI sends commands Back to the the python script which will then perform those actions

IMPORTANT : EMERGENCY STOP -> ESC , will crash the whole program , use if the AI is doing something you dont want.

# SETUP

Run the Program , and click the SETUP Wizard button.

Select your default Browser 

Enter your AI endpoint 
              Auth token (Aka. Api Key)
              Model (More Param , beter understanging , higher costs)

# NOTE
each output costs ~ 1000 tokens( 950 input and ~50 out) . make sure you can send at least 5-8 requests (50-80k) tokens , to make sure Jarvis can fulfill your command.




IF JARVIS IS NOT WORKING , Re:Run The Setup WIZARD . 

Some Notable FREE Ai Platforms For you to connect JARVIS To

Google Ai Studio ----> All Gemini Models
Groq --> Many Models , ~200 actions / day
Open Router --> Many free Models , sometimes unreliable

# CLICK ENTER TO START EXECUTION OF PROMPT

# VOICE RECOGNITION UPDATE 

Click Voice and OK to the message box . it will record your speech for the next 10 seconds .
After 10 seconds click OK to the next message box and it will automatically add the text to the input prompt


# Backround Service

The backround Service.py helps you to easily launch Jarvis anytime , just click win+enter while it's runnign

## NOTE
Backround service.py is exteremely buggy and may not work properly on certain machines , if you are having issues run main.py

# CUSTOM BINARY
A custom Binary is made out of main.py , just run it and jarvis opens

![alt text](https://github.com/DaynLalwani/JarVis/raw/refs/heads/main/Assets/SS.png)

# Video Tutorial On Setup

https://github.com/DaynLalwani/JarVis/raw/refs/heads/main/Assets/Setup%20Wizard.mp4

# Usage Tutorial

https://github.com/DaynLalwani/JarVis/raw/refs/heads/main/Assets/Usage.mp4

