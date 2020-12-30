# Importing libraries
import cv2
import math
import time
import win32gui
import win32process
import mediapipe as mp
import key_mapping


class GestureDriving:
	def __init__(self, proc, frame_width=720, frame_height=720, fps_div=1, min_detection_conf=0.5, min_tracking_conf=0.5, measure=0, nitrous=0, dir_thr_sm=10, dir_thr_bg=30, app_flag=False):
		'''
		`Input`
			- proc: psutil.Process object
			- frame_width: width of the input camera video
			- frame_height: height of the input camera video
			- fps_div: frames to be considered apart from each other
			- min_detection_conf: minimum detection confidence
			- min_tracking_conf: minimum tracking confidence
			- measure: `0` for distance measure or `1` for comparison measure
			- nitrous: `0` for no-nitrous or `1` for nitrous support
			- dir_thr_sm: direction threshold small
			- dir_thr_bg: direction threshold big
			- app_flag: apply keyboard mapping to all applications

		`Output`
			- GestureDriving class object
		'''
		self.proc = proc
		self.frame_width = frame_width
		self.frame_height = frame_height
		self.fps_div = fps_div
		self.min_detection_conf = min_detection_conf
		self.min_tracking_conf = min_tracking_conf
		self.measure = measure
		self.nitrous = nitrous
		self.direction_threshold_small = dir_thr_sm
		self.direction_threshold_big = dir_thr_bg
		self.app_flag = app_flag

		self.mp_drawing = mp.solutions.drawing_utils
		self.mp_hands = mp.solutions.hands

		self.circle_radius = self.mp_drawing.DrawingSpec.circle_radius
		self.color_red = (0, 0, 255)
		self.color_green = (0, 255, 0)
		self.color_blue = (255, 0, 0)
		self.thickness = self.mp_drawing.DrawingSpec.thickness

		self.hands = self.mp_hands.Hands(
			static_image_mode=False,
			max_num_hands=2,
			min_detection_confidence=self.min_detection_conf,
			min_tracking_confidence=self.min_tracking_conf
		)

		self.action_a = 4
		self.action_b = 6
		# self.action_b = 1

		self.winname = 'CameraFeed for {}'.format(self.proc.name()) if self.proc else 'DemoMode'
		self.fps_str = 'FPS for {}:'.format(self.proc.name()) if self.proc else 'FPS:'
		self.reset()


	def reset(self):
		'''Resets counts & actions'''
		self.n_frame = 0
		self.cnt_frame = 0

		self.prev_act = ''
		self.prev_dir = ''


	def draw_circle(self, pt):
		'''
		`Input`
			- pt: location of center of circle

		`Output`
			- Draws a circle at the given `pt`
		'''
		self.pt = pt
		cv2.circle(
			img=self.image,
			center=self.pt,
			radius=self.circle_radius,
			color=self.color_red,
			thickness=self.thickness,
			lineType=None,
			shift=None
		)


	def draw_text(self, txt, loc):
		'''
		`Input`
			- txt: text to be drawn on image
			- loc: location of bottom-left corner of `txt`

		`Output`
			- Draws the `txt` at the given `loc`
		'''
		self.txt = txt
		self.loc = loc
		cv2.putText(
			img=self.image,
			text=self.txt,
			org=self.loc,
			fontFace=cv2.FONT_HERSHEY_SIMPLEX,
			fontScale=1,
			color=self.color_blue,
			thickness=2,
			lineType=cv2.LINE_AA,
			bottomLeftOrigin=False
		)


	def chk_process(self):
		'''Checks if the Process is running'''
		if self.proc:
			return self.proc.is_running()
		else:
			return True


	def action(self, a, b, flag):
		'''
		`Input`
			- a: first point co-ordinate
			- b: second point co-ordinate
			- flag: `0` for left-hand or `1` for right-hand

		`Output`
			- Determines corresponding action
			- Returns action text
		'''
		self.flag = flag
		self.a = a
		self.b = b
		self.condn = (self.a >= self.b) if self.measure else (abs(self.a - self.b) < self.threshold)

		if self.condn:
			if self.flag:
				self.txt = 'ctrl+up' if self.nitrous else 'up'
			else:
				self.txt = 'down'
		else:
			self.txt = 'up' if self.nitrous else ''
		return self.txt


	def execute(self):
		'''Runs the GestureDriving Process'''
		self.s = time.time()
		self.cap = cv2.VideoCapture(index=0, apiPreference=cv2.CAP_ANY)
		# print(self.cap.getBackendName()) 			# checking which apiPreference selected by opencv
		self.cap.set(propId=cv2.CAP_PROP_FRAME_WIDTH, value=self.frame_width)
		self.cap.set(propId=cv2.CAP_PROP_FRAME_HEIGHT, value=self.frame_height)
		self.reset()

		while (self.cap.isOpened() & self.chk_process()):
			self.success, self.image = self.cap.read()

			if ((self.success) and ((self.n_frame%self.fps_div) == 0)):
				# Flip the image horizontally for a later selfie-view display, and convert the BGR image to RGB.
				self.image = cv2.cvtColor(src=cv2.flip(src=self.image, flipCode=1, dst=None), code=cv2.COLOR_BGR2RGB, dst=None, dstCn=None)
				
				# To improve performance, optionally mark the image as not writeable to pass by reference.
				self.image.flags.writeable = False
				
				self.results = self.hands.process(image=self.image)

				# Draw landmark annotation on the image.
				self.image.flags.writeable = True
				self.image = cv2.cvtColor(src=self.image, code=cv2.COLOR_RGB2BGR, dst=None, dstCn=None)
				
				# self.image_rows, self.image_cols = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(cv2.CAP_PROP_FRAME_WIDTH)
				self.image_rows, self.image_cols, _ = self.image.shape

				if self.results.multi_hand_landmarks:
					# https://google.github.io/mediapipe/images/mobile/hand_landmarks.png
					self.dct = {0: [], 1: [], 4: [], 5: [], 6:[]}
					self.center = (self.image_cols//2, self.image_rows//2)
					self.centers = []

					# iterating over hand landmarks
					for self.hand_landmarks in self.results.multi_hand_landmarks:
						# drawing landmarks for a hand
						self.mp_drawing.draw_landmarks(
							image=self.image,
							landmark_list=self.hand_landmarks,
							connections=self.mp_hands.HAND_CONNECTIONS
						)

						# storing reqd. landmarks of a hand
						for self.key in self.dct.keys():
							self.dct[self.key].append((self.hand_landmarks.landmark[self.key].x, self.hand_landmarks.landmark[self.key].y))

					# locating center pt. of palm(s)
					for self.wrist, self.index_finger_mcp in zip(self.dct[0], self.dct[5]):
						self.x = (self.wrist[0] + self.index_finger_mcp[0]) / 2
						self.y = (self.wrist[1] + self.index_finger_mcp[1]) / 2
						self.center_pt = self.mp_drawing._normalized_to_pixel_coordinates(
							normalized_x=self.x,
							normalized_y=self.y,
							image_width=self.image_cols,
							image_height=self.image_rows
						)
						self.draw_circle(pt=self.center_pt)
						self.centers.append(self.center_pt)

					# calculating hand/palm size
					# self.hand_size = abs(self.dct[1][0][1] - self.dct[0][0][1])
					self.hand_size = abs(self.dct[6][0][1] - self.dct[0][0][1])
					self.threshold = 0.38 * self.hand_size

					# checking the order of hand detected (0: Left, 1: Right)
					self.first_hand = bool(self.results.multi_handedness[0].classification[0].index)
					self.cur_act = self.action(a=self.dct[self.action_a][0][1], b=self.dct[self.action_b][0][1], flag=self.first_hand)

					if (len(self.results.multi_handedness) > 1):
						# dual hands
						self.x = (self.centers[0][0] + self.centers[1][0]) // 2
						self.y = (self.centers[0][1] + self.centers[1][1]) // 2
						self.center = (self.x, self.y)

						if (self.cur_act != 'down'):
							self.second_hand = not self.first_hand
							self.tmp = self.action(a=self.dct[self.action_a][1][1], b=self.dct[self.action_b][1][1], flag=self.second_hand)

							self.tmp_condn = (self.tmp != 'up') if self.nitrous else (self.tmp != '')
							if (self.tmp_condn):
								self.cur_act = self.tmp

					else:
						# single hand
						self.centers.append(self.center)
					
					# drawing (center of centers for dual-hand) or (center of frame for single-hand)
					self.draw_circle(pt=self.center)

					# connecting centers
					cv2.line(
						img=self.image,
						pt1=self.centers[0],
						pt2=self.centers[1],
						color=self.color_green,
						thickness=self.thickness,
						lineType=None,
						shift=None
					)

					# calculating angle of rotation
					try:
						self.tan_theta = ((self.centers[0][1] - self.center[1]) / (self.centers[0][0] - self.center[0]))
						self.theta = math.degrees(math.atan(self.tan_theta))
					except ZeroDivisionError:
						self.theta = 90
					except:
						self.theta = 0

					# determining direction
					self.direction_big_flag = False
					if (self.theta > self.direction_threshold_small):
						self.cur_dir = 'right'
						self.direction_big_flag = self.theta > self.direction_threshold_big
					elif (self.theta < (-1 * self.direction_threshold_small)):
						self.cur_dir = 'left'
						self.direction_big_flag = self.theta < (-1 * self.direction_threshold_big)
					else:
						self.cur_dir = ''

					# checking if there is a process or dummy-mode
					if self.proc:
						# checking if process window is focused
						if ((self.proc.pid == win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[-1]) or self.app_flag):
							# applying direction
							if (self.cur_dir != self.prev_dir):
								key_mapping.release(key=self.prev_dir)
								if (self.cur_dir != ''):
									if self.direction_big_flag:
										self.prev_dir = key_mapping.press(key=self.cur_dir)
									else:
										self.prev_dir = key_mapping.send(key=self.cur_dir)

							# applying motion
							if (self.cur_act != self.prev_act):
								key_mapping.release(key=self.prev_act)
								self.prev_act = key_mapping.press(key=self.cur_act)

					# drawing text on image
					self.draw_text(txt='{} + {}'.format(self.cur_act, self.cur_dir), loc=(50, 50))
					self.draw_text(txt='{:.2f}'.format(self.theta), loc=(450, 50))

				else:
					key_mapping.release(key=self.prev_act)
					key_mapping.release(key=self.prev_dir)
					self.prev_act = ''
					self.prev_dir = ''

				cv2.imshow(winname=self.winname, mat=self.image)
				self.cnt_frame += 1

			if cv2.waitKey(5) & 0xFF == 27:
				break

			self.n_frame += 1

		self.cap.release()
		cv2.destroyWindow(winname=self.winname)
		key_mapping.release(key=self.prev_act)
		key_mapping.release(key=self.prev_dir)

		self.e = time.time()
		print(self.fps_str, self.cnt_frame/(self.e-self.s), sep=' ', end='\n', flush=False)