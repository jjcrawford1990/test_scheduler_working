# import full tkinter module
import tkinter as tk  # renaming tkinter to tk for ease and efficiency
from tkinter import *  # this is importing all (*) modules from the tkinter package
import train as TrainModule #also begins to run main loop of this module
from train import train #import train object created in train module
from datetime import *

# default background colour
dbg = '#334157'
# default fg colours (font colour)
dfg = 'silver'
dfg2 = 'white'
actualbg = 'dodgerblue3'
# default fonts
dfont = 'courier 11 bold underline'
dfont2 = 'courier 11'
dfont3 = 'helvetica 15 bold italic underline'
dfont4 = 'helvetica 6 bold underline'
dfont5 = 'courier 8 bold' #font for tasks

# generate main window class and populate with windows and buttons

class Proj_select:

    def __init__(self, master):
        self.master = master #assign master parameter an attribute
        self.master.title('Test Scheduler')
        self.master.geometry('1320x600')
        self.master.configure(bg=dbg)
        self.fMainframe = Frame(self.master) #create our upper frame attribute, with master as the toplevel widget
        self.fMainframe.grid()
        self.user_choice()

    def user_choice(self):
        self.visible_days = IntVar()
        self.fRangeselection = Frame(self.fMainframe)
        self.fRangeselection.grid(row=0, column=0) #grid must be seperate line or frame cannot be destroyed
        self.lRangeoptions = Label(self.fRangeselection, text='Choose\nDesired\nRange:').grid(row=1, column=0, columnspan=1, rowspan=3, sticky=E)
        self.bSelectweek = Radiobutton(self.fRangeselection, text='1 Week', variable=self.visible_days, value=7).grid(row=1, column=1)
        self.bSelectfortnight = Radiobutton(self.fRangeselection, text='2 Weeks', variable=self.visible_days, value=14).grid(row=2, column=1)
        self.bSelectmonth = Radiobutton(self.fRangeselection, text='Month', variable=self.visible_days, value=30).grid(row=3, column=1)
        self.bRangeselection = Button(self.fRangeselection, text='OK', command=self.frame_set).grid(row=4, column=0, columnspan=2, ipadx=80)

    # method definition of which project shall be ran, then calls the suitable method
    def frame_set(self):
        self.no_days=self.visible_days.get() #get the new value set using radio button, and assign to no_days WHY DO I NEED TO DO THIS???
        self.cellwidth = int(230/self.no_days)
        self.fRangeselection.destroy()  #destroy setting frame
        mainapplication = Viewing_range(self.fMainframe) #create instance of Viewing_range class, pass main frame widget to viewing range class

class Viewing_range(tk.Frame):

    def __init__(self, master):
        self.master = master #master is fMainframe
        self.fRangewindow = Frame(master, bg=dbg)
        self.fRangewindow.grid(row=0, rowspan = TrainModule.Train.no_trains + 2, column=0, columnspan=mainapp.no_days + 1, sticky=NSEW)
        self.title_image = PhotoImage(file='C:\\Users\\Josh\\Desktop\\naytstitle.gif')
        self.lTitle = Label(self.fRangewindow, image=self.title_image, bg=dbg)
        self.lTitle.grid(row=0, column=0, columnspan = mainapp.no_days + 2, sticky=NSEW)
        self.bAddtrain = Button(self.fRangewindow, text='Add Trainset', command=self.addTrain)
        self.bAddtrain.grid(row=(TrainModule.Train.no_trains*2)+2, column=0, columnspan = int(mainapp.no_days*0.25))
        self.bApplyscenario = Button(self.fRangewindow, text='Apply Scenario', command=self.scenarioselect)
        self.bApplyscenario.grid(row=(TrainModule.Train.no_trains*2)+2, column=int((mainapp.no_days+1)*0.25), columnspan = int(mainapp.no_days*0.25))
        self.bDisplayend = Button(self.fRangewindow, text='Display End Dates')
        self.bDisplayend.grid(row=(TrainModule.Train.no_trains*2) + 2, column=int((mainapp.no_days+1)*0.5), columnspan = int(mainapp.no_days*0.25))
        self.bSave = Button(self.fRangewindow, text='Save Changes')
        self.bSave.grid(row=(TrainModule.Train.no_trains*2)+2, column=int((mainapp.no_days+1)*0.75), columnspan = int(mainapp.no_days*0.25))
        self.range_populate() #run range populate method, seperate to allow for range changing without re-writing whole window
        print(TrainModule.Train.no_trains)

    def range_populate(self):
        for i in range(TrainModule.Train.no_trains): #for loop to populate the train row
            instanceholder = 'Train ' + str(train[i].unit_number) #create a temporary variable for storing the new label attribute name
            self.trainlabel= Label(self.fRangewindow, text=instanceholder, bg='white', fg=dbg, font=dfont, borderwidth=1, relief="sunken").grid(row=(i*2)+2, rowspan = 2, column=0,sticky=NSEW) #create a label
            self.lideal = Label(self.fRangewindow, text='Plan:', bg=dbg, fg=dfg2, font=dfont4).grid(row=(i*2)+2, column=1)
            self.lactual = Label(self.fRangewindow, text='Live:', bg=dbg, fg=dfg2, font=dfont4).grid(row=(i*2)+3, column=1)
            for n in range(mainapp.no_days):
                delta_date = date.today() + timedelta(days=n) #calculate iterated date
                try: #try and retrieve element of key which is current date
                    instanceholder2 = TrainModule.Train.task_types.get(train[i].schedule[delta_date]) #get dict element from key
                    self.ltask = Label(self.fRangewindow, text = instanceholder2, bg=dbg, fg=dfg2).grid(row=(i*2)+2, column=n+2)
                except KeyError: #if the dictionary does not have this key/date (e.g. not started, train left), put blank in cell
                    self.ltask = Label(self.fRangewindow, text="    ", bg='red').grid(row=(i*2) + 2, column=n + 2)
                try:
                    instanceholder3 = TrainModule.Train.task_types.get(train[i].live_schedule[delta_date])
                    self.lactual_task = Label(self.fRangewindow, text=instanceholder3, bg=actualbg, fg=dfg2).grid(row=(i * 2) + 3, column=n + 2)
                except KeyError:  # if the dictionary does not have this key/date (e.g. not started, train left), put blank in cell
                    self.lactual_task = Label(self.fRangewindow, text="    ", bg='red').grid(row=(i * 2) + 3, column=n + 2)

        for i in range(mainapp.no_days):
            date_increase = date.today() + timedelta(i)
            instanceholder = date.__format__(date_increase, '%a %d %b')
            self.daylabel = Label(self.fRangewindow, text = instanceholder + '|', bg=dbg, fg=dfg2, font=dfont4, width=mainapp.cellwidth).grid(row=1, column=i+2, sticky=NSEW)

    def scenarioselect(self):
        self.scenario_live_selection = StringVar() #tkinter Stringvar
        self.scenario_live_selection.set("Choose:") #Default tkinter value for option menu first value
        # PUT THE BELOW INTO TRAIN MODULE ONCE WORKING
        self.scenario_options_tuple = ["STI123: Train On Fire", "STI456: Davey Mode", "MOD789: Make Train Well"]
        self.fScenariowindow = Frame(self.master)
        self.fScenariowindow.grid(row=3, column=0, padx=100, pady=100)
        lScenariotitle = Label(self.fScenariowindow, text='Scenario Options')
        lScenariotitle.grid(row=3, column=0, columnspan=2)
        scenario_options = OptionMenu(self.fScenariowindow, self.scenario_live_selection, *self.scenario_options_tuple)  #option menu
        scenario_options.grid(row=4, column=0, columnspan=2)
        self.bchooseScenario = Button(self.fScenariowindow, text='Set!', command=lambda:[self.datechoose(), self.bchooseScenario.destroy(), self.bexitScenario.destroy()])
        self.bchooseScenario.grid(row=5, column=0)
        self.bexitScenario = Button(self.fScenariowindow, text='Exit', command=lambda:[self.fScenariowindow.destroy, self.choosebutton.destroy])
        self.bexitScenario.grid(row=5, column=1)

    def datechoose(self):
        self.date_live_selection = StringVar()  # tkinter Stringvar
        self.date_live_selection.set("Choose Date:")  # Default tkinter value for option menu first value
        # PUT THE BELOW INTO TRAIN MODULE ONCE WORKING
        self.date_options_tuple = ["Today", "Tommorow", "04/07/2096"]
        lDatechoicetitle = Label(self.fScenariowindow, text='Implementation Date:')
        lDatechoicetitle.grid(row=5, column=0, columnspan=2)
        date_options = OptionMenu(self.fScenariowindow, self.date_live_selection, *self.date_options_tuple)  # option menu
        date_options.grid(row=6, column=0, columnspan=2)
        self.bchooseScenarioDate = Button(self.fScenariowindow, text='Set!', command=self.optionchoose)
        self.bchooseScenarioDate.grid(row=7, column=0)
        self.bexitScenario2 = Button(self.fScenariowindow, text='Exit', command=self.fScenariowindow.destroy)
        self.bexitScenario2.grid(row=7, column=1)

    def optionchoose(self):
        self.scenario_choice = self.scenario_live_selection.get()  #take tk stringvar and assign to str variable
        self.date_choice = self.date_live_selection.get()  # take tk stringvar and assign to str variable
        self.fScenariowindow.destroy()
        self.lshow_scenario_choice = Label(self.fRangewindow, text=self.scenario_choice + ' Applied, ' + self.date_choice, bg=dbg, fg=dfg2, font=dfont2, borderwidth=2, relief="sunken").grid(row=20, column=0, columnspan=mainapp.no_days+1, sticky=NSEW) #create a label

    def addTrain(self):
        self.project_selection = StringVar()  # tkinter Stringvar
        self.default_schedule_selection = StringVar()  # tkinter Stringvar
        self.fAddtrain = Frame(self.master)
        self.fAddtrain.grid(row=3, column=0, padx=100, pady=100)
        lAddtraintitle = Label(self.fAddtrain, text='Add Train')
        lAddtraintitle.grid(row=4, column=0, columnspan=3)
        lProject = Label(self.fAddtrain, text='Choose Project')
        lProject.grid(row=5, column=0, columnspan=3)
        project_tuple = ['ASR', 'IEP', 'Milano']
        project_options = OptionMenu(self.fAddtrain, self.project_selection, *project_tuple)  # option menu
        project_options.grid(row=5, column=1, columnspan=1)
        lUnitnumber = Label(self.fAddtrain, text='Unit No:')
        lUnitnumber.grid(row=6, column=0, columnspan=1)
        self.eUnitnumber = Entry(self.fAddtrain)
        self.eUnitnumber.grid(row=6, column=1, columnspan=1)
        lDate = Label(self.fAddtrain, text='Start Date\n(0=Today,7=7days from now):')
        lDate.grid(row=7, column=0, columnspan=1)
        self.eDateset = Entry(self.fAddtrain)
        self.eDateset.grid(row=7, column=1, columnspan=1)
        lDefaultschedule = Label(self.fAddtrain, text='Choose Schedule')
        lDefaultschedule.grid(row=8, column=0, columnspan=1)
        def_schedule_tuple = tuple(TrainModule.Train.schedules.keys())
        def_schedule_options = OptionMenu(self.fAddtrain, self.default_schedule_selection, *def_schedule_tuple)  # option menu
        def_schedule_options.grid(row=8, column=1, columnspan=2)
        self.bSetunitnumber = Button(self.fAddtrain, text='Set!', command=self.unitSave)
        self.bSetunitnumber.grid(row=9, column=0, columnspan=3)

    def unitSave(self):
        self.new_train = self.eUnitnumber.get()
        self.project_choice = self.project_selection.get()
        self.start_date_choice = int(self.eDateset.get())
        self.default_schedule_choice = self.default_schedule_selection.get()
        self.start_date_choice_2 = date.today() + timedelta(days=self.start_date_choice) #calculate iterated date
        self.start_date_choice_3 = self.start_date_choice_2.strftime('%Y %m %d')
        TrainModule.Train.trains_dates_ws.cell(row=TrainModule.Train.no_trains + 2, column=1).value = self.new_train
        TrainModule.Train.trains_dates_ws.cell(row=TrainModule.Train.no_trains + 2, column=2).value = self.start_date_choice_3
        TrainModule.Train.trains_dates_ws.cell(row=TrainModule.Train.no_trains + 2, column=3).value = self.project_choice
        TrainModule.Train.trains_dates_ws.cell(row=TrainModule.Train.no_trains + 2, column=4).value = self.default_schedule_choice
        TrainModule.Train.trains_dates_wb.save('C:\\Users\\Josh\\Desktop\\trains&dates.xlsx')
        self.fAddtrain.destroy()


# root is the main window
topLevel = Tk() #create top level widget object (window) of Tk class.

mainapp = Proj_select(topLevel) #create instance of class and pass Top widget as 1st parameter (master)

topLevel.mainloop()