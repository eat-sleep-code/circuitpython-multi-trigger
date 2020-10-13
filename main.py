from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
import board
import busio
import time


# === Thresholds ===============================================================

triggerBy = 'imperial'   # [imperial, metric, voltage]

pin1Threshold = 3
pin2Threshold = 3
pin3Threshold = 3
pin4Threshold = 3


# === Board Inputs =============================================================

pinCount = 4

pin1 = AnalogIn(board.D1)
pin2 = AnalogIn(board.D2)
pin3 = AnalogIn(board.D3)
pin4 = AnalogIn(board.D4)


# === Board Outputs ============================================================

output = DigitalInOut(board.D0)
output.direction = Direction.OUTPUT


# === On-board LEDs ============================================================

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT
dotstar = busio.SPI(board.APA102_SCK, board.APA102_MOSI)


# === Functions ================================================================

def getEstimatedDistance(voltage):
	voltageRounded = round(voltage, 1)
	imperial = 1000
	metric = 1000
	if (voltageRounded > 3):
		imperial = 2
	elif (voltageRounded > 2.8):
		imperial = 3
	elif (voltageRounded > 2.2):
		imperial = 4
	elif (voltageRounded > 1.8):
		imperial = 5
	elif (voltageRounded > 1.4):
		imperial = 6
	elif (voltageRounded > 1.2):
		imperial = 7
	elif (voltageRounded > 0.8):
		imperial = 8
	if imperial != 1000:
		metric = imperial * 25.4
	return imperial, metric

def getVoltage(pin):
	voltage = round((pin.value * 3.3) / 65536, 2)
	return voltage

def getPin(pin):
	voltage = 0
	if pin == 1:
		threshold = pin1Threshold
		voltage = getVoltage(pin1)
	elif pin == 2:
		threshold = pin2Threshold
		voltage = getVoltage(pin2)
	elif pin == 3:
		threshold = pin3Threshold
		voltage = getVoltage(pin3)
	elif pin == 4:
		threshold = pin4Threshold
		voltage = getVoltage(pin4)
	metric, imperial = getEstimatedDistance(voltage)
	return threshold, voltage, metric, imperial

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
			threshold, voltage, imperial, metric = getPin(pinNumber)
			print('Threshold: ', threshold)
			print('Voltage: ', '%.2f' % voltage )
			print('Imperial: ', '%.0f' % imperial )
			print('Metric: ', '%.0f' % metric )
			print('Trigger By: ', triggerBy)
			if (voltage >= threshold and triggerBy == 'voltage') or (metric <= threshold and triggerBy == 'metric') or (imperial <= threshold and triggerBy == 'imperial'):
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
			 
	
