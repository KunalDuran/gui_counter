import tkinter as tk
from tkinter import *
import time, json, os, datetime

CONFIG = 'config.json'
clock_running = False
paused = True


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
    with open(CONFIG, 'w') as f:
        data = {}
        data['time'] = 0
        data['already_studied'] = 0
        json.dump(data, f)
    clock_running = False
    paused = False

def remaining_days():
    target_date = datetime.datetime(2021,6,27)
    today = datetime.datetime.utcnow()
    return (target_date - today).days


if not os.path.exists(CONFIG):
    reset()


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

header = tk.Label(window, text="Time Tracker", width=45, height=2, fg="white", bg="#333333",
                    font=('times', 18, 'bold', 'underline'))
header.place(x=0, y=0)


# study_time = json.load(open(CONFIG))['already_studied']
# study_time = str(datetime.timedelta(seconds=round(study_time)))
text = tk.Label(window, text=f"Time Spent : 00:00:00", width=45, height=2, fg="white", bg="#333333",
                    font=('times', 18, 'bold', 'underline'))
text.place(x=0, y=90)

'''
def display_time(study_time):
    study_time = str(datetime.timedelta(seconds=round(study_time)))
    text = tk.Label(window, text=f"Time Spent {study_time}", width=45, height=2, fg="white", bg="#333333",
                        font=('times', 18, 'bold', 'underline'))
    text.place(x=0, y=90)

display_time(study_time)'''






var = StringVar()
var.set(str(remaining_days()))
dayLeft = tk.Label(window, text=f"Days Remaining : {var.get()}", width=45, height=2, fg="white", bg="#333333",
                    font=('times', 18, 'bold', 'underline'))
dayLeft.place(x=0, y=180)


start_btn = tk.Button(window, text="Start", command=start, fg="white", bg="#525252", width=15,
                    height=2,
                    activebackground="#118ce1", font=('times', 15, ' bold '))
start_btn.place(x=10, y=350)

pause_btn = tk.Button(window, text="Pause", command=pause, fg="white", bg="#525252", width=15,
                        height=2,
                        activebackground="#118ce1", font=('times', 15, ' bold '))
pause_btn.place(x=205, y=350)

reset_btn = tk.Button(window, text="Reset", command=reset, fg="white", bg="#525252",
                        width=15,
                        height=2,
                        activebackground="#118ce1", font=('times', 15, ' bold '))
reset_btn.place(x=400, y=350)


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


def update_day_count():
    dayLeft.configure(text=f"Days Remaining : {str(remaining_days())}")
    dayLeft.after(1000, update_day_count)




update_day_count()

window.mainloop()