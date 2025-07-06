import pyglet, tkinter, sys, json, asyncio, time, os
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub

#load settings for the app
with open('time.json', 'r') as file:
    timeLeftSettings = json.load(file)

with open('settings.json', 'r') as file:
    appsettings = json.load(file)

with open('twitch.json', 'r') as file:
    twitchsettings = json.load(file)

timeLeftInSeconds = timeLeftSettings['timeleft']
fontSize = 40
fontName = appsettings['font']
fontFilePath = appsettings['fontfile']
timeDaysColor = appsettings['timedayscolor']
timeLeftTextColor = appsettings['timelefttextcolor']
timeColor = appsettings['timecolor']
timeSeparatorColor = appsettings['timeseparatorcolor']
logFileDateFormat = appsettings['logdateformat']
bonusTimeAdd = appsettings['bonustimeplus']

APP_ID = twitchsettings['appid']
APP_SECRET = twitchsettings['appsecret']
TARGET_CHANNEL = appsettings['channel']
BOT_LISTEN_TO = appsettings['listento']
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file(fontFilePath)

#end settings
lastClickX = 0
lastClickY = 0
twitchConnected = False
addTime = 0
bonusTime = False
currentLogFile = {}
logFileTemplate = {
    "time": 0,
    "subs": {},
    "bonustime": {},
    "manual": {}
}
async def on_ready(ready_event: EventData):
    getOrCreateLogFile()
    await ready_event.chat.join_room(TARGET_CHANNEL)

# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    getOrCreateLogFile()
    if msg.user.name in BOT_LISTEN_TO:
        global addTime
        global bonusTime
        if msg.text == '!add60':
            addTime += 3600
            timeStamp = int(time.time()) 
            currentLogFile["manual"][timeStamp] = {
                "add": "60"
            }
            writeLogFile()
        elif msg.text == '!add30':
            addTime += 1800
            timeStamp = int(time.time()) 
            
            currentLogFile["manual"][timeStamp] = {
                "add": "30"
            }
            writeLogFile()
        elif msg.text == '!add15':
            addTime += 900
            timeStamp = int(time.time()) 
            currentLogFile["manual"][timeStamp] = {
                "add": "15"
            }
            writeLogFile()
        elif msg.text[:8] == '!addtime':
            userValue = int(msg.text[9:])
            secondsToMinutes = userValue/60
            addTime += userValue
            
            timeStamp = int(time.time()) 
            currentLogFile["manual"][timeStamp] = {
                "add": str(secondsToMinutes)
            }
            writeLogFile()
        if msg.text == '!add5':
            addTime += 450
            timeStamp = int(time.time()) 
            currentLogFile["manual"][timeStamp] = {
                "add": "5"
            }
            writeLogFile()
        if msg.text == '!clockbonustime':
            if bonusTime == True:
                bonusTime = False
                timeStamp = int(time.time()) 
                currentLogFile["bonustime"][timeStamp] = {
                    "event": "ended"
                }
                writeLogFile()
            else:
                bonusTime = True
                timeStamp = int(time.time()) 
                currentLogFile["bonustime"][timeStamp] = {
                    "event": "started"
                }
                writeLogFile()

def getOrCreateLogFile():
    global logFileDateFormat
    global currentLogFile
    global logFileTemplate

    logFileDate = time.strftime(logFileDateFormat)
    if "time" not in currentLogFile:
        logPath = 'Logs/' + logFileDate + '.json'
        if os.path.exists(logPath):
            with open(logPath, 'r') as file:
                    currentLogFile = json.load(file)
        else:
            currentLogFile = logFileTemplate
            writeLogFile()

def writeLogFile():
    global logFileDate
    global currentLogFile
    logFileDate = time.strftime(logFileDateFormat)
    logPath = 'logs/' + logFileDate + '.json'
    with open(logPath, "w") as outfile:
        outfile.write(json.dumps(currentLogFile))

async def on_sub(sub: ChatSub):
    global bonusTime
    global addTime
    global bonusTimeAdd
    global currentLogFile

    timeStamp = int(time.time()) 
    currentLogFile["subs"][timeStamp] = {
        "type": sub.sub_plan,
        "msg": sub.sub_message
    }
    writeLogFile()
    if bonusTime == True:
        addTime += 3600 + bonusTimeAdd #1h 15m
    else:
        addTime += 3600 #1h

async def run():
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_event(ChatEvent.SUB, on_sub)
    chat.start()
    try:
        input('press ENTER to close the clock\\n')
    finally:
        chat.stop() #stop chat listener
        await twitch.close() #disconnect from twitch
        sys.exit(0) #close whole app

def SaveLastClickPosition(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y

def DraggingWithMouse(event):
    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry("+%s+%s" % (x , y))

def countDownClockUpdate(timeLeftInSeconds):
    global addTime
    global timeLeftSettings

    if addTime > 0:
        timeLeftInSeconds += addTime
        addTime = 0
    
    timeLeftSettings['timeleft'] = timeLeftInSeconds
    timeLeftFilePath = 'time.json'
    with open(timeLeftFilePath, "w") as outfile:
        outfile.write(json.dumps(timeLeftSettings))
    
    if timeLeftInSeconds > 0:
        seconds = timeLeftInSeconds % 60
        minutes = int(timeLeftInSeconds / 60) % 60
        hours = int(timeLeftInSeconds / 3600) % 24
        
        if timeLeftInSeconds > 86400:
            days = int(timeLeftInSeconds / 86400)
            dayText = 'days'
            if days == 1:
                dayText = 'day'
            labelTimeDays = f"{days} {dayText}"
            canvas.itemconfig(labelDays, text=str(labelTimeDays))

        labelTimeHours = f"{hours:02}"
        canvas.itemconfig(labelHours1, text=str(labelTimeHours[0]))
        canvas.itemconfig(labelHours2, text=str(labelTimeHours[1]))
        labelTimeMinutes = f"{minutes:02}"
        canvas.itemconfig(labelMinutes1, text=str(labelTimeMinutes[0]))
        canvas.itemconfig(labelMinutes2, text=str(labelTimeMinutes[1]))
        labelTimeSeconds = f"{seconds:02}"
        canvas.itemconfig(labelSeconds1, text=str(labelTimeSeconds[0]))
        canvas.itemconfig(labelSeconds2, text=str(labelTimeSeconds[1]))
        root.after(1000, countDownClockUpdate, timeLeftInSeconds-1)

targetBgColor = appsettings['matchingedgecolor']
root = tkinter.Tk()
root.overrideredirect(True)
root.attributes('-topmost', True)
root.wm_attributes('-transparentcolor',targetBgColor)
root.config(highlightbackground=targetBgColor)

root.bind('<Button-1>', SaveLastClickPosition)
root.bind('<B1-Motion>', DraggingWithMouse)

root.title("Countdown TwitchApp")

if timeLeftInSeconds == 0:
    root.geometry('400x100')
    canvas = tkinter.Canvas(root, height=100, width=400, background=targetBgColor, bd=0, highlightthickness=0)
    canvas.pack()
    label = tkinter.Label(canvas,borderwidth=0,bg=targetBgColor)
    labelNoTimeLeft = canvas.create_text((200,30), text=str('No Time Left'), font=(fontName,fontSize-10), fill=timeLeftTextColor)  
elif timeLeftInSeconds > 86400:
    root.geometry('400x300')
    canvas = tkinter.Canvas(root, height=300, width=400, background=targetBgColor, bd=0, highlightthickness=0)
    canvas.pack()
    label = tkinter.Label(canvas,borderwidth=0,bg=targetBgColor)
    labelDays = canvas.create_text((200,30), text=str('daysnumber'), font=(fontName,fontSize), fill=timeDaysColor)
    labelHours1 = canvas.create_text((90,90), text=str('1'), font=(fontName,fontSize), fill=timeColor)
    labelHours2 = canvas.create_text((120,90), text=str('2'), font=(fontName,fontSize), fill=timeColor)
    labelTimeSeperatorOne = canvas.create_text((150,90), text=str(':'), font=(fontName,fontSize), fill=timeSeparatorColor)
    labelMinutes1 = canvas.create_text((180,90), text=str('1'), font=(fontName,fontSize), fill=timeColor)
    labelMinutes2 = canvas.create_text((210,90), text=str('2'), font=(fontName,fontSize), fill=timeColor)
    labelTimeSeperatorTwo = canvas.create_text((240,90), text=str(':'), font=(fontName,fontSize), fill=timeSeparatorColor)
    labelSeconds1 = canvas.create_text((270,90), text=str('1'), font=(fontName,fontSize), fill=timeColor)
    labelSeconds2 = canvas.create_text((300,90), text=str('2'), font=(fontName,fontSize), fill=timeColor)
    labelTimeLeft = canvas.create_text((200,150), text=str('Time Left'), font=(fontName,fontSize-10), fill=timeLeftTextColor)
else:
    root.geometry('400x200')
    canvas = tkinter.Canvas(root, height=200, width=400, background=targetBgColor, bd=0, highlightthickness=0)
    canvas.pack()
    label = tkinter.Label(canvas,borderwidth=0,bg=targetBgColor)
    labelHours1 = canvas.create_text((90,30), text=str('1'), font=(fontName,fontSize), fill=timeColor)
    labelHours2 = canvas.create_text((120,30), text=str('2'), font=(fontName,fontSize), fill=timeColor)
    labelTimeSeperatorOne = canvas.create_text((150,30), text=str(':'), font=(fontName,fontSize), fill=timeSeparatorColor)
    labelMinutes1 = canvas.create_text((180,30), text=str('1'), font=(fontName,fontSize), fill=timeColor)
    labelMinutes2 = canvas.create_text((210,30), text=str('2'), font=(fontName,fontSize), fill=timeColor)
    labelTimeSeperatorTwo = canvas.create_text((240,30), text=str(':'), font=(fontName,fontSize), fill=timeSeparatorColor)
    labelSeconds1 = canvas.create_text((270,30), text=str('1'), font=(fontName,fontSize), fill=timeColor)
    labelSeconds2 = canvas.create_text((300,30), text=str('2'), font=(fontName,fontSize), fill=timeColor)
    labelTimeLeft = canvas.create_text((200,90), text=str('Time Left'), font=(fontName,fontSize-10), fill=timeLeftTextColor)

countDownClockUpdate(timeLeftInSeconds)

canvas.create_window(0, 0, anchor=tkinter.NW, window=label)

if twitchConnected == False:
    twitchConnected = True
    asyncio.run(run())

root.mainloop()