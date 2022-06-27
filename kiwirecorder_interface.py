# Built by Pezzler.
# Operates as a basic interface to kiwirecorder.py.
# Needs to exist in the same folder as kiwirecorder.py.

import sys
if(sys.version_info[0] == 3):
    import tkinter as tk
else:
    import Tkinter as tk
import subprocess
import psutil
from multiprocessing import Process

# kill process recursively
def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

# a multiprocess function to contain and not block the main thread
def threadRecord(cmd):
    subprocess.run(cmd , shell=True)#stdout=subprocess.PIPE, shell=True

# main implemented UI class
class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        parent.geometry("500x260")
        
        self.greeting = tk.Label(text="Welcome to the kiwiclient Interface")
        self.greeting.pack()
        
        self.server = tk.Label(self.parent, text="Address:")
        self.server.place(x=0, y=25)
        self.port = tk.Label(self.parent, text="Port:")
        self.port.place(x=0, y=50)
        self.freq = tk.Label(self.parent, text="Freq:")
        self.freq.place(x=0, y=75)
        self.lowCut = tk.Label(self.parent, text="Lowcut:")
        self.lowCut.place(x=0, y=100)
        self.highCut = tk.Label(self.parent, text="Highcut:")
        self.highCut.place(x=125, y=100)

        self.modulation = tk.Label(self.parent, text="Modulation (optional)")
        self.modulation.place(x=0, y=130)
        
        self.userID = tk.Label(self.parent, text="Username (optional)")
        self.userID.place(x=0, y=160)
        self.password = tk.Label(self.parent, text="Password (optional)")
        self.password.place(x=0, y=185)
        
        self.serverEntry = tk.Entry(self.parent, width= 40)
        self.serverEntry.place(x=50, y=25)
        self.portEntry = tk.Entry(self.parent, width= 40)
        self.portEntry.place(x=50, y=50)
        self.portEntry.insert(0,"8073")
        self.freqEntry = tk.Entry(self.parent, width= 40)
        self.freqEntry.place(x=50, y=75)
        self.lowEntry = tk.Entry(self.parent, width= 10)
        self.lowEntry.place(x=50, y=100)
        self.lowEntry.insert(0,"50")
        self.highEntry = tk.Entry(self.parent, width=10)
        self.highEntry.place(x=180, y=100)
        self.highEntry.insert(0,"3500")

        modulation = [ "Default", "am", "lsb", "usb", "cw", "nbfm", "iq"]
        
        self.modulationChoice = tk.StringVar()
        self.modulationChoice.set(modulation[0])
        self.modulationOptions = tk.OptionMenu(self.parent, self.modulationChoice, *modulation)
        self.modulationOptions.place(x=125,y=125)
        
        self.userIDEntry = tk.Entry(self.parent, width=20)
        self.userIDEntry.place(x=125, y=160)
        self.passEntry = tk.Entry(self.parent, show="*", width=20)
        self.passEntry.place(x=125,y=185)

        
        self.recordB = tk.Button(self.parent, text="Start Recording", width=25, height=2,command = self.startRecording)
        self.stopB = tk.Button(self.parent, text="Stop Recording", width=25, height=2, command = self.stopRecording)
        self.recordB.place(x=25, y=210)
        self.stopB.place(x=225, y=210)
        
        # enable/disable buttons
        self.recordB['state'] = tk.NORMAL
        self.stopB['state'] = tk.DISABLED

    def startRecording(self):
    
        # enable/disable buttons
        self.recordB['state'] = tk.DISABLED
        self.stopB['state'] = tk.NORMAL
        
        # get values for subprocess
        lowcut = self.lowEntry.get()
        highcut = self.highEntry.get()
        userID = self.userIDEntry.get()
        freq = self.freqEntry.get()
        port = self.portEntry.get()
        server = self.serverEntry.get()
        password = self.passEntry.get()
        modulation = self.modulationChoice.get()
        
        cmd = "python kiwirecorder.py " + "-f " + freq + " -s " + server + " -p " + port + " --lp-cutoff " + lowcut + " --hp-cutoff " + highcut
        if len(userID) > 0:
            cmd +=" -u " + userID
        if len(password) > 0:
            cmd +=" --pw " + password
        if(modulation != "Default"):
            cmd +=" -m " + modulation
        
        print(cmd)
        
        #self.lock = thread.allocate_lock()
        #with self.lock:
        self.currentP = Process(target=threadRecord, args=(cmd,))
        self.currentP.start()
            
    
    
    # stops recording multiprocess and kills it
    def stopRecording(self):
    
        # enable/disable buttons
        self.recordB['state'] = tk.NORMAL
        self.stopB['state'] = tk.DISABLED
        
        # kill the process
        kill(self.currentP.pid)


# main execution loop
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Kiwiclient Interface')
    MainApplication(root)
    root.mainloop()
