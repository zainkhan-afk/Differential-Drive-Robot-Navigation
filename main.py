from car import Car
from draw import Draw


W, H = 400, 700
draw = Draw(W, H)

car = Car(50, 50)

lw = 0
rw = 0

while True:
	draw.clear()
	draw.draw(car.get_points(), color = (0, 255, 0))
	k = draw.show()
	car.update(0.5)
	car.set_wheel_velocity(lw, rw)

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