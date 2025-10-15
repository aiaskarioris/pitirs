from sense_hat import SenseHat
import time

sense = SenseHat()
sense.set_rotation(270)  # LED orientation only
time.sleep(0.15)

X = [255, 0, 0]
O = [0, 0, 0]
right_arrow = [
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    X,
    X,
    X,
    X,
    X,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
]
left_arrow = [
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    X,
    X,
    X,
    X,
    X,
    X,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
]
up_arrow = [
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    X,
    X,
    O,
    O,
    O,
    O,
    X,
    O,
    X,
    O,
    X,
    O,
    O,
    X,
    O,
    O,
    X,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
]
down_arrow = [
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    X,
    O,
    O,
    X,
    O,
    O,
    X,
    O,
    X,
    O,
    X,
    O,
    O,
    O,
    O,
    X,
    X,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    X,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
    O,
]
blank = [O] * 64

THRESH = 0.45
DEAD_HYST = 0.08
SLEEP = 0.01

state = "CENTER"  # CENTER, LEFT, RIGHT, UP, DOWN


print("Waiting for joystick press...")
while True:
    sense.show_message("Press joystick to start", scroll_speed=0.05, text_colour=X)
    for e in sense.stick.get_events():
        if e.action == "pressed":
            break
    else:
        time.sleep(0.05)
        continue
    break

baseline = sense.get_accelerometer_raw()
sense.set_pixels(blank)
sense.show_message("GO!", scroll_speed=0.05, text_colour=[0, 255, 0])


def get_delta():
    a = sense.get_accelerometer_raw()
    dx = a["x"] - baseline["x"]
    dy = a["y"] - baseline["y"]

    dx, dy = dy, dx
    dx = -dx
    dy = -dy
    return dx, dy


try:
    while True:
        # Re-zero baseline on joystick middle press
        for ev in sense.stick.get_events():
            if ev.action == "pressed" and ev.direction == "middle":
                baseline = sense.get_accelerometer_raw()
                state = "CENTER"
                sense.set_pixels(blank)

        dx, dy = get_delta()

        new_state = "CENTER"
        if dx > THRESH:
            new_state = "RIGHT"
        elif dx < -THRESH:
            new_state = "LEFT"
            # else:
        elif dy > THRESH:
            new_state = "UP"
        elif dy < -THRESH:
            new_state = "DOWN"

        if state != "CENTER" and new_state == "CENTER":
            if state == "RIGHT" and dx > (THRESH - DEAD_HYST):
                new_state = "RIGHT"
            elif state == "LEFT" and dx < -(THRESH - DEAD_HYST):
                new_state = "LEFT"
            elif state == "UP" and dy > (THRESH - DEAD_HYST):
                new_state = "UP"
            elif state == "DOWN" and dy < -(THRESH - DEAD_HYST):
                new_state = "DOWN"

        if new_state != state:
            state = new_state
            if state == "LEFT":
                sense.set_pixels(left_arrow)
            elif state == "RIGHT":
                sense.set_pixels(right_arrow)
            elif state == "UP":
                sense.set_pixels(up_arrow)
            elif state == "DOWN":
                sense.set_pixels(down_arrow)
            else:
                sense.set_pixels(blank)

        time.sleep(SLEEP)

except KeyboardInterrupt:
    sense.clear()
