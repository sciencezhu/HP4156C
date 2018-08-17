import visa,time, sys, io, os
from hp4156b import hp4156c
import parameter_analyser_hp4156b as pa


def main():
    address = 'GPIB0::17::INSTR'
#    rm = visa.ResourceManager("C:/Windows/SysWOW64/visa32.dll")
#    pa = rm.open_resource(address)
#    pa.read_termination = '\n'
#    pa.write_termination = '\n'
#    pa.timeout = 8000
#    pa.write("*rst")
#    print(pa.query('*IDN?'))
#######################################
#### Transfer Curve Measurement
#######################################    
    
#    abc = pa.initialize_device()
#    define_transfer_smu(abc)    
#    measure_transfer(abc, "test.csv", savedir="", vg_start=-15, vg_stop=2, vg_step=0.2, vds_start=0.5, vds_step=9.5, vds_num=2)
#    
    
#######################################
###### I-V family or output curve Measurement
#######################################    

#    abc = pa.initialize_device()
#    define_output_smu(abc)
#    measure_output(abc, "I-V_Family.csv", savedir="", vds_start=0, vds_stop=10, vds_step=0.5, vg_start=-4, vg_step=1, vg_num=3)
#    

#########################################
####  IGSS Measurement
#########################################





def diodesweep():
    # Initialise the device
    device = hp4156c()
    device.get_error()
    device.reset()
    device.get_error()
    ## Setup the device for a Diode Measurement
    device.measurementMode("SWEEP","MEDIUM")
    device.get_error()
    device.smu("SMU1",["VF","VAR1","IF","V"])
    device.get_error()
    device.smu("SMU3",["V","CONS","I","COMM"])
    device.get_error()
    device.disableSmu(["SMU2","SMU4"])
    device.get_error()
    device.var("VAR1",["LIN","DOUB","-1","0.1","1.0","100e-3"])
    device.get_error()
    device.visualise(["Voltage","1","-1","1"], ["Current","1","-0.1","0.1"])
    device.get_error()
    device.single()
    device.get_error()
    dataReturned = device.daq(["VF","IF"])
    device.get_error()
    print(device.data)
    device.get_error()
    #for saving
    #device.save_data(fname='test.csv')



def measure_output(device, fname, savedir, vds_start, vds_stop, vds_step, vg_start, vg_step, vg_num):
#    device.var("VAR1",["LIN","DOUB",str(vds_start),str(vds_step),str(vds_stop),"1e-3"])
    device.var("VAR1",["LIN","SING",str(vds_start),str(vds_step),str(vds_stop),"1e-3"])
    device.get_error()
    device.var("VAR2",["LIN","SING",str(vg_start),str(vg_step),str(vg_num),"1e-3"])
    device.get_error()
    device.visualiseTwoYs(["VDS","LIN",str(vds_start),str(vds_stop)], ["ID","LIN","-1e-6","1e-6"], ["IG","LIN","-1e-8","1e-8"])
    device.get_error()
    print("=>Sweep Parameters set")
    device.single()
    device.get_error()
    if "[INFO]"in fname:
        if vds_step==0:
            fname = fname.replace("[INFO]", "outputVDS" + str(abs(vds_start)) + "VG" + str(abs(vg_start)))
        else:
            fname = fname.replace("[INFO]", "outputVDS" + str(abs(vds_start)) + "VG" + str(abs(vg_start)) + "+" + str(vg_num) + "x" + str(abs(vg_step)))
    device.collect_data(['VG', 'VDS', 'ID', 'IG'],fname,savedir)
    device.get_error()
    print("=>Data Finished Collecting")



def define_output_smu(device):
    device.measurementMode("SWEEP","MEDIUM")
    device.get_error()
    device.smu("SMU2",["VS","CONS","IS","COMM"])
    device.get_error()
    device.smu("SMU4",["VDS","VAR1","ID","V"])
    device.get_error()
    device.smu("SMU1",["VG","VAR2","IG","V"])
    device.get_error()
    device.smu("SMU3",["VGND","CONS","IGND","COMM"])
    device.get_error()
    print("=>SMU's assigned")
    

def measure_transfer(device, fname, savedir, vg_start, vg_stop, vg_step, vds_start, vds_step, vds_num):
    device.var("VAR1",["LIN","DOUB",str(vg_start),str(vg_step),str(vg_stop),"1e-3"])
    device.get_error()
    #note, VAR2 is always linear
    device.var("VAR2",["LIN","SING",str(vds_start),str(vds_step),str(vds_num),"1e-3"])
    device.get_error()
    device.visualiseTwoYs(["VG","LIN",str(vg_start),str(vg_stop)], ["ID","LOG","1e-11","1e-6"], ["IG","LIN","-1e-8","1e-8"])
    device.get_error()
    print("=>Sweep Parameters set")
    device.single()
    device.get_error()
    if "[INFO]"in fname:
        if vds_step==0:
            fname = fname.replace("[INFO]", "transferVG" + str(abs(vg_start)) + "VDS" + str(abs(vds_start)))
        else:
            fname = fname.replace("[INFO]", "transferVG" + str(abs(vg_start)) + "VDS" + str(abs(vds_start)) + "+" + str(vds_num) + "x" + str(abs(vds_step)))
    device.collect_data(['VG', 'VDS', 'ID', 'IG'],fname,savedir)
    device.get_error()
    print("=>Data Finished Collecting")

def define_transfer_smu(device):
    device.measurementMode("SWEEP","MEDIUM")
    device.get_error()
    device.smu("SMU2",["VS","CONS","IS","COMM"])
    device.get_error()
    device.smu("SMU4",["VDS","VAR2","ID","V"])
    device.get_error()
    device.smu("SMU1",["VG","VAR1","IG","V"])
    device.get_error()
    device.smu("SMU3",["VGND","CONS","IGND","COMM"])
    device.get_error()
    print("=>SMU's assigned")



def initialize_device():
    """Initialise the device and resets. returns the resetted device"""
    device = hp4156c()
    device.get_error()
    device.reset()
    device.get_error()
    print("=>Device Initialized")
    return device



if __name__ == '__main__':
	main()




#rm = visa.ResourceManager("C:/Windows/SysWOW64/visa32.dll")
#
#inst = rm.open_resource('GPIB0::17::INSTR')
#
#_devices = rm.list_resources()
#print(_devices)
#
#inst.write("*rst")
#print(inst.query('*IDN?'))
#inst.timeout = 8000
#
#inst.read_termination = '\n'
#inst.write_termination = '\n'
#
#
#
#################IDSS Function
### Set source (SMU1) to ground
#print (inst.write(":PAGE:CHAN:SMU1:COMM"))
#time.sleep(1)
#
### Set gate (SMU2) to var1
#print (inst.write(":PAGE:CHAN:SMU2:VNAME 'Vg' "))
#print (inst.write(":PAGE:CHAN:SMU2:INAME 'Ig' "))
#print (inst.write(":PAGE:CHAN:SMU2:MODE V"))
#print (inst.write(":PAGE:CHAN:SMU2:FUNC CONS"))
#time.sleep(1)
#
### Set drain (SMU3) to var1
#print (inst.write(":PAGE:CHAN:SMU3:dis"))
##print (inst.write(":PAGE:CHAN:SMU3:VAR1"))
#time.sleep(1)
#
### Set (SMU4) to disabled
#print (inst.write(":PAGE:CHAN:SMU4:DIS"))
#time.sleep(1)




#
#print(inst.write('US'))
#
#time.sleep(3)
#
#print(inst.write('FMT 1,1'))
#
#time.sleep(3)
#
## Set short integration time
#print(inst.write('SLI 1'))
#
#time.sleep(3)
## Enable SMU 3
#print(inst.write('CN 3'))
#
#time.sleep(3)
## Set measurement mode to sweep (2) on SMU 3
#print(inst.write('MM 2,3'))
#
#time.sleep(3)
## Setup voltage sweep on SMU 3
##print(inst.write('WV 3,3,0,0.01,0.1,0.01'))
#print(inst.write('WV 3,3,0,-0.1,0.1,0.01,0.01,0.001,1'))
#
#time.sleep(3)
## Execute
#print(inst.write('XE'))
#
#time.sleep(10)
#
## Query output buffer
#print("********** Querying RMD **********")
#print(inst.write('RMD? 0'))
#
##time.sleep(2)
#
##print(inst.query('*IDN?'))
#
#
#print ("Reached here")
#
#time.sleep(10)
#
#print(inst.read(count=200))
#
#print ("Reached here _2 ")
#
#time.sleep(10)
#
#print("********** Querying STB **********")
#print(inst.query('*STB?'))
