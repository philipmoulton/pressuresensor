"""CircuitPython Pressure Transducer Data Logger"""
# This is a mini version of `code.py`, in case there are issues with file size on the device
# Generated using: https://python-minifier.com/

import time as B,adafruit_sdcard as K,board as A,busio,digitalio as C,storage as G
from analogio import AnalogIn as L
try:
	M=L(A.A0)
	def N(pin):return pin.value*5./65536
	D=C.DigitalInOut(A.LED);D.direction=C.Direction.OUTPUT
	def O(s):D.value=True;B.sleep(s);D.value=False
	P=C.DigitalInOut(A.SD_CS);Q=busio.SPI(A.SD_CLK,A.SD_MOSI,A.SD_MISO);R=K.SDCard(Q,P);S=G.VfsFat(R);G.mount(S,'/sd');T=B.monotonic();H=T;E=0
	with open('/sd/volt_test.txt','a')as F:
		F.write('voltage,elapsed_time,count')
		while True:U=N(M);I=f"{U:.3f},{H:.3f},{E}";print(I);F.write(I);F.flush();E=E+1;O(.1);B.sleep(.9);H=B.monotonic()
except Exception as J:
	V=str(J)
	with open(f"/sd/err_{B.monotonic()}",'w')as W:W.write(V)
	raise J