import numpy as np
from utils import *

class Controller:
	def __init__(self, 
					kp_linear = 0.1, kd_linear = 0.1, ki_linear = 0, 
					kp_angular = 0.1, kd_angular = 0.1, ki_angular = 0):
		self.kp_linear = kp_linear
		self.kd_linear = kd_linear
		self.ki_linear = ki_linear

		self.kp_angular = kp_angular
		self.kd_angular = kd_angular
		self.ki_angular = ki_angular

		self.prev_error_position = 0
		self.prev_error_angle = 0


	def get_control_inputs(self, x, goal_x, nose):
		error_position = get_distance(x[0, 0], x[1, 0], goal_x[0], goal_x[1])
		
		body_to_goal = get_angle(x[0, 0], x[1, 0], goal_x[0], goal_x[1])
		body_to_nose = get_angle(x[0, 0], x[1, 0], nose[0], nose[1])

		error_angle = body_to_nose - body_to_goal

		print(round(body_to_goal, 3), round(x[2, 0], 3), round(error_angle, 3))

		linear_velocity_control = self.kp_linear*error_position + self.kd_linear*(error_position - self.prev_error_position)
		angular_velocity_control = self.kp_angular*error_angle + self.kd_angular*(error_angle - self.prev_error_angle)

		self.prev_error_angle = error_angle
		self.prev_error_position = error_position

		return linear_velocity_control, angular_velocity_control
