# Importing libraries
import time
import keyboard


def release(key):
	'''
	`Input`
		- key: keyboard key-name

	`Output`
		- Releases keyboard's `key` if pressed
	'''
	try:
		keyboard.release(hotkey=key)
	except:
		pass


def press(key):
	'''
	`Input`
		- key: keyboard key-name

	`Output`
		- Presses keyboard's `key`
		- Returns `key` if successfully pressed else returns empty-string
	'''
	try:
		keyboard.press(hotkey=key)
		return key
	except:
		return ''


def send(key):
	'''
	`Input`
		- key: keyboard key-name

	`Output`
		- Presses `key` for 0.05 sec & then releases it
		- Returns empty-string if successfully else returns `key`
	'''
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