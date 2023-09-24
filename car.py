import numpy as np
from parameters import *

class Car:
	def __init__(self, x, y):
		self.x = np.array([
							[x],
							[y],
							[0]
						  ])

		self.x_dot = np.array([
							[0],
							[0],
							[0]
						  ])

		self.wheel_speed = np.array([
										[0],
										[0]
									])

		self.b = 25
		self.r = 5

		self.car_dims = np.array([
										[-self.b, -self.b, 1],
										[0 		, -self.b, 1],
										[ self.b,  		0, 1],
										[ 0, 	   self.b, 1],
										[ -self.b, self.b, 1]
									])

		self.get_transformed_pts()


	def set_wheel_velocity(self, lw_speed, rw_speed):
		self.wheel_speed = np.array([
										[rw_speed],
										[lw_speed]
									])
		self.x_dot = self.forward_kinematics()

	def set_robot_velocity(self, linear_velocity, angular_velocity):
		self.x_dot = np.array([
										[linear_velocity],
										[0],
										[angular_velocity]
									])
		self.wheel_speed = self.inverse_kinematics()


	def update_state(self, dt):
		A = np.array([
						[1, 0, 0],
						[0, 1, 0],
						[0, 0, 1]
					])
		B = np.array([
						[np.sin(self.x[2, 0] + np.pi/2)*dt,  0],
						[np.cos(self.x[2, 0] + np.pi/2)*dt,  0],
						[0					 , dt]
					])

		vel = np.array([
							[self.x_dot[0, 0]],
							[self.x_dot[2, 0]]
						])
		self.x = A@self.x + B@vel


	def update(self, dt):
		self.wheel_speed[self.wheel_speed>MAX_WHEEL_ROT_SPEED_RAD] = MAX_WHEEL_ROT_SPEED_RAD;
		self.wheel_speed[self.wheel_speed<MIN_WHEEL_ROT_SPEED_RAD] = MIN_WHEEL_ROT_SPEED_RAD;
		self.x_dot = self.forward_kinematics()
		self.update_state(dt)
		self.wheel_speed = self.inverse_kinematics()


	def get_state(self):
		return self.x, self.x_dot

	def forward_kinematics(self):
		kine_mat = np.array([
							[self.r/2  		  , self.r/2],
							[0 		 		  ,	0],
							[self.r/(2*self.b), -self.r/(2*self.b)]
							])

		return kine_mat@self.wheel_speed

	def inverse_kinematics(self):
		ikine_mat = np.array([
							[1/self.r, 0, self.b/self.r],
							[1/self.r, 0, -self.b/self.r]
							])

		return ikine_mat@self.x_dot

	def get_transformed_pts(self):
		rot_mat = np.array([
							[ np.cos(self.x[2, 0]), np.sin(self.x[2, 0]), self.x[0, 0]],
							[-np.sin(self.x[2, 0]), np.cos(self.x[2, 0]), self.x[1, 0]],
							[0, 0, 1]
							])

		self.car_points = self.car_dims@rot_mat.T

		self.car_points = self.car_points.astype("int")

	def get_points(self):
		self.get_transformed_pts()
		return self.car_points