from tkinter import *
import matplotlib.pyplot as plt
from numpy import *
import math as m
import os.path
import re


#Global variables



class Application(Frame):


	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.master = master
		delete_plots()


		
		
def plot3phase():
	nsamp_g=int(nsamp.get())
	dt_g=float(dt.get())*.001
	freq_g=float(freq.get())
	vpp_g=float(rms.get())*m.sqrt(2)
	offset_g=float(offset.get())
	
	#graph info
	graph_start=int(.001*float(startg.get())/(dt_g))
	graph_end=int(.001*float(endg.get())/(dt_g))
	
	L=float(Inductor.get())*10**-6
	C=float(Cap.get())*10**-6
	Lesr=.05
	Cesr=.1
	Cdamp=500.*10**-6
	Rdamp=.5

	Iload=1.
	
	################################################
	# create time base
	################################################

	n_range=arange(1,nsamp_g+1)

	t=[]
	for i in range(1,nsamp_g+1):
		t.append(n_range[i-1]*dt_g)

	################################################
	# create 3 phase sine wave
	################################################
	
	sin_a=[]
	for i in range(1,nsamp_g+1):
		sin_a.append(offset_g+vpp_g*m.sin(2.*m.pi*freq_g*t[i-1]))
	sin_b=[]
	for i in range(1,nsamp_g+1):
		sin_b.append(offset_g+vpp_g*m.sin(2.*m.pi*freq_g*t[i-1]+(2*m.pi/3)))
	sin_c=[]
	for i in range(1,nsamp_g+1):
		sin_c.append(offset_g+vpp_g*m.sin(2.*m.pi*freq_g*t[i-1]+(4*m.pi/3)))
		
	################################################
	# 3phase rectifier
	################################################	

	#Reference rectified voltage to 0vdc

	#plus rail
	rect_out_p=[]
	for i in range(1,nsamp_g+1):
		if sin_a[i-1] > sin_b[i-1] and sin_a[i-1] > sin_c[i-1]:
			rect_out_p.append(sin_a[i-1])
		elif sin_b[i-1] > sin_a[i-1] and sin_b[i-1] > sin_c[i-1]:
			rect_out_p.append(sin_b[i-1])
		elif sin_c[i-1] > sin_a[i-1] and sin_c[i-1] > sin_b[i-1]:
			rect_out_p.append(sin_c[i-1])
		else:
			rect_out_p.append(0)

	#Reference rectified voltage to 0vdc
	for i in range(1,nsamp_g+1):
		rect_out_p[i-1]=rect_out_p[i-1]+135.
	
	################################################
	# LC Filter
	################################################

	VL_drop=[0.]
	L_crnt=[0.]
	LVesr=[0.]

	C_crnt=[0.]
	VCesr=[0.]
	Vcap=[0.]
	Cv_tot=[0.]

	VR_dmp=[0.]
	Ir_dmp=[0.]
	VC_dmp=[0.]

	Iout=[0.]


	for i in range(1,nsamp_g):
		VL_drop.append(rect_out_p[i-1]-(Vcap[i-1]+LVesr[i-1]))
		L_crnt.append(L_crnt[i-1]+((VL_drop[i]+VL_drop[i-1])/2)*dt_g/L)
		LVesr.append(L_crnt[i]*Lesr)
		
		C_crnt.append(L_crnt[i]-(Ir_dmp[i-1]+Iout[i-1]))
		VCesr.append(C_crnt[i]*Cesr)
		Vcap.append(Vcap[i-1]+((C_crnt[i]+C_crnt[i-1])/2)*dt_g/C)
		Cv_tot.append(VCesr[i]+Vcap[i])
		
		VR_dmp.append(Cv_tot[i]-VC_dmp[i-1])
		Ir_dmp.append(VR_dmp[i]/Rdamp)
		VC_dmp.append(VC_dmp[i-1]+((Ir_dmp[i]+Ir_dmp[i-1])/2)*dt_g/Cdamp)
		
		Iout.append(Iload)
	
	################################################
	# Plot the graph
	################################################

	fig=plt.figure(num=None, figsize=(12,9), dpi=240,facecolor='w',edgecolor='k')
	ax1=fig.add_subplot(111)
	ax1.grid(True,which="both")
	ax1.set_ylabel('Voltage(volts)')
	ax1.set_xlabel('Time(s)')
	ax1.set_title('Rectified 3 Phase Sine Wave')
	ln1=ax1.plot(t[graph_start:graph_end],sin_a[graph_start:graph_end],color='r',label='Phase A')
	ln2=ax1.plot(t[graph_start:graph_end],sin_b[graph_start:graph_end],color='k',label='Phase B')
	ln3=ax1.plot(t[graph_start:graph_end],sin_c[graph_start:graph_end],color='b',label='Phase C')
	ax1.axhline(y=270,color='g')
	ln4=ax1.plot(t[graph_start:graph_end],Cv_tot[graph_start:graph_end],color='m',label='Rectified Voltage')
	ax1.set_ylim(-200,300)

	lns=ln1+ln2+ln3+ln4
	labs=[l.get_label() for l in lns]
	ax1.legend(lns,labs,loc=4)

	ax1.annotate("270VDC",xy=(.05,270),arrowprops=dict(arrowstyle='->'),xytext=(.06,200))
	
	num=find_num()
	file='phaseplot_%d.png' % num
	plt.savefig(file)
	
	os.startfile(file)
	#plt.show(block=True)

def delete_plots():
################
# delete all of the .png files in the current directory
################

	for f in os.listdir():
		if re.search('phaseplot',f):
			os.remove(os.path.join('',f))
			
			
def find_num():
################
# Find all of the .png files in the current directory
# Next, return a number +1 greater than the highest numbered .png file in the directory
################

	nums=[]
	for f in os.listdir():
		if re.search('.png',f):
			nums.append(f)
	vals=[]
	for i in nums:
		list=re.findall(r'\d+',i)
		for z in list:
			vals.append(int(z))
	if not vals:
		return 1
	else:
		return max(vals)+1
	
	
def timecalc():
################
# Calculate the time based on samples and time step input in the gui
################
	total = str(float(nsamp.get())*float(dt.get()))
	equation1.set(total)
	startg.set(0)
	endg.set(total)

def vpp_calc():
################
# Calculate the peak to peak voltage based on rms voltage input in the gui
################
	total_1 = str(float(rms.get())*m.sqrt(2))
	Vpp.set(total_1)
	

################
# Program begins here
################	
root = Tk()


#Set the size of the window
#root.geometry("400x300")
root.title('3 Phase Rectified LC Filter Plotter')

#create titles at the top of gui
title1 = Label(root, text='This gui will plot a 3 Phase bridge rectified output with LC filter')
title1.grid(row=0, columnspan=8)
title2 = Label(root, text='Input your parameters below. (Recomended min values: 20k samples at .0025ms, use a ratio of samples/time for 100ms total time.)')
title2.grid(row=1,columnspan=8)


#############
#Generate input fields for sample info
#and calculate the total sampled time
#############

nsamp=StringVar()
dt=StringVar()

#create label for nsamp entry
label1 = Label(root, text='Number of Samples:')
label1.grid(row=2, column=0)

#create entry box for nsamp
entry1 = Entry(root, bd=5, textvariable=nsamp)
entry1.insert(END,0)
nsamp.set(100000)
entry1.grid(row=2,column=1)

#create label for dt entry
label2 = Label(root, text='Time step dt (ms):')
label2.grid(row=3, column=0)

#create entry box for dt
entry2 = Entry(root, bd=5, textvariable=dt)
entry2.insert(END,0)
dt.set(.001)
entry2.grid(row=3,column=1)

#calculate the total time to be sampled
label3 = Label(root, text='Total Time (ms):')
label3.grid(row=4, column=0)

equation1 = StringVar()
equal1 = Button(root, text='Calculate', fg='red', bg='grey', command=timecalc, height=1, width=7)
equal1.grid(row=4, column=1)
#display total sampled time
tot_t = Entry(root, textvariable=equation1)
tot_t.grid(row=4, column=2)



#############
# AC Power Inputs
#############

freq=StringVar()
rms=StringVar()
offset=StringVar()

title3 = Label(root, text='Input the AC voltage info below:')
title3.grid(row=5)

#create label for frequency entry
label4 = Label(root, text='Input AC Voltage Frequency (Hz):')
label4.grid(row=6, column=0)

#create entry box for frequency
entry3 = Entry(root, bd=5, textvariable=freq)
entry3.insert(END,0)
freq.set(400)
entry3.grid(row=6,column=1)

#create label for rms voltage entry
label5 = Label(root, text='Input RMS Phase Voltage (Volts):')
label5.grid(row=7, column=0)

#create entry box for voltage
entry4 = Entry(root, bd=5, textvariable=rms)
entry4.insert(END,0)
rms.set(115)
entry4.grid(row=7,column=1)

#calculate the Vpp
label6 = Label(root, text='Peak to Peak (Vpp):')
label6.grid(row=7, column=2)

Vpp = StringVar()
equal2 = Button(root, text='Calculate', fg='red', bg='grey', command=vpp_calc, height=1, width=7)
equal2.grid(row=7, column=3)
#display total sampled time
vppcalc = Entry(root, textvariable=Vpp)
vppcalc.grid(row=7, column=4)



#create label for offset voltage entry
label7 = Label(root, text='Input Voltage Offset (Volts):')
label7.grid(row=8, column=0)

#create entry box for offset voltage
entry5 = Entry(root, bd=5, textvariable=offset)
entry5.insert(END,0)
offset.set(0)
entry5.grid(row=8,column=1)


#############
# LC Filter Inputs
#############

Inductor=StringVar()
Cap=StringVar()

title4 = Label(root, text='Input the LC Filter info below:')
title4.grid(row=9)
title5 = Label(root, text='(DCPS Values: 500uH, 750uF)')
title5.grid(row=10)

#create label for Inductor entry
label8 = Label(root, text='Input Inductance (uH):')
label8.grid(row=11, column=0)

#create entry box for Inductor
entry6 = Entry(root, bd=5, textvariable=Inductor)
entry6.insert(END,0)
Inductor.set(500)
entry6.grid(row=11,column=1)

#create label for Cap entry
label9 = Label(root, text='Input Capacitance (uF):')
label9.grid(row=12, column=0)

#create entry box for Cap
entry7 = Entry(root, bd=5, textvariable=Cap)
entry7.insert(END,0)
Cap.set(750)
entry7.grid(row=12,column=1)

#############
# Run Calculations and display graph
#############

title6 = Label(root, text='')
title6.grid(row=13)

label10 = Label(root, text='Run the calculations and display the graph:')
label10.grid(row=14, column=4)

equation2 = StringVar()
equal = Button(root, text='Graph It!!', fg='red', bg='grey', command=plot3phase, height=1, width=7)
equal.grid(row=14, column=5)

label11 = Label(root, text='graph start time (ms):')
label11.grid(row=14, column=0)
#create entry box for graph start
startg=StringVar()
entry7 = Entry(root, bd=5, textvariable=startg)
entry7.insert(END,0)
startg.set(0)
entry7.grid(row=14,column=1)

label12 = Label(root, text='graph end time (ms):')
label12.grid(row=14, column=2)
#create entry box for graph start
endg=StringVar()
entry7 = Entry(root, bd=5, textvariable=endg)
entry7.insert(END,0)
endg.set(100)
entry7.grid(row=14,column=3)


	
app = Application(root)




root.mainloop()