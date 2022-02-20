import tkinter as tk
from tkinter import *
import time, json, os, datetime
from tkinter import ttk
from tkcalendar import *


CONFIG = 'config.json'
clock_running = False
paused = True
if not os.path.exists(CONFIG):
    with open(CONFIG, 'w') as f:
        data = {}
        data['time'] = 0
        data['already_studied'] = 0
        data['target_date'] = 0
        json.dump(data, f)




def start():
    global clock_running
    clock_running = True

    with open(CONFIG, 'r+') as f:
        data = json.load(f)
        already = data['already_studied']

        if already != 0: 
            data['time'] = time.time()
            data['already_studied'] = already
            f.seek(0)
            f.truncate(0)
            json.dump(data, f)
            
        else:
            data['time'] = time.time()
            f.seek(0)
            f.truncate(0)
            json.dump(data, f)
    def start_timer():
        if clock_running:
            ass = round(time.time() - data['time'])
            text.configure(text=f"Time Spent : {datetime.timedelta(seconds=ass+round(data['already_studied']))}")
            text.after(1000, start_timer)
    start_timer()


def pause():
    global clock_running
    with open(CONFIG, 'r+') as f:
        data = json.load(f)
        already = data['already_studied']

        # print(study_time, "study time")
        start_time = data['time']
        data['already_studied'] = time.time() - start_time + already
        # display_time(data['already_studied'])
        data['time'] = 0
        f.seek(0)
        f.truncate(0)
        json.dump(data, f)
    clock_running = False
    global pause
    pause = True



def reset():
    global clock_running, paused
    try: text.configure(text=f'Time Spent : 00:00:00')
    except: pass
    with open(CONFIG, 'r+') as f:
        data = json.load(f)
        data['time'] = 0
        data['already_studied'] = 0
        f.seek(0)
        f.truncate(0)
        json.dump(data, f)
    clock_running = False
    paused = False


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

tabControl.add(tab1, text='Time Tracker')
tabControl.add(tab2, text='Goal Timeout')
tabControl.add(tab3, text='Streak Counter')

tabControl.pack(expand=1, fill="both")

# header = tk.Label(window, text="Time Tracker", width=45, height=1, fg="white", bg="#333333",
#                     font=('times', 18, 'bold', 'underline'))
# header.place(x=0, y=20)










############################  TAB 1 CONTENT ##################################

#### TIME TRACKER BAR
study_time = json.load(open(CONFIG))['already_studied']
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
    # target_date = datetime.datetime(2021,6,27)
    today = datetime.datetime.utcnow()
    if not target_date: target_date = today
    return (target_date - today).days



def calender_pop():
    today = datetime.datetime.utcnow()
    cal = Calendar(tab2, selectmode='day',year=today.year, month=today.month, day=today.day)
    cal.pack(pady=90)
    
    def get_date():
        target_date = datetime.datetime.strptime(cal.get_date() , '%m/%d/%y')
        with open(CONFIG, 'r+') as f:
            data = json.load(f)
            data['target_date'] = remaining_days(target_date)
            f.seek(0)
            f.truncate(0)
            json.dump(data, f)

        cal.destroy()
        cal_btn.destroy()
        dayLeft.config(text=f"Days Remaining is : {remaining_days(target_date)}")
    cal_btn = tk.Button(tab2, text='Select', command=get_date)
    cal_btn.place(x=275, y=275)


dayLeft = tk.Label(tab2, text=f"Days Remaining : {json.load(open(CONFIG))['target_date']}", width=45, height=2, fg="white", bg="#333333",
                    font=('times', 18, 'bold', 'underline'))
dayLeft.place(x=0, y=30)


pause_btn = tk.Button(tab2, text="Set Date", command=calender_pop, fg="white", bg="#525252", width=15,
                        height=2,
                        activebackground="#118ce1", font=('times', 15, ' bold '))
pause_btn.place(x=205, y=300)





############################  TAB 3 CONTENT ##################################



############################  FOOTER CONTENT ##################################
link2 = tk.Label(window, text="Copyright©2020, kunalduran.com", fg="blue", font=('times',8) )
link2.place(x=430, y=430)
def site(link):
    import webbrowser
    webbrowser.open(link)
link2.bind("<Button-1>", lambda e: site("https://www.kunalduran.com"))
label = tk.Label(window)

def update_timer():
    start()
    text.configure(text=f"Time Spent : {str()}")
    # text.after(1000, update_day_count)


# def update_day_count():
#     dayLeft.configure(text=f"Days Remaining : {str(remaining_days())}")
#     dayLeft.after(1000, update_day_count)




# update_day_count()

window.mainloop()