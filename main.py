
from customtkinter import *
import sys
from tkinter import PhotoImage , filedialog
from groq import Groq
import subprocess
import keyboard
import pyautogui
import io
import base64
import aiendpoint
import localmodel
import time
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
try:
    with open("C:\\ProgramData\\JarVis.txt","x",encoding="utf+8") as data:
        pass
except FileExistsError as e:
    has_vals = True
    with open("C:\\ProgramData\\JarVis.txt","r",encoding="utf+8") as data:
            print(data.read())


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
        "CRITICAL: Look at the screenshot. If the task described in the instructions is done or the previous message(s) have already executed your task move on to the next one "
        +pmsgstr
    )

    msg = aiendpoint.req(full_prompt,mime_type,b64img)
    print(msg)
    previousmsg.append(msg)
    
    if msg == "{DONE}":
        sys.exit()
    elif "CTE" in msg:
        flash()
        X = int(msg.split("|")[0].split("(")[1].split(")")[0].split[0])
        Y = int(msg.split("|")[0].split("(")[1].split(")")[0].split[1])
        text = msg.split("|")[1].split("\"")[1]
        pyautogui.click(X,Y)
        keyboard.write(text)
        pyautogui.press("enter")
    elif msg == "{BROWSER}":
        flash()
        subprocess.Popen(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe")
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
        root.geometry(f"500x160+{int((root.winfo_screenwidth() - 500) / 2)}+{int((root.winfo_screenheight() - 80) / 2)}")
    else:
        root.geometry(f"500x80+{int((root.winfo_screenwidth() - 500) / 2)}+{int((root.winfo_screenheight() - 80) / 2)}")


def setup():
    global AutoOut
    AutoOut = False
    global Vals
    Vals = {}
    default_browser = ''
    #Default Browser
    def dbset():
        default_browser = filedialog.askopenfilename(
                    title="SELECT YOUR DEFAULT BROWSER",
                    initialdir="%USERPROFILE%",
                    filetypes=[("Windows Executables (Your Browser)","*.exe")]
                )
        btn1.configure(text="Current Browser :"+default_browser)
        Vals["Browser"] = default_browser

    def nxt():
        global Vals
        DB.withdraw()
        
        AApi = CTkToplevel()
        def Api():
            global Vals
            Vals["Endpoint"] = E1
            Vals["Auth"] = E2
            Vals["Model"] = E3
            AApi.withdraw()
            global AutoOut
            AutoOut = True

        E1 = CTkEntry(AApi,placeholder_text="Enter Your Api Endopint :")
        E1.grid()
        E2 = CTkEntry(AApi,placeholder_text="Enter Your Api Key : ")
        E2.grid()
        E3 = CTkEntry(AApi,placeholder_text="Enter Your Ai Model :  ")
        E3.grid()
        CTkButton(AApi,text="Next",command=Api).grid()
        AApi.mainloop() 

        with open("C:\\ProgramData\\JarVis.txt","w") as file :
            file.write(str(Vals))

    DB = CTkToplevel()
    btn1 = CTkButton(DB,text="Current Browser : None",command=dbset)
    btn1.grid()
    CTkButton(DB , text="Next",command=nxt).grid(row=1)
    DB.mainloop()





#=========================================================================================================================
keyboard.add_hotkey('esc', estop)

#Initalise Window
root = CTk()

root.title("")
root.overrideredirect(True) 
root.geometry(f"500x160+{int((root.winfo_screenwidth() - 500) / 2)}+{int((root.winfo_screenheight() - 80) / 2)}")
root.attributes('-alpha',0.9)
set_appearance_mode("Dark")

#Main Entry box
Mainbox = CTkEntry(root,placeholder_text="Enter instructions to the AI model ...",width=500,height=80,fg_color="#2c2e35")
Mainbox.grid(row=0,column =0)
Mainbox.bind("<Return>",lambda event :enter(Mainbox.get()))
Mainbox.bind("<KeyRelease>", lambda event:textchange(Mainbox.get()))

#Setup Box

CTkButton(root,width=480, text="SETUP WIZARD",fg_color="#2c2e35",command=setup).grid(row=2,column=0)

#AutoClose Code
root.bind("<FocusOut>", lambda event : autoclose(""))
root.after(10,lambda : autoout())
if not has_vals:
    root.after(50,lambda event : setup())
root.mainloop()