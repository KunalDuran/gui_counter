import tkinter as tk
from tkinter import *
import time, json, os, datetime
from tkinter import ttk
from tkcalendar import *
import pymongo


CONFIG = 'config.json'
clock_running = False


if not os.path.exists(CONFIG):
    with open(CONFIG, 'w') as f:
        data = {}
        data['time'] = 0
        data['already_studied'] = 0
        data['target_date'] = 0
        data['username'] = ""
        data['user_mail'] = ""
        json.dump(data, f)


def load_config():
    with open(CONFIG, 'r+') as f:
        data = json.load(f)
    return data


def write_to_config(data):
    with open(CONFIG, 'r+') as f:
        f.seek(0)
        f.truncate(0)
        json.dump(data, f)



def start():
    global clock_running
    clock_running = True

    data = load_config()
    already = data['already_studied']

    if already != 0: 
        data['time'] = time.time()
        data['already_studied'] = already
        write_to_config(data)      
    else:
        data['time'] = time.time()
        write_to_config(data)


    def start_timer():
        if clock_running:
            ass = round(time.time() - data['time'])
            text.configure(text=f"Time Spent : {datetime.timedelta(seconds=ass+round(data['already_studied']))}")
            text.after(1000, start_timer)
    start_timer()


def pause():
    global clock_running
    if clock_running:
        data = load_config()
        already = data['already_studied']
        start_time = data['time']
        data['already_studied'] = time.time() - start_time + already
        data['time'] = 0
        write_to_config(data)
    clock_running = False



def reset():
    global clock_running, paused
    try: text.configure(text=f'Time Spent : 00:00:00')
    except: pass
    data = load_config()
    data['time'] = 0
    data['already_studied'] = 0
    write_to_config(data)
    clock_running = False


window = tk.Tk()
window.title("Time Tracker")

# this removes the maximize button
window.resizable(0, 0)
window_height = 450
window_width = 600

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
# window.geometry('880x600')
window.configure(background='#ffffff')


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

tabControl = ttk.Notebook(window)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Time Tracker')
tabControl.add(tab2, text='Goal Timeout')
tabControl.add(tab3, text='Streak Counter')
tabControl.add(tab4, text='Leader Board')

tabControl.pack(expand=1, fill="both")





############################  TAB 1 CONTENT ##################################

#### TIME TRACKER BAR
study_time = load_config()['already_studied']
study_time = str(datetime.timedelta(seconds=round(study_time)))
text = tk.Label(tab1, text=f"Time Spent : {study_time}", width=45, height=2, fg="white", bg="#333333",
                    font=('times', 18, 'bold', 'underline'))
text.place(x=0, y=50)

#### START BUTTON
start_btn = tk.Button(tab1, text="Start", command=start, fg="white", bg="#525252", width=15,
                    height=2,
                    activebackground="#118ce1", font=('times', 15, ' bold '))
start_btn.place(x=10, y=275)

#### PAUSE BUTTON
pause_btn = tk.Button(tab1, text="Pause", command=pause, fg="white", bg="#525252", width=15,
                        height=2,
                        activebackground="#118ce1", font=('times', 15, ' bold '))
pause_btn.place(x=205, y=275)

#### RESET BUTTON
reset_btn = tk.Button(tab1, text="Reset", command=reset, fg="white", bg="#525252",
                        width=15,
                        height=2,
                        activebackground="#118ce1", font=('times', 15, ' bold '))
reset_btn.place(x=400, y=275)





############################  TAB 2 CONTENT ##################################
def remaining_days(target_date=None):
    today = datetime.datetime.utcnow()
    if not target_date: target_date = today
    return (target_date - today).days



def calender_pop():
    today = datetime.datetime.utcnow()
    cal = Calendar(tab2, selectmode='day',year=today.year, month=today.month, day=today.day)
    cal.pack(pady=90)
    
    def get_date():
        target_date = datetime.datetime.strptime(cal.get_date() , '%m/%d/%y')
        data = load_config()
        data['target_date'] = remaining_days(target_date)
        write_to_config(data)
        cal.destroy()
        cal_btn.destroy()
        dayLeft.config(text=f"Days Remaining is : {remaining_days(target_date)}")
    cal_btn = tk.Button(tab2, text='Select', command=get_date)
    cal_btn.place(x=275, y=275)


dayLeft = tk.Label(tab2, text=f"Days Remaining : {load_config()['target_date']}", width=45, height=2, fg="white", bg="#333333",
                    font=('times', 18, 'bold', 'underline'))
dayLeft.place(x=0, y=30)


pause_btn = tk.Button(tab2, text="Set Date", command=calender_pop, fg="white", bg="#525252", width=15,
                        height=2,
                        activebackground="#118ce1", font=('times', 15, ' bold '))
pause_btn.place(x=205, y=300)


############################  TAB 3 CONTENT ##################################



############################  TAB 4 CONTENT ##################################
def load_database_collection():
    dbConn = pymongo.MongoClient('mongodb+srv://<user>:<pass>@guicountercluster.om69r.mongodb.net/<db>?retryWrites=true&w=majority')
    db = dbConn['guiCounterCluster']
    collection = db['record']
    return collection


def update_leaderboard():
    data = load_config()
    collection = load_database_collection()
    collection.update_one({'_id': data['user_mail']}, {'$set':{'today': data['already_studied']}})
    players = collection.find({})
    players = sorted(list(players), key= lambda x: x['today'], reverse=True)

    for player_label in tab4.pack_slaves():
        if type(player_label) == tk.Label:
            player_label.pack_forget()
    
    display_leaderboard(players)

if not load_config()['username']:
    def register_user():
        username = register_user_entry.get()
        usermail = register_usermail_entry.get()
        data = load_config()
        data['username'] = username
        data['user_mail'] = usermail
        write_to_config(data)
        
        register_user_entry.destroy()
        register_usermail_entry.destroy()
        registerBtn.destroy()
        # registerBtn.config(text='Reset User')
        collection = load_database_collection()
        try: collection.insert_one({'_id': usermail, 'username': username, 'today': data['already_studied']})
        except: pass
        refreshLeaderboardBtn = tk.Button(tab4, text='Refresh' ,command=update_leaderboard, height=1, width=14, fg="white", bg="#525252")
        refreshLeaderboardBtn.pack(side=BOTTOM)

    register_user_entry = tk.Entry(tab4, width=25)
    register_user_entry.insert(0,'Enter Name')
    register_user_entry.place(x=0, y=403)
    register_usermail_entry = tk.Entry(tab4, width=35)
    register_usermail_entry.insert(0,'Enter Email Id')
    register_usermail_entry.place(x=150, y=403)
    registerBtn = tk.Button(tab4, text='Register', command=register_user , height=1, width=7, fg="white", bg="#525252", font=('times',8))
    registerBtn.place(x=350, y=403)
else:
    refreshLeaderboardBtn = tk.Button(tab4, text='Refresh' ,command=update_leaderboard, height=1, width=14, fg="white", bg="#525252")
    refreshLeaderboardBtn.pack(side=BOTTOM)

        


players = load_database_collection().find({})
players = sorted(list(players), key= lambda x: x['today'], reverse=True)
# players = [{'username': 'Kunal', 'today': 10, 'this_week': 100}, {'username': 'Puneet', 'today': 10, 'this_week': 130}]

def display_leaderboard(players):
    for score in players:
        tk.Label(tab4, text=f"{score['username']} > Today : {str(datetime.timedelta(seconds=round(score['today'])))}", 
                        width=45, height=2, fg="white", bg="#3c4256",
                        font=('times', 18, 'bold')).pack(pady=2)
                      
display_leaderboard(players)





############################  FOOTER CONTENT ##################################
link2 = tk.Label(window, text="Copyright©2020, kunalduran.com", fg="blue", font=('times',8) )
link2.place(x=430, y=430)


def site(link):
    import webbrowser
    webbrowser.open(link)
link2.bind("<Button-1>", lambda e: site("https://www.kunalduran.com"))
label = tk.Label(window)


window.mainloop()

## 
## pyinstaller --onefile --noconsole --hidden-import babel.numbers myscript.py