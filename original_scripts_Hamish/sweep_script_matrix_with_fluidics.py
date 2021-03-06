#!/var/run/python
# Agilent Parameter Analyser Sweep function script.
"""
Original script = python program_test6_TimeScanHannah.py
Created on Wed Oct 21 10:20:18 2013
@author b.hall + j.lovellsmith

This script = sweep_version2.py
Created Thu Dec 12 09:15:10 2013
@author h.colenso
"""
##----------------------
## DON'T MODIFY THIS
##----------------------
import os.path
import msvcrt
import sys
import time
import serial
import io
import visa

##----------------------
## MODIFY THESE SETTINGS
##----------------------

#Path to save files
ROOT = "C:/Users/Cleanroom.STAFF/Desktop/Leo/"
# File header information
SAMPLE = 'DEP 1' # Information about the sample used
CONDITIONS = 'Thick Au nw' # Information about production conditions
# Source Settings
# VAR1
sweep_mode = '1' # 1:Linear 2:Log10 3:Log25 4:Log50
sweep = 'double' # Single: sweep up or down depending on the sign of VDS_step  Double: sweep both up and down the sign of VDS_step just denotes which direction happens first.
VAR1_voltage = 'VDS' # VAR1 voltage label
VAR1_current = 'ID' # VAR1 current label
VAR1_start = '-40' # -100 to 100V for SMU; -200 to 200V for HPSMU; -20 to 20V for VSU
VAR1_stop = '40' # -100 to 100V for SMU; -200 to 200V for HPSMU; -20 to 20V for VSU
VAR1_step = '0.5' # 0 to 200V for SMU; 0 to 400V for HPSMU; 0 to 40V for VSU
VAR1_compliance = '1E-3' # -0.1 to 0.1A for SMU; -1 to 1A for HPSMU
# VAR2
VAR2_voltage = 'VG' # VAR2 voltage label
VAR2_current = 'IG' # VAR2 current label
VAR2_start = '0' # -100 to 100V for SMU; -200 to 200V for HPSMU
VAR2_step = '0' # -100 to 100V for SMU; -200 to 200V for HPSMU
VAR2_number_of_steps = '1' # 1 to 128
VAR2_compliance = '1E-3' # -0.1 to 0.1A for SMU; -1 to 1A for HPSMU 

# Time Settings
Cycles = 1 # number of cycles the script should run # REMEMBER IF VG_STEP IS SET TO INCREMENT THE NUMBER OF CYCLES VG COULD BECOME AN EXTREMELY HIGH VALUE
Time_between_cycles = 100
Integration_time = '2' # 1 = Short, 2 = Medium, 3 = Long
waitTime = '5'
intervalTime = '0'
numReadings = abs(float(VAR1_start) - float(VAR1_stop) / float(VAR1_step))
# Measurement Display - Graph scaling on the parameter analyser
x_axis_scale = '1' # 1:Linear 2:Logarithmic
x_axis_minimum = '-42' # numeric value
x_axis_maximum = '42' # numeric value
y_axis_VAR1_scale = '1' # 1:Linear 2:Logarithmic
y_axis_VAR1_minimum = '-1E-3' # numeric value
y_axis_VAR1_maximum = '1E-3' # numeric value
y_axis_VAR2_scale = '1' # 1:Linear 2:Logarithmic
y_axis_VAR2_minimum = '-2E-3' # numeric value
y_axis_VAR2_maximum = '2E-3' # numeric value

# Pressure Pump
pump_disabled = 0 # set to one to disable pressure pump operation
pressure = 200 # Pressure to set the pump in mbar
# time_period = 300 # Time in seconds to leave the pressure pump running for
wait_time = 10 # time to wait between status updates
COM = 2 # COM port (starts from 0, so subtract one from the COM number windows states, ie COM1 in windows is 0 here.)
##----------------------
## DON'T MODIFY THIS
##----------------------
matrix = []
for i in xrange(int(numReadings)):
    matrix.append
## Check to press ctrl+c to escape the script
def check_escape():
    return msvcrt.kbhit() and msvcrt.getch() == chr(27)

def Integration_text(x):
    return{'1':"Short",'2':"Medium",'3':"Long"}[x]
	
## Error codes from the parameter analyser
def print_error(sp):
	"error message"
	message = {
		0 : "data ready",
		1 : "syntax error",
		2 : "end status",
		3 : "illegal program",
		4 : "busy",
		5 : "self-test fail",
		6 : "service request",
		7 : "emergency"
	}
	for i in xrange(7):
		if sp & 2**i:
			print " %i: %s" %(i+1,message[i])
def timeStampYMDH():
    #-> 'YYYY_MM_DD_HHMM' as a time stamp
    return time.strftime('%Y_%m_%d_%H%M')

def timeStampYYMMDD():
    #-> 'YYMMDD' as a time stamp (JLS)
    return time.strftime('%Y%m%d')

def timeStampHHMMSS():
    #-> 'HH:MM:SS' as a time stamp
    return time.strftime('%H:%M:%S')

def timeStampDDMMYYYY():
	#-> 'DD.MM.YYYY' as a time stamp
	return time.strftime('%d.%m.%Y')
    
def xlTimeStamp():
    #-> 'HH:MM:SS DD/MM/YYYY' as a time stamp
    return time.strftime('%H:%M:%S %d/%m/%Y')

# Different loop modes
class ModeCycle(object):
    def __init__(self,interval):
        self.interval = interval
        
    def begin(self,*args):
        self.cycle_start = time.clock()
        # print "begin worked"
    
    @property
    def message(self):
        return ""
        
    def end(self,*args):
        elapsed = time.clock() - self.cycle_start
        remaining = self.interval - elapsed
        # print "end worked"
        if remaining < 0:
            print "interval exceeded by %G s" % abs(remaining)
        else:
            print "waiting %G s" % remaining
            time.sleep(remaining)
            
## File setup methods
def initialise_file(path,info):
    """

    """
    with open(path,'w') as f:
        f.writelines(info)
        f.write('\n')
        f.write('Directory,%s\n' % (str(ROOT)))
        f.write('Sample,%s\n' % (SAMPLE))
        f.write('Conditions,%s\n' % (CONDITIONS))
	f.write('Script Type,Sweep\n')
        f.write('Sweep Mode,%s\n' % (sweep_mode))
	f.write('Sweep direction,%s\n' % (sweep))
        f.write('Number of Cycles,%s\n' % (Cycles))
        f.write('%s Initial Value,%s\n' % (VAR1_voltage,VAR1_start))
        f.write('%s Increment Value,%s\n' %(VAR1_voltage,VAR1_step))
        f.write('%s Final Value,%s\n' % (VAR1_voltage,VAR1_stop))
        f.write('%s Compliance Value,%s\n' % (VAR1_current,VAR1_compliance))
        f.write('%s Value,%s\n' % (VAR2_voltage,VAR2_start))
        f.write('%s Increment Between Cycles,%s\n' %(VAR2_voltage,VAR2_step))
        f.write('%s Final Cycle Value,%s\n' % (VAR2_voltage,float(VAR2_start) + (float(VAR2_step)*float(VAR2_number_of_steps))))
        f.write('%s Compliance Value,%s\n' % (VAR2_current,VAR2_compliance))
	f.write('Wait Time,%s\n' % (waitTime))
	f.write('Interval Time,%s\n' % (intervalTime))
	f.write('Number of Readings,%s\n' % (numReadings))
	f.write('Integration Time,%s\n' % (Integration_text(Integration_time)))
	if pump_disabled == 0:
            f.write('Microfluidic Pump Pressure (mbar), %s\n' % (pressure))
        else:
            f.write('Microfluidic Pump Pressure (mbar), Pump Disabled\n')
        if x_axis_scale == str(1):
            f.write('X axis is Linear\n')
        else: 
            f.write('X axis is Logarithmic\n')
        f.write('X axis Minimum Value,%s\n' % (x_axis_minimum))
        f.write('X axis Maximum Value,%s\n' % (x_axis_maximum))
        if y_axis_VAR1_scale == str(1):
            f.write('Y axis VAR1 is Linear\n')
        else: 
            f.write('Y axis VAR1 is Logarithmic\n')
        f.write('Y axis VAR1 Minimum Value,%s\n' %(y_axis_VAR1_minimum))
        f.write('Y axis VAR1 Maximum Value,%s\n' % (y_axis_VAR1_maximum))
        if y_axis_VAR2_scale == str(1):
            f.write('Y axis VAR2 is Linear\n')
        else: 
            f.write('Y axis VAR2 is Logarithmic\n')
        f.write('Y axis VAR2 Minimum Value,%s\n' % (y_axis_VAR1_minimum))
        f.write('Y axis VAR2 Maximum Value,%s\n' % (y_axis_VAR1_maximum))
        f.write('\n')

def update_file(path,info,data):
    with open(path,'a') as f:
        f.write(info[0])
        f.write(', ')
        f.write(info[1])
        f.write(', ')
        f.write(info[2])
        f.write(', ')
        f.write(
            ", ".join("%.16G" % x_i for x_i in data)
        )
        f.write('\n')
## simplified script to control the Agilent Parameter Analyser
## this script just throws GPIB commands into the parameter analyser
## it could cause USB buffer overflow errors on the GPIB converter unit

## File setup methods matrix
def initialise_matrix_file(path,info):
    """

    """
    with open(path,'w') as f:
	f.write('Carbon Nanotube Semiconductor Analysis\n')
	f.write('Date of experiment:,%s\n' % (timeStampDDMMYYYY()))
	f.write('Time of experiment:,%s\n' % (timeStampHHMMSS()))
	f.write('\n')
	f.write('Sample:\n%s\n' % (SAMPLE))
	f.write('\n')
	f.write('Device being measured\n')
	f.write('FET\n')
	f.write('\n')
	f.write('%s\n' %(VAR1_voltage))
	f.write(' ,%s,to,%s,in,%s,step(s)\n' % (float(VAR1_start),float(VAR1_stop),float(VAR1_step)))
	f.write('%s\n' %(VAR2_voltage))
	f.write(' ,%s,to,%s,in,%s,step(s)\n' % (float(VAR2_start),(float(VAR2_start)+(float(VAR2_step)*float(VAR2_number_of_steps))),float(VAR2_step)))
	f.write('\n')
	
def update_matrix_file(path,info,data):
    with open(path,'a') as f:
        #f.write(info[0])
        #f.write(', ')
        #f.write(info[1])
        #f.write(', ')
        #f.write(info[2])
        #f.write(', ')
        #f.write(", ".join("%.16G" % x_i for x_i in data))
	f.write(", ".join("%s" % x_i for x_i in transpose_matrix[i]))
        f.write('\n')
        
## Initialise each file
string_YMDH=timeStampYMDH();
filename_VAR1 = "%s_%s_%s_%s.txt" % (SAMPLE,CONDITIONS,VAR1_current,string_YMDH)
filename_VAR2 = "%s_%s_%s_%s.txt" % (SAMPLE,CONDITIONS,VAR2_current,string_YMDH)
filename_matrix = "%s_%s_matrix_%s.txt" % (SAMPLE,CONDITIONS,string_YMDH)

path_VAR1 = os.path.join(ROOT,filename_VAR1)
path_VAR2 = os.path.join(ROOT,filename_VAR2)
path_matrix = os.path.join(ROOT,filename_matrix)
print path_VAR1
print path_VAR2
print path_matrix


info_string="%s:  %s: %s V to %s V %s: %s V to %s V \n" % (
    filename_VAR1,
    VAR2_voltage,
    VAR2_start,
    float(VAR2_start) + (float(VAR2_step)*float(VAR2_number_of_steps)),
    VAR1_voltage,
    VAR1_start, 
    VAR1_stop
)
string_xlTimeStamp=xlTimeStamp()
Header_string="Start time,%s, \n" % (string_xlTimeStamp)

initialise_file(
    path_VAR1,
    (info_string,Header_string)
)
initialise_file(
    path_VAR2,
    (info_string,Header_string)
)
initialise_matrix_file(
    path_matrix,
    (info_string,Header_string)
)    
  
#===================================================
# Pump Controller Setup!
if pump_disabled == 0:
    print "Pressure Pump Controller\n"
    try:
        ser = serial.Serial(COM,57600,timeout=2) # pump com port
    except:
        print "COM%s not found. Aborting communication with pressure pump!" % (COM+1)
        pump_disabled = 1
    if pump_disabled == 0:
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser)) # serial data reply wrapper
else:
    print "Pressure Pump Disabled\n"
LF = serial.to_bytes([10])
CR = serial.to_bytes([13])
CRLF = serial.to_bytes([13, 10])
start_char = 0
end_char = 0
# Status Interpreter
def status_decode(status_string,start,end):
	while status_string[end] != ",":
		end = end + 1
	code = status_string[start:end]	
	start = end + 1
	end = end + 2
	return [code,start,end]
	
def status():
	[error_code,start_char,end_char] = status_decode(status_string,2,3)
	[pump_state,start_char,end_char] = status_decode(status_string,start_char,end_char)
	[remote_state,start_char,end_char] = status_decode(status_string,start_char,end_char)
	[chamber_pressure,start_char,end_char] = status_decode(status_string,start_char,end_char)
	[supply_pressure,start_char,end_char] = status_decode(status_string,start_char,end_char)
	[target_pressure,start_char,end_char] = status_decode(status_string,start_char,end_char)
	print "Error Code: %s %s" % (error_code,Errors(error_code))
	print "Pump state: %s %s" % (pump_state,States(pump_state))
	print "Remote state: %s %s" % (remote_state,Remote(remote_state))
	print "Chamber Pressure: %s mbar" % chamber_pressure
	print "Supply Pressure: %s mbar" % supply_pressure
	print "Target Pressure: %s mbar" % target_pressure
	return[error_code,pump_state,remote_state,chamber_pressure,supply_pressure,target_pressure]
	
def Errors(x):
	return{
		'0': "no error",
		'1': "Supply pressure: too high",
		'2': "Tare: timeout",
		'3': "Tare: Supply still connected",
		'4': "Control: timeout",
		'5': "Target Pressure: too low",
		'6': "Target Pressure: too high",
		'7': "Leak test: Supply too low",
		'8': "Leak test: timeout",
		'100': "Fatal Error: Service needed on pressure pump"}[x]
		
def Remote(x):	
	return{
		'0': "Manual control mode",
		'1': "Remote control mode"}[x]
		
def States(x):
	return{
		'0': "Idle",
		'1': "Controlling",
		'2': "Tare",
		'3': "Error",
		'4': "Leak Test"}[x]

##-------------------------------------------

#===================================================
# Enter remote
if pump_disabled == 0:
    print "\n================================="

    #print "Serial Write A1"
    ser.write("A1"+CRLF)
    reply = sio.readline()
    #print reply
    if reply == "#A0%c"%LF:
            print "Entered Remote Mode"
            pump_disabled = 0
    else:
            print "Failed to Enter Remote Mode"
            pump_disabled = 1
            # May want to exit here? 
            # Disable pressure pump usage.
    #print "=================================\n"
# Clear status bit
if pump_disabled == 0:
    #print "\n================================="
    ser.write("C"+CRLF)
    #print "Clearing error conditions.\n"
    reply = sio.readline()
    if reply == "#C0%c"%LF:
            print "Status Cleared, Pump Idle"
    else:
            print "Failed to clear status"
    #print "=================================\n"
    #===================================================

    #===================================================  
    # Get pump information
    #print "\n================================="
    ser.write("v"+CRLF)
    version = sio.readline()
    print "Version: %s" % version[2:]
    ser.write("n"+CRLF)
    serial = sio.readline()
    print "Serial: %s" % serial[2:]
    #print "=================================\n"
    #=================================================== 

    #===================================================
    # Pump status
    #print "\n================================="
    ser.write("s"+CRLF)
    status_string = sio.readline()
    #print status_string[2:]
    status()			
    #print "=================================\n"
    #===================================================

    #===================================================
    # Set Pressure
    #print "\n================================="
    ser.write("P%d" % pressure +CRLF)
    reply = sio.readline()
    if reply == "#P0%c"%LF:
            print "Pressure Set OK\n"
    else:
            print "Failed to Set Pressure\n"
    # Check the status compare chamber pressure to target pressure
    # If the pressure has not reached target pressure within 60 seconds, vent the chamber and exit
    time.sleep(wait_time)
    ser.write("s"+CRLF)
    status_string = sio.readline()
    #print status_string[2:]
    status()
    print "=================================\n"
    #===================================================

## Open the GPIB bus
print "Initialising the Analyser"		
try:
    HP4145B = visa.instrument("GPIB::02") ## 4145 Code
    HP4145B.timeout = 60
    HP4145B.term_char = CR+LF
    HP4145B.delay = 1
    ## Clear the device errors
    HP4145B.clear()
    ## Check communications
    print "Parameter Analyser ID:"
    print HP4145B.ask("ID") ## 4145 Code
    # HP4155B.write("*IDN?") ## 4155 Code
except:
    print "Could not connect to the Parameter Analyser!"
    sys.exit()

## Setup Program parameters
program_parameters = "IT%s CA1 DR1 BC" % (Integration_time)
print program_parameters
HP4145B.write(program_parameters)
## Setup Channel Definitions for sweep
channel_definitions = "DE CH1,'VS','IS',3,3;CH2,'%s','%s',1,1;CH3,'%s','%s',1,2;CH4;" % (VAR1_voltage,VAR1_current,VAR2_voltage,VAR2_current)
## Channel 1
## Channel 2
## Channel 3
## Channel 4
print channel_definitions
HP4145B.write(channel_definitions)
## Setup Measurement display
measurement_display = "SM DM1 XN '%s',%s,%s,%s; YA '%s',%s,%s,%s; YB '%s',%s,%s,%s" % (VAR1_voltage,x_axis_scale,x_axis_minimum,x_axis_maximum,VAR1_current,y_axis_VAR1_scale,y_axis_VAR1_minimum,y_axis_VAR1_maximum,VAR2_current,y_axis_VAR2_scale,y_axis_VAR2_minimum,y_axis_VAR2_maximum)
# this needs to be modified to include variable VAR1 and VAR2 names.
print measurement_display
HP4145B.write(measurement_display)

## Check error flag
sp = HP4145B.stb
if sp != 0:
	print "Instrument state problem, spoll = %s" % hex(sp)
	print_error(sp)
	sys.exit()
# record start time	
start_time = time.clock()
# Data Acquisition loop
Mode = ModeCycle(Time_between_cycles)
for i in xrange(Cycles):
    print "cycle: %i of %i" % (i,Cycles)
    
    Mode.begin()
    ## Setup VAR1 Source
    var1_setup = "SS VR %s,%s,%s,%s,%s" % (sweep_mode,VAR1_start,VAR1_stop,VAR1_step,VAR1_compliance)
    print var1_setup
    HP4145B.write(var1_setup)
    ## Setup VAR2 Source
    var2_setup = "SS VP %s,%s,%s,%s" % (VAR2_start,VAR2_step,VAR2_number_of_steps,VAR2_compliance)
    print var2_setup
    HP4145B.write(var2_setup)
    HP4145B.write("BC")
    time_since_start = str(time.clock() - start_time)
    T_start_sweep = time.clock()
    # Start Measurement
    HP4145B.write("MD ME1")
    ## HP4145B.wait_for_ready()
    while not HP4145B.stb & 1:
        if pump_disabled == 0:
            ser.write("s"+CRLF)
            status_string = sio.readline()
            status()
        else:
            sys.stdout.write('.') # Update the screen to inform user of progress
        time.sleep(HP4145B.delay)
    print
    # Get Measured values
    ## VAR1_down=HP4145B.ask_for_values("DO '%s'" % VAR1_current)
    ## VAR2_down=HP4145B.ask_for_values("DO '%s'" % VAR2_current)
    try:
        visa.instrument("GPIB::02").write("DO '%s'"%VAR1_current)
    except:
        print("Timeout processing DO '%s'"%VAR2_current)
    VAR1_down = visa.instrument("GPIB::02").read_values()
    try:
        visa.instrument("GPIB::02").write("DO '%s'"%VAR2_current)
    except:
        print("Timeout processing DO '%s'"%VAR2_current)
    VAR2_down = visa.instrument("GPIB::02").read_values()
    
    # Do we want to loop up and down?
    if sweep == 'double':
    	# Reverse sweep direction
	var1_setup = "SS VR %s,%s,%s,%s,%s" % (sweep_mode,VAR1_stop,VAR1_start,'-'+VAR1_step,VAR1_compliance)
        print var1_setup
	HP4145B.write(var1_setup)
	# Start Measurement
	HP4145B.write("MD ME1")
	## HP4145B.wait_for_ready()
	while not HP4145B.stb & 1:
            if pump_disabled == 0:
                ser.write("s"+CRLF)
                status_string = sio.readline()
                status()
            else:
                sys.stdout.write('.') # Update the screen to inform user of progress
            time.sleep(HP4145B.delay)
        print
	# Get Measured values
	##VAR1_ask = "DO '%s'" % (VAR1_current)
	##VAR2_ask = "DO '%s'" % (VAR2_current)
	##VAR1_total = VAR1_down + HP4145B.ask_for_values(VAR1_ask)
	##VAR2_total = VAR2_down + HP4145B.ask_for_values(VAR2_ask)
	try:
            visa.instrument("GPIB::02").write("DO '%s'"%VAR1_current)
        except:
            print("Timeout processing DO '%s'"%VAR2_current)
        VAR1_total = VAR1_down + visa.instrument("GPIB::02").read_values()
        try:
            visa.instrument("GPIB::02").write("DO '%s'"%VAR2_current)
        except:
            print("Timeout processing DO '%s'"%VAR2_current)
        VAR2_total = VAR2_down + visa.instrument("GPIB::02").read_values()
 
    else:
	VAR1_total = VAR1_down
	VAR2_total = VAR2_down
    T_stop_sweep = time.clock()
    time_for_sweep = str(T_stop_sweep - T_start_sweep)
    print 'sweep time', time_for_sweep
    ## Print Values
    ## print VAR1_down
    ## print VAR2_down
    ## Save values to disk
    msg = Mode.message
    update_file(path_VAR1,(time_since_start,time_for_sweep,"%s %s" % (VAR1_current,msg)),VAR1_total)
    update_file(path_VAR2,(time_since_start,time_for_sweep,"%s %s" % (VAR2_current,msg)),VAR2_total)
    VAR1_total.insert(0,VAR1_current)
    VAR2_total.insert(0,VAR2_current)
    # X axis title, insert X axis period and label
    X_axis = [VAR1_voltage,VAR1_start]
    X_values = abs((float(VAR1_start) - float(VAR1_stop)) / float(VAR1_step))+1
    for j in range(0,int(X_values)):
        X_axis.append(float(VAR1_start) + (j * float(VAR1_step)))
    if sweep == 'double':
        for j in range(1,int(X_values)):
            X_axis.append(float(VAR1_stop) - (j * float(VAR1_step)))
    matrix.append(X_axis)
    matrix.append(VAR1_total)
    matrix.append(VAR2_total)
    transpose_matrix = zip(*matrix)
    ## print transpose_matrix
    if i == Cycles - 1:
        for i in range(0,len(transpose_matrix)):
            update_matrix_file(path_matrix,(time_since_start,time_for_sweep,"%s" % msg),transpose_matrix[i])
    # Exit nicely
    if check_escape(): sys.exit()

    Mode.end()
if pump_disabled == 0:
    #===================================================
    # Vent Chamber
    #print "\n================================="
    ser.write("P0"+CRLF)
    pressure = sio.readline()
    if pressure == "#P0%c"%LF:
            print "Pressure set to zero, venting\n"
    else:
            print "Unable to vent, chamber still pressurised!\n"
    #time.sleep(wait_time)
    ser.write("s"+CRLF)
    status_string = sio.readline()
    #print status_string[2:]
    status()
    #print "=================================\n"
    #===================================================

    #===================================================
    # Exit remote
    #print "\n================================="
    print "Exit Remote Mode: "
    ser.write("A0"+CRLF)
    reply = sio.readline()
    if reply == "#A0%c"%LF:
            print "Success"
    else:
            print "Failure"
    #print "=================================\n"
    #===================================================

    #===================================================
    # Clear up
    #print "\n================================="
    print "Clear status bits"
    ser.write("C"+CRLF)
    #print "=================================\n"
    #===================================================
