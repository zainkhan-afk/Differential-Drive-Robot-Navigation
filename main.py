from car import Car
from draw import Draw
from controllers import PID
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
controller = PID(kp_linear = 0.5, kd_linear = 0.1, ki_linear = 0,
						kp_angular = 3, kd_angular = 0.1, ki_angular = 0)

lw = 0
rw = 0
current_idx = 0
linear_v = 0
angular_v = 0
car_path_points = []
while True:
	draw.clear()
	draw.add_text("Press right click to place waypoint, press left click to remove a way point", 
					color = (0, 0, 0), fontScale = 0.5, thickness = 1, org = (50, 15))
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
		linear_v, angular_v = controller.get_control_inputs(x, goal_pt, car.get_points()[2], current_idx)
		dist = get_distance(x[0, 0], x[1, 0], goal_pt[0], goal_pt[1])
		if dist<10:
			current_idx+= 1
	else:
		linear_v = 0
		angular_v = 0
	car.set_robot_velocity(linear_v, angular_v)
	# car.set_wheel_velocity(lw, rw)
	# car.set_robot_velocity(linear_v, angular_v)
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