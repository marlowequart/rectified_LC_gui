import matplotlib.pyplot as plt
from numpy import *
import math as m


print ('This file will plot a 3 Phase bridge rectified output with LC filter')
print ('\n')
################################################
# Sampling Inputs
################################################

################
#turn on this section for user inputs
################
print ('Input your sampling info')
print ('(Recomended min values: 20k samples at .0025ms)')
print ('(Recomended ratio samples/time for 100ms total time)')
nsamp1 = input('Number of samples = ')
dt1 = input('Time step (ms) = ')

nsamp = int(nsamp1)
dt = float(dt1)*.001
tot_t=dt*float(nsamp1)



###############
#use this section for testing
###############
# nsamp=10000
# dt=.005*.001


################################################
# AC Power Inputs
################################################

################
#turn on this section for user inputs
################

print ('\n')
print ('Input your AC power info')
freq1 = input('AC Frequency = ')
rms1 = input('RMS Voltage = ')
offset1 = input('Voltage Offset = ')

freq = float(freq1)
vpp = float(rms1)*math.sqrt(2.)
offset = float(offset1)

print('vpp= %d ' % vpp)

###############
#use this section for testing
###############

# freq=400
# vpp=115.*m.sqrt(2)
# offset=0

################################################
# Filter Value Inputs
################################################

################
#turn on this section for user inputs
################
print ('\n')
print ('Input your filter values (in microhenry/microfarads)')
print ('(DCPS Values: 500uH, 750uF)')
L1 = input('L = ')
C1 = input('C = ')

L2 = float(L1)
C2 = float(C1)

L=L2*10**-6
C=C2*10**-6
Lesr=.05
Cesr=.1
Cdamp=500.*10**-6
Rdamp=.5

Iload=1.

###############
#use this section for testing
###############

# L=500.*10**-6
# Lesr=.05
# C=750.*10**-6
# Cesr=.1

# ##Damper Parameters
# Cdamp=500.*10**-6
# Rdamp=.5

# Iload=1.


################################################
# create time base
################################################

n_range=arange(1,nsamp+1)

t=[]
for i in range(1,nsamp+1):
    t.append(n_range[i-1]*dt)
	
################################################
# create 3 phase sine wave
################################################	

sin_a=[]
for i in range(1,nsamp+1):
    sin_a.append(offset+vpp*m.sin(2.*m.pi*freq*t[i-1]))
sin_b=[]
for i in range(1,nsamp+1):
    sin_b.append(offset+vpp*m.sin(2.*m.pi*freq*t[i-1]+(2*m.pi/3)))
sin_c=[]
for i in range(1,nsamp+1):
    sin_c.append(offset+vpp*m.sin(2.*m.pi*freq*t[i-1]+(4*m.pi/3)))


################################################
# 3phase rectifier
################################################	

#Reference rectified voltage to 0vdc

#plus rail
rect_out_p=[]
for i in range(1,nsamp+1):
	if sin_a[i-1] > sin_b[i-1] and sin_a[i-1] > sin_c[i-1]:
		rect_out_p.append(sin_a[i-1])
	elif sin_b[i-1] > sin_a[i-1] and sin_b[i-1] > sin_c[i-1]:
		rect_out_p.append(sin_b[i-1])
	elif sin_c[i-1] > sin_a[i-1] and sin_c[i-1] > sin_b[i-1]:
		rect_out_p.append(sin_c[i-1])
	else:
		rect_out_p.append(0)
	
#minus rail
# rect_out_m=[]
# for i in range(1,nsamp+1):
	# if sin_a[i-1] < sin_b[i-1] and sin_a[i-1] < sin_c[i-1]:
		# rect_out_m.append(sin_a[i-1])
	# elif sin_b[i-1] < sin_a[i-1] and sin_b[i-1] < sin_c[i-1]:
		# rect_out_m.append(sin_b[i-1])
	# elif sin_c[i-1] < sin_a[i-1] and sin_c[i-1] < sin_b[i-1]:
		# rect_out_m.append(sin_c[i-1])
	# else:
		# rect_out_m.append(0)
		
#Reference rectified voltage to 0vdc
for i in range(1,nsamp+1):
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


for i in range(1,nsamp):
	VL_drop.append(rect_out_p[i-1]-(Vcap[i-1]+LVesr[i-1]))
	L_crnt.append(L_crnt[i-1]+((VL_drop[i]+VL_drop[i-1])/2)*dt/L)
	LVesr.append(L_crnt[i]*Lesr)
	
	C_crnt.append(L_crnt[i]-(Ir_dmp[i-1]+Iout[i-1]))
	VCesr.append(C_crnt[i]*Cesr)
	Vcap.append(Vcap[i-1]+((C_crnt[i]+C_crnt[i-1])/2)*dt/C)
	Cv_tot.append(VCesr[i]+Vcap[i])
	
	VR_dmp.append(Cv_tot[i]-VC_dmp[i-1])
	Ir_dmp.append(VR_dmp[i]/Rdamp)
	VC_dmp.append(VC_dmp[i-1]+((Ir_dmp[i]+Ir_dmp[i-1])/2)*dt/Cdamp)
	
	Iout.append(Iload)

	
	
# fig=plt.figure(1)
# ax1=fig.add_subplot(111)
# ax1.grid(True,which="both")
# ax1.set_ylabel('Voltage(volts)')
# ax1.set_xlabel('Time(s)')
# ax1.set_title('Sine Wave')
# ax1.plot(t,sin_a,color='r')
# ax1.plot(t,sin_b,color='k')
# ax1.plot(t,sin_c,color='b')


# plt.show()

fig=plt.figure(2)
ax1=fig.add_subplot(111)
ax1.grid(True,which="both")
ax1.set_ylabel('Voltage(volts)')
ax1.set_xlabel('Time(s)')
ax1.set_title('Rectified 3 Phase Sine Wave')
#ax1.plot(t[2500:],rect_out_p[2500:],color='k')
ln1=ax1.plot(t[10000:],sin_a[10000:],color='r',label='Phase A')
ln2=ax1.plot(t[10000:],sin_b[10000:],color='k',label='Phase B')
ln3=ax1.plot(t[10000:],sin_c[10000:],color='b',label='Phase C')
ax1.axhline(y=270,color='g')
ln4=ax1.plot(t[10000:],Cv_tot[10000:],color='m',label='Rectified Voltage')
ax1.set_ylim(-200,300)

lns=ln1+ln2+ln3+ln4
labs=[l.get_label() for l in lns]
ax1.legend(lns,labs,loc=4)

# Locations:
# 'best'         : 0, (only implemented for axis legends)
# 'upper right'  : 1,
# 'upper left'   : 2,
# 'lower left'   : 3,
# 'lower right'  : 4,
# 'right'        : 5,
# 'center left'  : 6,
# 'center right' : 7,
# 'lower center' : 8,
# 'upper center' : 9,
# 'center'       : 10,

ax1.annotate("270VDC",xy=(.05,270),arrowprops=dict(arrowstyle='->'),xytext=(.06,200))

plt.show()

