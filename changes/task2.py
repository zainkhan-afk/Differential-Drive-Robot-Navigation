import cv2 
import numpy as np
import math

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

W, H = 512, 512 #size of the canvas
draw = Draw(W, H, window_name = "Homework 3") 

#setting inital velocities
vel_r = 1
vel_l = 1
diff = 0 #difference from the light sensors

#input from the sensors 
rl = 0  #right light sensor
ll = 0 #left light sensor
ro = 0 #right obstacle sensor
lo = 0 #left obstacle sensor

#spawning positions of the car
#car = Car(100, 50) 
#car = Car(400, 50) 
car = Car(50, 365) 


while True: 
    draw.clear() 
    draw.draw(car.get_points(), color = (255, 0, 0), thickness = 1) 
    k = draw.show() 
    
    coor = car.get_points() #get the coordinates from the robot
    
    #calculating the distance from each light sensor
    len_l = math.sqrt((400 - coor[1][0])**2 + (300 - coor[1][1])**2) #left light sensor
    len_r = math.sqrt((400 - coor[2][0])**2 + (300 - coor[2][1])**2) #right light sensor

    diff = len_l - len_r #calculating the difference

    #comparing the differences of the light source
    #whichever is closest to the light soucre gets activated
    #so the right light sensor becomes 1 if it is closer to the light source
    #if they are the same distance, then they both activate
    if diff > 3:
        ll = 0
        rl = 1
    elif diff < -3:
        ll = 1
        rl = 0
    elif  abs(diff) < 3:
        ll = 1
        rl = 1
   
    #checking whether the robot is hitting the obstacle
    #if left sensor hits the obstacle, then it gets activated and becomes 1
    #i compare the coordinates of the left obstacle sensor and the coordinates of the obstacle 
    #if they are the same, then it must be hitting it. 
    if ((coor[1][0] - 300)**2 + (coor[1][1] - 150)**2) <= 400:
        lo = 1
        ro = 0
    elif ((coor[2][0] - 300)**2 + (coor[2][1] - 150)**2) <= 400:
        lo = 0
        ro = 1
    elif ((coor[1][0] - 150)**2 + (coor[1][1] - 300)**2) <= 400:
        lo = 1
        ro = 0
    elif ((coor[2][0] - 150)**2 + (coor[2][1] - 300)**2) <= 400:
        lo = 0
        ro = 1
    elif ((coor[1][0] - 400)**2 + (coor[1][1] - 400)**2) <= 400:
        lo = 1
        ro = 0
    elif ((coor[2][0] - 400)**2 + (coor[2][1] - 400)**2) <= 400:
        lo = 0
        ro = 1
    else:
        lo = 0
        ro = 0   

    #this is a neural network
    #the weight of the light sensor is 0.3
    #the weight of the obstacle sensor is 1
    vel_l = (0.3*rl - 1*ro)*2
    vel_r = (0.3*ll - 1*lo)*2
    
    #we set the calculaated velocity
    car.set_wheel_velocity(vel_l, vel_r) 
    car.update(0.8) 

    if k == ord("q"): 
        break
