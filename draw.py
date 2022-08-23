import cv2
import numpy as np

class Draw:
	def __init__(self, W, H, window_name, mouse_callback = None):
		self.W = W
		self.H = H
		self.window_name = window_name
		self.canvas = np.zeros((self.H, self.W, 3)).astype("uint8")
		cv2.namedWindow(self.window_name)
		if mouse_callback is not None:
			cv2.setMouseCallback(self.window_name, mouse_callback)

	def clear(self):
		self.canvas = np.zeros((self.H, self.W, 3)).astype("uint8")

	def draw(self, points, color = (255, 0, 0), thickness = 2):
		for i in range(len(points)-1):
			cv2.line(self.canvas, 
						(points[i][0], points[i][1]), 
						(points[i+1][0], points[i+1][1]), 
						color, thickness)

		cv2.line(self.canvas, 
						(points[0][0], points[0][1]), 
						(points[-1][0], points[-1][1]), 
						color, thickness)

	def draw_path(self, points, color = (255, 0, 0), thickness = 2, dotted = False):
		for i in range(len(points)-1):
			if dotted:
				if i%2 == 0:
					cv2.circle(self.canvas, (points[i][0], points[i][1]), 2, color, thickness)
			else:
				cv2.line(self.canvas, 
							(points[i][0], points[i][1]), 
							(points[i+1][0], points[i+1][1]), 
							color, thickness)

	def add_text(self, text, color = (255, 0, 0), thickness = 2, fontScale = 1, org = (100, 50)):
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(self.canvas, text, org, font, 
						   fontScale, color, thickness, cv2.LINE_AA)

	def show(self):
		cv2.imshow(self.window_name, self.canvas)
		k = cv2.waitKey(30)

		return k