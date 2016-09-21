"""
Tkinter app for running the pa download, cleandata and PAplot scripts
from a simple GUI
"""

from Tkinter import Tk, Text, BOTH, W, N, E, S, RAISED, StringVar, Menu, Radiobutton, IntVar, OptionMenu
from ttk import Frame, Button, Label, Style, Entry
import tkFileDialog

import time

import modules.download_pa as download_pa




##HELPER FUNCTIONS##

def iterate(instring,iterstring,iterval,pad):
    """Iterates the iter sequence in the instring, padding to pad number of digits with zeros on the left"""
    try:
        int(iterval)
    except:
        print("iterval is not an integer string")
    return instring[:instring.find(iterstring)]+str(int(iterval)+1).zfill(pad)+instring[instring.find(iterstring)+len(iterstring):]

def insertstring(instring,placeholder,value,pad=0):
    # assert type(value)==int
    return instring[:instring.find(placeholder)]+str(value).zfill(pad)+instring[instring.find(placeholder)+len(placeholder):]

def timeStampYMDH():
    # -> 'YYYY_MM_DD_HHMM' as a time stamp
    return time.strftime('%Y_%m_%d_%H%M')

def make_fname_final(instring,chipval,deviceval):
    postchip=insertstring(instring,"[chip]",chipval,pad=3)
    postdev=insertstring(postchip,"[device]",deviceval,pad=2)
    posttime=insertstring(postdev,"[time]",timeStampYMDH(),pad=0)
    return posttime



# MAIN PAGE CLASS

class PAGUI(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Parameter Analyzer Control")
        self.style = Style()
        self.style.theme_use("clam")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        # self.rowconfigure(3, weight=1)
        # self.rowconfigure(5, pad=7)

        #set up instance variables
        self.directory = StringVar()
        self.fname = StringVar()
        self.fname_final=StringVar()
        self.device = StringVar()
        self.chip = StringVar()


        self.toplabel = Label(self, text="Dummy label at the top of the widget",justify="center")
        self.bottomlabel = Label(self, text="for help/info see github.com/leobrowning92/pa-control",justify="center",font="arial 11 italic")


        self.directory_btn = Button(self, text="Directory", command=self.askdirectory)

        self.filename_btn = Button(self, text="Filename", command=self.askfile)

        # self.exit_btn = Button(self, text="Exit", command=self.quit)
        # self.exit_btn.grid(row=5, column=0, padx=5)

        self.update_btn = Button(self, text="Update", command=self.runUpdate)

        self.iterdevice_btn = Button(self, text="Iterate [device]", command=self.newDevice)

        self.iterchip_btn = Button(self, text="Iterate [chip]", command=self.newChip)

        self.chip.set("001")
        self.chipnum_entry = Entry(self, textvariable=self.chip,width=5)

        self.device.set("01")
        self.devicenum_entry = Entry(self, textvariable=self.device,width=5)

        self.directory_entry = Entry(self, textvariable=self.directory)

        self.fname.set('Chip[chip]_device[device]_somenotes_[time].csv')
        self.fname_final.set(" => "+make_fname_final(self.fname.get(),
                            self.chip.get(),self.device.get()))

        self.fname_entry = Entry(self, textvariable=self.fname)

        self.fname_final_label = Label(self, textvariable=self.fname_final,
                          justify="center", font="arial 11 italic")


        # this button runs pulldata with parameter set by
        # self.datatype, which stores the value of self.radbtn
        self.pulldata_btn = Button(self, text="Pull Data", command=self.pulldata)


        #datatype=1 => diode, datatype=2 => FET
        self.datatype = IntVar()
        self.datatype1_radiobutton = Radiobutton(
            self, text='Diode (VF, IF)',
            variable=self.datatype, value=1)
        self.datatype2_radiobutton = Radiobutton(
            self, text='FET (VG, VDS, ID, IG)',
            variable=self.datatype, value=2)

        #grid alignments of all widgets
        self.toplabel.grid(column=0,columnspan=3, sticky=W, pady=4, padx=5)
        self.directory_btn.grid(row=1, column=0)
        self.filename_btn.grid(row=2, column=0)
        self.update_btn.grid(row=5, column=0, padx=5)
        self.iterdevice_btn.grid(row=4, column=0, sticky=N)
        self.iterchip_btn.grid(row=3, column=0, sticky=N)
        self.chipnum_entry.grid(row=3, column=1,
                         padx=5, sticky=W)
        self.devicenum_entry.grid(row=4, column=1,
                         padx=5, sticky=W)
        self.directory_entry.grid(row=1, column=1, columnspan=2,
                         padx=5, sticky=E + W)
        self.fname_entry.grid(row=2, column=1, columnspan=2,
                         padx=5, sticky=E + W)
        self.fname_final_label.grid(column=3, row=2, columnspan=1,
                       sticky=N + E + W, pady=4, padx=5)
        self.pulldata_btn.grid(row=5, column=3, padx=5,sticky=E)
        self.datatype1_radiobutton.grid(row=5,column=1,padx=5,sticky=N + E + S)
        self.datatype2_radiobutton.grid(row=5,column=2,padx=5,sticky=N + W + S)
        self.bottomlabel.grid(row=6,column=0,columnspan=3, sticky=W, pady=4, padx=5)

    def newChip(self):
        if self.fname.get() == '':
            self.askfile()
        else:
            try:
                self.chip.set(str((int(self.chip.get())+1)).zfill(2))
                self.device.set(str(1).zfill(2))
            except Exception as e:
                print(e)
            self.runUpdate()


    def newDevice(self):
        if self.fname.get() == '':
            self.askfile()
        else:
            try:
                self.device.set(str((int(self.device.get())+1)).zfill(2))
            except Exception as e:
                print(e)
            self.runUpdate()

    def runUpdate(self):
        self.fname_final.set(" => "+make_fname_final(self.fname.get(),
                            self.chip.get(),self.device.get()))

    def askdirectory(self):
        """Returns a selected directoryname."""
        self.entry1.delete(0, 'end')
        self.entry1.insert(0, tkFileDialog.askdirectory())

    def askfile(self):
        fullpath = tkFileDialog.askopenfilename()
        if "/" in fullpath:
            i = fullpath.rfind("/")
        if "\\" in fullpath:
            i = fullpath.rfind("\\")
        self.entry2.delete(0, 'end')
        self.entry2.insert(0, fullpath[i + 1:])

    def pulldata(self):
        if self.datatype.get() == 1:
            download_pa.download_data(path=self.entry1.get(
            ), filename=self.entry2.get(), values=['VF', 'IF'])
        elif self.datatype.get() == 2:
            download_pa.download_data(path=self.entry1.get(
            ), filename=self.entry2.get(), values=['VG', 'VDS', 'ID', 'IG'])


##MAIN INSTANCE OF PAGE##

def main():
    root = Tk()
    root.geometry("1000x200+300+300")
    app = PAGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
