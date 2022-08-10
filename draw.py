import cv2
import numpy as np

class Draw:
	def __init__(self, W, H, window_name, mouse_callback):
		self.W = W
		self.H = H
		self.window_name = window_name
		self.canvas = np.zeros((self.H, self.W, 3)).astype("uint8")
		cv2.namedWindow(self.window_name)
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

	def draw_path(self, points, color = (255, 0, 0), thickness = 2):
		for i in range(len(points)-1):
			cv2.circle(self.canvas, (points[i][0], points[i][1]), 5, (255, 255, 0), thickness)
			cv2.line(self.canvas, 
						(points[i][0], points[i][1]), 
						(points[i+1][0], points[i+1][1]), 
						color, thickness)

		cv2.circle(self.canvas, (points[-1][0], points[-1][1]), 5, (255, 255, 0), thickness)

	def show(self):
		cv2.imshow(self.window_name, self.canvas)
		k = cv2.waitKey(30)

		return k