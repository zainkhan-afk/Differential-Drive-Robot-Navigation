import numpy as np
from utils import *
from copy import deepcopy
from scipy.optimize import minimize

class PID:
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

		self.prev_body_to_goal = 0
		self.prev_waypoint_idx = -1


	def get_control_inputs(self, x, goal_x, nose, waypoint_idx):
		error_position = get_distance(x[0, 0], x[1, 0], goal_x[0], goal_x[1])
		
		body_to_goal = get_angle(x[0, 0], x[1, 0], goal_x[0], goal_x[1])
		body_to_nose = get_angle(x[0, 0], x[1, 0], nose[0], nose[1])

		# if self.prev_waypoint_idx == waypoint_idx and 350<(abs(self.prev_body_to_goal - body_to_goal)*180/np.pi):
		# 	print("HERE")
		# 	body_to_goal = self.prev_body_to_goal
		error_angle = (-body_to_goal) - x[2, 0]

		linear_velocity_control = self.kp_linear*error_position + self.kd_linear*(error_position - self.prev_error_position)
		angular_velocity_control = self.kp_angular*error_angle + self.kd_angular*(error_angle - self.prev_error_angle)

		self.prev_error_angle = error_angle
		self.prev_error_position = error_position

		self.prev_waypoint_idx = waypoint_idx
		self.prev_body_to_goal = body_to_goal

		if linear_velocity_control>5:
			linear_velocity_control = 5

		return linear_velocity_control, angular_velocity_control


class MPC:
	def __init__(self, horizon):
		self.horizon = horizon
		self.R = np.diag([0.01, 0.01])                 # input cost matrix
		self.Rd = np.diag([0.01, 1.0])                 # input difference cost matrix
		self.Q = np.diag([1.0, 1.0])                   # state cost matrix
		self.Qf = self.Q							   # state final matrix

	def cost(self, u_k, car, path):
		path = np.array(path)
		controller_car = deepcopy(car)
		u_k = u_k.reshape(self.horizon, 2).T
		z_k = np.zeros((2, self.horizon+1))

		desired_state = path.T

		cost = 0.0

		for i in range(self.horizon):
			controller_car.set_robot_velocity(u_k[0,i], u_k[1,i])
			controller_car.update(0.5)
			x, _ = controller_car.get_state()
			z_k[:,i] = [x[0, 0], x[1, 0]]
			cost += np.sum(self.R@(u_k[:,i]**2))
			cost += np.sum(self.Q@((desired_state[:,i]-z_k[:,i])**2))
			if i < (self.horizon-1):     
				cost += np.sum(self.Rd@((u_k[:,i+1] - u_k[:,i])**2))

		return cost

	def optimize(self, car, points):
		self.horizon = len(points)
		bnd = [(0, 5),(np.deg2rad(-60), np.deg2rad(60))]*self.horizon
		result = minimize(self.cost, args=(car, points), x0 = np.zeros((2*self.horizon)), method='SLSQP', bounds = bnd)
		return result.x[0],  result.x[1]
