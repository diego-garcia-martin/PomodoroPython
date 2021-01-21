import tkinter as tk
import datetime

class Timer():
    def __init__(self, workTime):
        self.totalTime = workTime * 60
        self.time = self.totalTime
        self.running = False

    def restartTimer(self):
        self.time = self.totalTime
        self.running = False

    def resetTimer(self, workTime):
        self.totalTime = workTime * 60
        self.time = self.totalTime
        self.running = False

    def startTimer(self):
        self.running = True

    def pauseTimer(self):
        self.running = False

    def updateTimer(self):
        if self.running:
            self.time -= 1
            if self.time <= 0:
                self.running = False
                return False
        return True
                

class UI():
    def __init__(self, work, rest, longRest, periods, width=500, height=300):
        self.window = tk.Tk()
        self.window.resizable(False, False);
        self.window.title("Pomodoro Timer")
        self.photoIcon = tk.PhotoImage(file="tomato.png")
        self.window.iconphoto(False, self.photoIcon)
        self.work = work
        self.rest = rest
        self.longRest = longRest
        self.periods = periods
        self.periodCount = self.periods
        self.state = "WORKING"
        self.timer = Timer(self.work)
        self.width = width
        self.height = height
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.configure(background="black")
        self.setWidgets()

    def setWidgets(self):
        self.frame = tk.Frame(self.window, bg="#4a4a4a")
        self.frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        self.stateLabel = tk.Label(self.frame, text=self.state, font=("Arial", 28), bg="#4a4a4a")
        self.stateLabel.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.25)
        self.label = tk.Label(self.frame, text=f"{datetime.timedelta(seconds=self.timer.time)}", font=("Arial", 32), bg="#4a4a4a")
        self.label.place(relx=0.20, rely=0.3, relwidth=0.6, relheight=0.25)
        self.startButton = tk.Button(self.frame, text="Start", font=("Arial", 18), bg="gray", command=self.startTimerLoop)
        self.startButton.place(relx=0.15, rely=0.6, relwidth=0.3, relheight=0.15)
        self.pauseButton = tk.Button(self.frame, text="Pause", font=("Arial", 18), bg="gray", command=self.stopTimerLoop)
        self.pauseButton.place(relx=0.55, rely=0.6, relwidth=0.3, relheight=0.15)
        self.resetButton = tk.Button(self.frame, text="Restart", font=("Arial", 18), bg="gray", command=self.resetTimerLoop)
        self.resetButton.place(relx=0.15, rely=0.8, relwidth=0.3, relheight=0.15)
        self.configButton = tk.Button(self.frame, text="Config", font=("Arial", 18), bg="gray", command=self.configTimer)
        self.configButton.place(relx=0.55, rely=0.8, relwidth=0.3, relheight=0.15)

    def configTimer(self):
        self.newWin = tk.Tk()
        self.newWin.title("Configuration")
        self.newWin.configure(background="#4a4a4a")
        self.l_work = tk.Label(self.newWin, text="Working time:", font=("Arial", 18), bg="#4a4a4a").grid(row=0, column=0)
        self.l_rest = tk.Label(self.newWin, text="Resting time:", font=("Arial", 18), bg="#4a4a4a").grid(row=1, column=0)
        self.l_longrest = tk.Label(self.newWin, text="Long Rest time:", font=("Arial", 18), bg="#4a4a4a").grid(row=2, column=0)
        self.l_period = tk.Label(self.newWin, text="Working Periods:", font=("Arial", 18), bg="#4a4a4a").grid(row=3, column=0)
        self.e_work = tk.Entry(self.newWin, font=("Arial", 18))
        self.e_work.grid(row=0, column=1, padx=50)
        self.e_rest = tk.Entry(self.newWin, font=("Arial", 18))
        self.e_rest.grid(row=1, column=1, padx=50)
        self.e_longrest = tk.Entry(self.newWin, font=("Arial", 18))
        self.e_longrest.grid(row=2, column=1, padx=50)
        self.e_period = tk.Entry(self.newWin, font=("Arial", 18))
        self.e_period.grid(row=3, column=1, padx=50)
        self.btn_conf = tk.Button(self.newWin, text="Apply", font=("Arial", 18), bg="gray", command= self.applyChanges).grid(row=4, column=0)
        self.btn_cancel = tk.Button(self.newWin, text="Cancel", font=("Arial", 18), bg="gray", command= self.newWin.destroy).grid(row=4, column=1, padx=50)
        self.e_work.insert(0, self.work)
        self.e_rest.insert(0, self.rest)
        self.e_longrest.insert(0, self.longRest)
        self.e_period.insert(0, self.periods)
        self.newWin.mainloop()

    def applyChanges(self):
        self.work = int(self.e_work.get())
        self.rest = int(self.e_rest.get())
        self.longRest = int(self.e_longrest.get())
        self.periods = int(self.e_period.get())
        self.timer.resetTimer(self.work)
        self.label['text'] = f"{datetime.timedelta(seconds=self.timer.time)}"
        self.newWin.destroy()

    def timerLoop(self):
        if not self.timer.updateTimer():
            self.updateState()
        self.label['text'] = f"{datetime.timedelta(seconds=self.timer.time)}"
        if self.timer.running:
            self.frame.after(1000, self.timerLoop)
    
    def startTimerLoop(self):
        if not self.timer.running:
            self.timer.startTimer()
            self.timerLoop()

    def stopTimerLoop(self):
        if self.timer.running:
            self.timer.pauseTimer()
            self.timerLoop()

    def resetTimerLoop(self):
        self.timer.restartTimer()
        self.timerLoop()

    def updateState(self):
        if self.state == "WORKING" and self.periodCount > 0:
            self.periodCount -= 1
            self.state = "RESTING"
            self.timer.resetTimer(self.rest)
        elif self.state == "WORKING" and self.periodCount <= 0:
            self.periodCount = self.periods
            self.state = "LONG REST"
            self.timer.resetTimer(self.longRest)
        else:
            self.state = "WORKING"
            self.timer.resetTimer(self.work)
        self.stateLabel.config(text=self.state)
        self.startTimerLoop()


    def mainloop(self):
        self.window.mainloop()

app = UI(25, 5, 15, 3)
app.mainloop()