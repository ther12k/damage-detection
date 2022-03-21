from src.utils import AdamAdam6050DInput
from adam_io import DigitalOutput
import time

adam = AdamAdam6050DInput()

#prev_inputs = list()
prev_A1, prev_A2 = int(), int()
prev_B1, prev_B2 = int(), int()
while True:
	adam_inputs = adam.di_inputs()
	A1, A2 = adam_inputs[0][1], adam_inputs[1][1]
	B1, B2 = adam_inputs[2][1], adam_inputs[3][1]
	
	if A1==0 and A2==1 and B1==1 and B2==1:
		adam.di_output(DigitalOutput(array=[0,1,0,0,0,0]))
	if A1==1 and A2==1 and B1==1 and B2==1:
		adam.di_output(DigitalOutput(array=[0,0,0,0,0,0]))
	#adam.di_output(
	#	[('DO0',1),('DO1',1),('DO2',1),('DO3',1),('DO4',1),('DO5',1)]
	#)
	prev_A1, prev_A2, prev_B1, prev_B2 = A1, A2, B1, B2
	if prev_A1==1 and prev_A2==1 and\
	   prev_B1==0 and prev_B2==0 and \
	   A1==1 and A2==1 and \
           B1==1 and B2==0:
		print('Camera Belakang')
	# Adam input
	#print(not prev_inputs == adam_inputs)
	#	prev_inputs = adam_inputs
	#	if not prev_inputs[4] and adam_inputs[4]:
	#		print('capture_camera')
	#print(adam_inputs[4])
	time.sleep(0.5)
