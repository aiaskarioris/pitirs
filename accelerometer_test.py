from sense_hat import SenseHat
import time

sense = SenseHat()
sense.set_imu_config(True, True, True)


# Colors
X = [255, 0, 0]
O = [0, 0, 0]

# Right arrow
right_arrow = [
    O, O, O, O, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, O, X, O, O, O,
    X, X, X, X, X, X, O, O,
    O, O, O, O, O, X, O, O,
    O, O, O, O, X, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, O, O, O, O, O
]


# Left arrow
left_arrow = [
    O, O, O, O, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, X, O, O, O, O, O,
    O, X, X, X, X, X, X, X,
    O, X, O, O, O, O, O, O,
    O, O, X, O, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, O, O, O, O, O
]

up_arrow = [
    O, O, O, X, O, O, O, O,
    O, O, X, X, X, O, O, O,
    O, X, O, X, O, X, O, O,
    X, O, O, X, O, O, X, O,
    O, O, O, X, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, O, O, O, O, O
]


down_arrow = [
    O, O, O, X, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, X, O, O, O, O,
    X, O, O, X, O, O, X, O,
    O, X, O, X, O, X, O, O,
    O, O, X, X, X, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, O, O, O, O, O
]


blank = [O] * 64

try:

    while True:

        # change text speed
        sc = 0.05

        sense.set_rotation(270)
        sense.show_message(f'Press joystick to play !!', text_colour = X,  scroll_speed = sc)
        time.sleep(1)
        for e in sense.stick.get_events():
            if e.action == 'pressed':
                break
        else:
            #time.sleep(0.1)
            continue
        break

    sense.set_rotation(0)


    while True:
        sense = SenseHat()
      #  sense.clear()
        raw = sense.get_compass_raw()
        y = raw['y']
        z = raw['z']
        sense.set_rotation(270)
        if y > -3:
            sense.set_pixels(left_arrow)
        elif y < -10:
            sense.set_pixels(right_arrow)
        elif z > 1:
            sense.set_pixels(up_arrow)
        elif z < -5:
            sense.set_pixels(down_arrow)
        else:
            sense.set_pixels(blank)

except KeyboardInterrupt:
    # clear on Ctrl+C
    sense.clear()
