
from customtkinter import *
import sys
from tkinter import PhotoImage , filedialog , messagebox
from groq import Groq
import subprocess
import keyboard
import pyautogui
import io
import base64
import aiendpoint
import localmodel
import time
import json
import VoiceRecognition
pyautogui.FAILSAFE = True
global AutoOut 
AutoOut = False
global previousmsg
previousmsg = []
global has_vals
has_vals = False
global Vals 
Vals = {}

#First Time Setup 
try :
    with open("C:\\ProgramData\\JarVis.json","r",encoding="utf-8")as file:
        Vals = json.load(file)
        print(Vals)
except Exception as e:
    print("Error in loading file :",e)

#==========================================================================================================================
#autoclose functions
def autoout():
    global AutoOut
    AutoOut = True

def autoclose(kc):
    if AutoOut:
        sys.exit()
def estop():
    print("EMERGENCY STOP")
    os._exit(0)
    sys.exit()

def flash():
    flash_win = CTkToplevel(root)
    flash_win.overrideredirect(True)
    flash_win.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    flash_win.attributes('-topmost', True)
    
    flash_win.configure(fg_color="white") 
    flash_win.attributes('-alpha', 0.25)
    
    flash_win.update()
    
    time.sleep(0.06) 
    
    flash_win.destroy()
    root.update() 

#Main function to send the Prompt
def enter(text):
    global previousmsg
    visualiser = CTk()
    visualiser.geometry("500x80")
    Info = CTkLabel(visualiser,text="Information Panel : Whatever Ai wants to tell you will be written here",width=500,height=80)
    Info.grid()
    visualiser.attributes("-topmost",True)
    try:
        Info.configure(text=previousmsg[-1].split("#*&")[1])
    except Exception as e:
        pass
    
    ss = pyautogui.screenshot()
    bufferedimg = io.BytesIO()
    ss.save(bufferedimg, format="PNG")
    ss.save("SS.png",format="PNG")
    b64img = base64.b64encode(bufferedimg.getvalue()).decode('utf-8')
    print("Screen size:", pyautogui.size())
    screen_width, screen_height = pyautogui.size()
    mime_type = "image/png"
    pmsgstr = "Pevious commands are : "+str(previousmsg)
    full_prompt = (
        "YOU ARE AN AI AGENT NAMED JARVIS. Reply only with the given predefined "
        "commands else the program will crash. Include the curly brackets. "
        "Your Instructions are to follow this: " + text + " and refer to the attached image. "
        "To open the default Browser reply with {BROWSER}. "
        "To click at a point on the screen reply with {CLICK : (X pixel , Y Pixel)}. "
        "To type a phrase on the keyboard reply with {TYPE : (\" Phrase \")}. "
        "To type a phrase on the keyboard and click enter after that reply with {ETYPE : (\" Phrase \")}. "
        "To click a point then type and click enter reply with {CTE : (X Pixel , Y Pixel)|(\"Text\")}"
        "Click Enter Using the command {ENTER}"
        "IF you dont know what to do or are done with the task at hand reply with {DONE}. "
        "Only reply with one command at a time, another prompt will be given after the action is done."
        "The SIZE OF THE DISPLAY IS  : "+str(screen_width)+"x"+str(screen_height)+""
        "IMPORTANT COORDINATE RULES: "
        "Use coordinates in the ORIGINAL screenshot's pixel coordinate system. "
        "The origin (0,0) is the top-left corner. "
        "X increases to the right; Y increases downward. "
        "Click the CENTER of the target, not its edge. "
        "Do not resize or scale coordinates. "
        "Carefully estimate the center of the target using its visible boundaries. "
        "IF YOU WANT TO INFORM THE USER OF SOMETHING , at the end of the PROMPT add #*& followed by your message"
        "CRITICAL: Look at the screenshot. If the task described in the instructions is done or the previous message(s) have already executed your task move on to the next one "
        +pmsgstr
    )
    msg = aiendpoint.req(full_prompt,mime_type,b64img,Vals["Endpoint"],Vals["Auth"],Vals["Model"])
    print(msg)
    previousmsg.append(msg)
    visualiser.withdraw()
    if msg == "{DONE}":
        sys.exit()
    elif "CTE" in msg:
        flash()
        X = int(msg.split("|")[0].split("(")[1].split(")")[0].split(',')[0])
        Y = int(msg.split("|")[0].split("(")[1].split(")")[0].split(',')[1])
        text = msg.split("|")[1].split("\"")[1]
        pyautogui.click(X,Y)
        keyboard.write(text)
        pyautogui.press("enter")
        enter(text)
    elif msg == "{BROWSER}":
        flash()
        subprocess.Popen(Vals["Browser"])
        time.sleep(2)
        enter(text)
    elif "CLICK" in msg :
        flash()
        pyautogui.click(int(msg.split("(")[1].split(")")[0].split(",")[0]) ,int( msg.split("(")[1].split(")")[0].split(",")[1]))
        time.sleep(1)
        enter(text)
    elif "ETYPE" in msg:
        flash()
        keyboard.write(msg.split("(")[1].split(")")[0].split("\"")[1])
        pyautogui.press("enter")
        time.sleep(1)
        enter(text)
    elif "TYPE" in msg:
        flash()
        keyboard.write(msg.split("(")[1].split(")")[0].split("\"")[1])
        time.sleep(1)
        enter(text)
    elif "{ENTER}" in msg:
        flash()
        pyautogui.press('enter') 
        time.sleep(0)
        enter(text)
    else:
        sys.exit()

def textchange(text):
    if text == "":
        root.geometry(f"550x160+{int((root.winfo_screenwidth() - 500) / 2)}+{int((root.winfo_screenheight() - 80) / 2)}")
    else:
        root.geometry(f"550x80+{int((root.winfo_screenwidth() - 500) / 2)}+{int((root.winfo_screenheight() - 80) / 2)}")


def setup():
    global AutoOut
    AutoOut = False
    global Vals
    Vals = {}
    default_browser = ''
    global page
    page = 0
    #Default Browser
    def pick_browser():
        default_browser = filedialog.askopenfilename(
                    title="SELECT YOUR DEFAULT BROWSER",
                    initialdir="%USERPROFILE%",
                    filetypes=[("Windows Executables (Your Browser)","*.exe")]
                )
        Value.insert(0,default_browser)
    def nxt():
        global page
        if page == 0:
            Vals["Browser"] = Value.get()
            page = 1
            file_pick.destroy()
            lbl.configure(text="Enter Your API Endpoint")
            Value.delete(0,"end")
            Value.configure(placeholder_text="Enter your api endpoint ....")
        elif page == 1:
            Vals["Endpoint"] = Value.get()
            page = 2
            lbl.configure(text="Enter Your Api Auth Token") 
            Value.delete(0,"end")
            Value.configure(placeholder_text="Enter API KEY , usually a long string ....")
        elif page == 2:
            Vals["Auth"] = Value.get()
            lbl.configure(text="Enter Your Model :")
            Value.delete(0,"end")
            Value.configure(placeholder_text="Enter model , better model is usually more expensive")
            page = 3
        elif page == 3:
            Vals["Model"] = Value.get()
            lbl.configure(text="Enter Voice Recognition Time :")
            Value.delete(0,"end")
            Value.configure(placeholder_text="In seconds ... (default 10)")
            page = 4

        elif page == 4:
            Vals["VRT"] = Value.get()
            lbl.configure(text="Enter Voice Recognition Model Size :")
            Value.destroy()
            dropdown.grid(row=1,column=0)
            next_button.configure(text="Submit")
            page = 5
        elif page == 5:
            Vals["Voice_Model"] = dropdown.get()
            setup_wizard.withdraw()
            global AutoOut
            AutoOut = True
            with open("C:\\ProgramData\\JarVis.json","w") as file:
                json.dump(Vals,file,indent=4)
    
    setup_wizard = CTk()
    setup_wizard.title("SETUP WIZARD")
    lbl = CTkLabel(setup_wizard,text="ENTER DEFAULT BROWSER : ")
    lbl.grid(row=0,column=0)
    Value = CTkEntry(setup_wizard,placeholder_text="ENTER PATH TO DEFAULT BROWSER OR Pick A FILE ....",width=300)
    Value.grid(row=1,column=0)
    file_pick =CTkButton(setup_wizard,text="...",command=lambda : pick_browser())
    file_pick.grid(row=1,column=1)
    next_button =CTkButton(setup_wizard,text="NEXT",command=nxt)
    next_button.grid(row=2,column=1)
    dropdown = CTkComboBox(setup_wizard,values=["tiny","base","small","medium","Large-v3"])
    setup_wizard.mainloop()

def voice_recog():
    global AutoOut
    AutoOut = False
    Mainbox.insert(0,VoiceRecognition.recognise(int(Vals["VRT"]) if Vals["VRT"] != None else 10  , Vals["Voice_Model"] if Vals["Voice_Model"] != None else "base"))
    root.after(250,autoout)
    

#=========================================================================================================================
keyboard.add_hotkey('esc', estop)

#Initalise Window
root = CTk()

root.title("")
root.overrideredirect(True) 
root.geometry(f"550x160+{int((root.winfo_screenwidth() - 500) / 2)}+{int((root.winfo_screenheight() - 80) / 2)}")
root.attributes('-alpha',0.9)
set_appearance_mode("Dark")

#Main Entry box
Mainbox = CTkEntry(root,placeholder_text="Enter instructions to the AI model ...",width=500,height=80,fg_color="#2c2e35")
Mainbox.grid(row=0,column =0)
Mainbox.bind("<Return>",lambda event :enter(Mainbox.get()))
Mainbox.bind("<KeyRelease>", lambda event:textchange(Mainbox.get()))
VRB = CTkButton(root,text="Voice",command=voice_recog,width=50)
VRB.grid(row=0,column=1)
#Setup Box

CTkButton(root,width=480, text="SETUP WIZARD",fg_color="#2c2e35",command=setup).grid(row=2,column=0)

#AutoClose Code
root.bind("<FocusOut>", lambda event : autoclose(""))
root.after(10,lambda : autoout())

root.mainloop()
