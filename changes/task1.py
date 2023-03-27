#we import the neccessary libraries
import cv2 
import numpy as np

#this class creates a robots movement
class Car: 
 def __init__(self, x, y): 
  self.x = np.array([ #position of the robot
       [x], 
       [y], 
       [0] 
        ]) 
 
  self.x_dot = np.array([ #velocity of the robot
       [0], 
       [0], 
       [0] 
        ]) 
 
  self.wheel_speed = np.array([ #input speed for the robot
          [0], 
          [0] 
         ]) 
 
  self.b = 30 #distance between wheels 
  self.r = 5 #radius of the wheel
 
  self.car_dims = np.array([ #dimensions of the car
          [-self.b, -self.b, 1], 
          [self.b   , -self.b, 1],  
          [ self.b,     self.b, 1], 
          [ -self.b, self.b, 1] 
         ]) # here we create 4 points of the square that make up the robot itself
 
  self.get_transformed_pts() 
 
 
 def set_wheel_velocity(self, lw_speed, rw_speed): #this function sets the velocity of the wheels
  self.wheel_speed = np.array([ 
          [rw_speed], 
          [lw_speed] 
         ]) 
  self.x_dot = self.forward_kinematics() 
 
 
 def update_state(self, dt): #this function is needed to draw the robot on the canvas with the correct positions
  A = np.array([ 
      [1, 0, 0], 
      [0, 1, 0], 
      [0, 0, 1] 
     ]) 
  B = np.array([ 
      [np.sin(self.x[2, 0] + np.pi/2)*dt,  0], 
      [np.cos(self.x[2, 0] + np.pi/2)*dt,  0], 
      [0      , dt] 
     ]) 
 
  vel = np.array([ 
       [self.x_dot[0, 0]], 
       [self.x_dot[2, 0]] 
      ]) 
  self.x = A@self.x + B@vel 
 
 
 def update(self, dt): 
  self.x_dot = self.forward_kinematics() 
  self.update_state(dt) 
 
 def forward_kinematics(self): #fucntion that calculates the forward kinematics
  kine_mat = np.array([ 
       [self.r/2      , self.r/2], 
       [0        , 0], 
       [self.r/(2*self.b), -self.r/(2*self.b)] 
       ]) 
 
  return kine_mat@self.wheel_speed 
 
 def get_transformed_pts(self): #this is needed to correctly rotate the robot and draw its rotation
  rot_mat = np.array([ 
       [ np.cos(self.x[2, 0]), np.sin(self.x[2, 0]), self.x[0, 0]], 
       [-np.sin(self.x[2, 0]), np.cos(self.x[2, 0]), self.x[1, 0]], 
       [0, 0, 1] 
       ]) 
 
  self.car_points = self.car_dims@rot_mat.T 
 
  self.car_points = self.car_points.astype("int") 
 
 def get_points(self): #retrieving the coordinates of the robot
  self.get_transformed_pts() 
  return self.car_points

#this class is used to draw the robot, obstacles, and a light soucre
class Draw: 
	def __init__(self, W, H, window_name, color = (255, 255, 255)): #creating a canvas
		self.W = W
		self.H = H
		self.window_name = window_name
		self.color = color
		cv2.namedWindow(self.window_name)
		
	def clear(self): #clearing the canvas
		self.canvas = np.ones((self.H, self.W, 3)).astype("uint8")
		for i in range(len(self.color)):
			self.canvas[:, :, i] = self.canvas[:, :, i]*self.color[i]

	def draw(self, points, color = (255, 0, 0), thickness = 2): #drawing all the elements
		for i in range(len(points)-1): #drawing body of the robot
			cv2.line(self.canvas, 
						(points[i][0], points[i][1]), 
						(points[i+1][0], points[i+1][1]), 
						color, thickness)
		
		cv2.line(self.canvas, #the back line of the robot
						(points[0][0], points[0][1]), 
						(points[-1][0], points[-1][1]), 
						color, thickness)
          
          #these are the sensors of the robot
		cv2.circle(self.canvas,(points[1][0],points[1][1]), 10, (255,0,0), 1)
		cv2.circle(self.canvas,(points[2][0],points[2][1]), 10, (255,0,0), 1)

          #obstacles
		cv2.circle(self.canvas,(150,300), 20, (255,0,0), -1)
		cv2.circle(self.canvas,(300,150), 20, (255,0,0), -1)
		cv2.circle(self.canvas,(400,400), 20, (255,0,0), -1)

          #light source
		cv2.circle(self.canvas,(400,300), 5, (0,0,255), -1)
		
	def show(self): #showing the canvas
		cv2.imshow(self.window_name, self.canvas)
		k = cv2.waitKey(30)

		return k



W, H = 512, 512 #dimensions of the canvas
draw = Draw(W, H, window_name = "Homework 3") #name of the canvas

car = Car(200, 50) #spawning position of the robot
 
while True: #infinite loop
 draw.clear() #clear the canvas
 draw.draw(car.get_points(), color = (255, 0, 0), thickness = 1) #draws neccessary objects
 k = draw.show() #shows everything on canvas
 
 car.set_wheel_velocity(2,1.5) #setting the differential velocity of the robot 
 car.update(0.5) #updating the car position
 
 if k == ord("q"): #by pressing the button q we quit the program
  break
