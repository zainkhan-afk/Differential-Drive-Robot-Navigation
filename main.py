from car import Car
from draw import Draw
from controllers import PID, MPC
import cv2
from utils import *
import argparse


parser = argparse.ArgumentParser(description='Process some integers.')


parser.add_argument('--controller', default="PID", 
		help="Select the controller for the robot.\nAvailable:\n1) MPC\n2) PID\nDefault: PID")

args = parser.parse_args()
controller_name = args.controller.upper()


if controller_name not in ["PID", "MPC"]:
	print("Invalid controller used. Available controllers: MPC and PID.")
	exit()

print(f"Using {controller_name} Controller.")

way_points = []
horizon = 5
def add_waypoint(event, x, y, flags, param):
    global way_points
    if event == cv2.EVENT_LBUTTONDOWN:
        way_points.append([x, y])
    if event == cv2.EVENT_RBUTTONDOWN:
        way_points.pop()

W, H = 700, 700
draw = Draw(W, H, window_name = "Canvas", mouse_callback = add_waypoint)

car = Car(50, 50)

if controller_name == "PID":
	controller = PID(kp_linear = 0.5, kd_linear = 0.1, ki_linear = 0,
							kp_angular = 3, kd_angular = 0.1, ki_angular = 0)
if controller_name == "MPC":
	controller = MPC(horizon = horizon)


lw = 0
rw = 0
current_idx = 0
linear_v = 0
angular_v = 0
car_path_points = []
while True:
	draw.clear()
	draw.add_text("Press the right click to place a way point, press the left click to remove a way point", 
					color = (0, 0, 0), fontScale = 0.5, thickness = 1, org = (5, 20))
	if len(way_points)>0:
		draw.draw_path(way_points, color = (200, 200, 200), thickness = 1)

	if len(car_path_points)>0:
		draw.draw_path(car_path_points, color = (255, 0, 0), thickness = 1, dotted = True)

	draw.draw(car.get_points(), color = (255, 0, 0), thickness = 1)
	

	k = draw.show()

	x, _ = car.get_state()
	if len(way_points)>0 and current_idx != len(way_points):
		car_path_points.append([int(x[0, 0]), int(x[1, 0])])
		goal_pt = way_points[current_idx]

		if controller_name == "PID":
			linear_v, angular_v = controller.get_control_inputs(x, goal_pt, car.get_points()[2], current_idx)
		
		if controller_name == "MPC":
			linear_v, angular_v = controller.optimize(car = car, points = way_points[current_idx:current_idx+horizon])
		
		dist = get_distance(x[0, 0], x[1, 0], goal_pt[0], goal_pt[1])
		if dist<10:
			current_idx+= 1
	else:
		linear_v = 0
		angular_v = 0
	car.set_robot_velocity(linear_v, angular_v)
	car.update(0.5)

	if k == ord("q"):
		break