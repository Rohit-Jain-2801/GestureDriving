# Importing libraries
import time
import keyboard


def release(key):
	try:
		keyboard.release(hotkey=key)
	except:
		pass


def press(key):
	try:
		keyboard.press(hotkey=key)
		return key
	except:
		return ''


def send(key):
	try:
		# keyboard.send(hotkey=key, do_press=True, do_release=True)
		# ---------------------------------------------------------
		keyboard.press(hotkey=key)
		# time.sleep(secs=0.5)
		# --------------------------------
		start = time.time()
		while((time.time()-start) < 0.05):
			continue
		# --------------------------------
		keyboard.release(hotkey=key)
		# ---------------------------------------------------------
		return ''
	except:
		return key