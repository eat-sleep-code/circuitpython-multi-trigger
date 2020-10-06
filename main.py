from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
import board
import busio
import time


# === Board Inputs (and Threshold Voltages) ====================================

pinCount = 4

pin1 = AnalogIn(board.D1)
pin1Threshold = 1.6

pin2 = AnalogIn(board.D2)
pin2Threshold = 2.3

pin3 = AnalogIn(board.D3)
pin3Threshold = 1.6

pin4 = AnalogIn(board.D4)
pin4Threshold = 1.6


# === Board Outputs ============================================================

output = DigitalInOut(board.D0)
output.direction = Direction.OUTPUT


# === On-board LEDs ============================================================

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT
dotstar = busio.SPI(board.APA102_SCK, board.APA102_MOSI)


# === Functions ================================================================

def getVoltage(pin):
	voltage = (pin.value * 3.3) / 65536
	return voltage

def getPin(pin):
	if pin == 1:
		return pin1Threshold, getVoltage(pin1)
	elif pin == 2:
		return pin2Threshold, getVoltage(pin2)
	elif pin == 3:
		return pin3Threshold, getVoltage(pin3)
	elif pin == 4:
		return pin4Threshold, getVoltage(pin4)

def setPixel(red, green, blue):
	if not dotstar.try_lock():
		return
	#print('Setting dotstar to: %d %d %d' % (red, green, blue))
	data = bytearray([0x00, 0x00, 0x00, 0x00, 0xff, blue, green, red, 0xff, 0xff, 0xff, 0xff])
	dotstar.write(data)
	dotstar.unlock()

def scanInputs():
	pinNumber = 1
	allOff = True
	led.value = False 
	setPixel(255, 0, 0)
	while pinNumber <= pinCount:
		print('\n--- Pin ' + str(pinNumber) + ' ----------------')
		try:
			threshold, voltage = getPin(pinNumber)
			print('Threshold: ', threshold)
			print('Voltage: ', voltage)
			if voltage >= threshold:
				output.value = False
				led.value = True
				setPixel(14, 180, 14)
				allOff = False
				print('Pin ' + str(pinNumber) + ' has detected movement...')
				time.sleep(5)
			else: 
				output.value = True 
				if allOff == True:
					led.value = False 
					setPixel(255, 0, 0)
					print('All is quiet around these parts...')  	
				else:
					print('Something is going on elsewhere...')
		except Exception as ex:
			print(ex)
			pass
		pinNumber += 1

	

	

# === Multi-Trigger ============================================================


time.sleep(0.01)
output.value = True

while True:
	scanInputs()
	time.sleep(0.1)
			 
	
