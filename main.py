from car import Car
from draw import Draw
from controller import Controller
import cv2
from utils import *



way_points = []
def add_waypoint(event, x, y, flags, param):
    global way_points
    if event == cv2.EVENT_LBUTTONDOWN:
        way_points.append([x, y])
    if event == cv2.EVENT_RBUTTONDOWN:
        way_points.pop()

W, H = 700, 700
draw = Draw(W, H, window_name = "Canvas", mouse_callback = add_waypoint)

car = Car(50, 50)
controller = Controller(kp_linear = 0.1, kd_linear = 0, ki_linear = 0,
						kp_angular = 3, kd_angular = 0.01, ki_angular = 0)

lw = 0
rw = 0
current_idx = 0

while True:
	draw.clear()
	if len(way_points)>0:
		draw.draw_path(way_points, color = (255, 0, 0), thickness = 2)
	draw.draw(car.get_points(), color = (0, 255, 0))
	

	k = draw.show()

	x, _ = car.get_state()
	if len(way_points)>0 and current_idx != len(way_points):
		goal_pt = way_points[current_idx]
		linear_v, angular_v = controller.get_control_inputs(x, goal_pt, car.get_points()[2])
		dist = get_distance(x[0, 0], x[1, 0], goal_pt[0], goal_pt[1])
		if dist<10:
			current_idx+= 1
		car.set_robot_velocity(linear_v, angular_v)
	car.update(0.5)

	if k == ord("q"):
		break

	if k == ord("w"):
		lw += 0.5

	if k == ord("s"):
		lw -= 0.5

	if k == ord("e"):
		rw += 0.5

	if k == ord("d"):
		rw -= 0.5

	if k == ord("i"):
		linear_v += 0.5

	if k == ord("k"):
		linear_v -= 0.5

	if k == ord("o"):
		angular_v += 0.5

	if k == ord("l"):
		angular_v -= 0.5