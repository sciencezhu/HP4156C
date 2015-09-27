import PAplot
import os
import cleandata
#Plotter.plot_two(os.getcwd()+"\\10umgap0_10V.csv",skip=16,title="",xlabel="Gate Voltage (V)",ylabel="Current (A) x$10^{-8}$",data1="$I_G$",data2="$I_D$")
#Plotter.plot_from_file("pa/10umgap-10_10Vdiode.csv",title="",xlabel="Voltage (V)",ylabel="Current (I) x$10^{-12}$")

cleandata.clean_data()

filenames=os.listdir("data")
paths=[]

for name in filenames:
	paths.append("data/"+name)
#uncomment for fet measurements
#for path in paths:
#	PAplot.plot_two_yscales(path,skip=1,title="",show=False,log=True,
#		xlabel="Gate Voltage (VG)",y1label="ID (A)",y2label="IG (A)")
#uncomment for diode measurments
for path in paths:
    try:
        PAplot.plot_one(path,skip=1,title="",show=False,
            xlabel="Gate Voltage (VG)",ylabel="ID (A)")
    except Exception as e:
        print('could not make a plot for:\n ' +path)
        print(e)
