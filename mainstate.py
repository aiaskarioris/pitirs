import os
import time
from enum import Enum

from sense_hat import SenseHat
from gamestate import GameState

sense = SenseHat()
THRESH = 0.45
DEAD_HYST = 0.08


class MainStateEnum(Enum):
    wait_to_start = 0
    playing = 1
    game_over = 2
    exception = 3


# Renderer for debugging purposes
class CLIRenderer:
    def __init__(self):
        # Create the LED gird represantation
        self.p = []
        for i in range(0, 64):
            self.p.append([0, 0, 0])
        return

    # for game_over_loop
    def show_message(self, text):
        print("[CLI]", text)

    # for game_over_loop
    def clear(self):
        print("[CLI] clear")

    def set_pixels(self, p):
        # Store new pixels
        self.p = p

        # Clear screen
        os.system("clear")
        # print("")
        for l in range(0, 8):
            for c in range(0, 8):
                if p[l * 8 + c] == 1:
                    print("█", end="")
                else:
                    print(" ", end="")
                print("")

    def get_pixels(self):
        return self.p


class MainState:
    def __init__(self):
        # self.renderer = CLIRenderer() # or SenseHat()
        self.renderer = SenseHat()
        self.state = MainStateEnum.wait_to_start
        self.frame = 0
        self.refresh_time_ms = 300
        self.game = None
        self.pixels = []
        self.begin = True

        global THRESH, DEAD_HYST, baseline, state
        THRESH = 0.45
        DEAD_HYST = 0.08
        baseline = self.renderer.get_accelerometer_raw()
        state = "CENTER"

    # Main loop
    def run(self):
        while True:
            self.renderer.set_rotation(270)
            print("Starting frame.")
            if self.state == MainStateEnum.wait_to_start:
                self.wait_to_start_loop()

            elif self.state == MainStateEnum.playing:
                self.playing_loop()

            elif self.state == MainStateEnum.game_over:
                self.game_over_loop()
                if self.frame > 2:
                    self.state = MainStateEnum.wait_to_start

            elif self.state == MainStateEnum.exception:
                self.exception_loop()

            self.frame += 1
            time.sleep(self.refresh_time_ms / 1000)

    ### State Functions ###########################################################################

    def get_delta(self):
        a = self.renderer.get_accelerometer_raw()
        dx = a["x"] - baseline["x"]
        dy = a["y"] - baseline["y"]

        dx, dy = dy, dx
        dx = -dx
        dy = -dy
        return dx, dy

    # Sub-Loops; Each loop can freely display things on screen and change the program's states
    def wait_to_start_loop(self):
        # Wait for input
        while self.state == MainStateEnum.wait_to_start and self.begin:
            self.renderer.show_message(
               "Press joystick to play!!", text_colour=[0, 0, 255], scroll_speed=0.05
            )

            time.sleep(1.5)
            for event in self.renderer.stick.get_events():
                if event.action == "pressed":
                    self.renderer.clear()
                    baseline = self.renderer.get_accelerometer_raw()
                    self.game = GameState()
                    self.state = MainStateEnum.playing
                    self.begin = False
                    return

        self.game = GameState()
        self.state = MainStateEnum.playing
        return

    def playing_loop(self):
        # Generate a random block if we don't have one (just started playing or prev. one was piled)
        if self.game.blockObj == None:
            self.game.generate_block()

        # Check input and apply effect to block
        global baseline, state

        # Re-zero (recalibrate) if joystick middle is pressed
        for ev in self.renderer.stick.get_events():
            if ev.action == "pressed" and ev.direction == "middle":
                baseline = self.renderer.get_accelerometer_raw()
                state = "CENTER"

        # get tilt deltas
        dx, dy = self.get_delta()

        new_state = "CENTER"
        if dx > THRESH:
            new_state = "RIGHT"
        elif dx < -THRESH:
            new_state = "LEFT"
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
                self.game.blockObj.move(-1)
                state = "CENTER"  # auto-reset so next tilt works again
            elif state == "RIGHT":
                self.game.blockObj.move(1)
                state = "CENTER"
            elif state == "UP":
                self.game.blockObj.rotate_left()
                state = "CENTER"
            elif state == "DOWN":
                self.game.blockObj.rotate_right()
                state = "CENTER"

        # If the top line has something on it it's game over
        self.game.check_overflow()

        # Allow block to drop by 1 pixel; The block may enter the pile in this function (thus clearing it)
        if self.frame % 2 == 0:
            self.game.drop_block()

        # Render current state; Create the 8x8 grid first and pass it to `.set_pixels` once
        self.clear_screen()
        self.draw_block()
        self.draw_pile()
        self.renderer.set_pixels(self.pixels)

        # Check if the pile has any full lines and drop remaining lines; score may be updated
        self.game.check_pile()

        # `check_pile` may generate a game-over; Check if this is the case
        if self.game.gameOver == True:
            self.frame = 0
            self.state = MainStateEnum.game_over

        # Update frame rate
        if self.game.score > 70:
            self.refresh_time_ms = min(100 - 5 * (self.game.score - 60) / 10, 40)
        if self.game.score > 50:
            self.refresh_time_ms = 100
        elif self.game.score > 30:
            self.refresh_time_ms = 200

        return

    def game_over_loop(self):
        global baseline
        while self.state == MainStateEnum.game_over:
            self.renderer.show_message(
                "GAME OVER! Score: " + str(self.game.score),
                text_colour=[255, 0, 0],
                scroll_speed=0.05,
            )
            self.renderer.show_message(
                "Press joystick to play!!", text_colour=[0, 0, 255], scroll_speed=0.05
            )
            self.frame = self.frame + 1
            print(str(self.frame))

            time.sleep(1.5)
            for event in self.renderer.stick.get_events():
                if event.action == "pressed":
                    self.renderer.clear()
                    baseline = self.renderer.get_accelerometer_raw()
                    self.state = MainStateEnum.wait_to_start
                    return

        baseline = self.renderer.get_accelerometer_raw()
        self.state = MainStateEnum.wait_to_start
        return

    def exception_loop(self):
        return

    ### Drawing Functions #########################################################################
    def clear_screen(self):
        self.pixels = []
        for i in range(0, 64):
            self.pixels.append([0, 0, 0])
        return

    def draw_block(self):
        # Get a reference
        p = self.pixels
        block = self.game.blockObj
        if block is None:
            return

        # Draw the block in columns
        idx = block.x + block.y * 8

        # Draw first column
        if block.d[0] == 1:
            p[idx] = block.palette
        if block.d[2] == 1:
            p[idx + 8] = block.palette

        # Draw second column; If the block is on the right-most column, wrap
        if block.x < 7:
            idx = block.x + 1 + block.y * 8
        else:
            idx = block.y * 8

        if block.d[1] == 1:
            p[idx] = block.palette
        if block.d[3] == 1:
            p[idx + 8] = block.palette

        return

    def draw_pile(self):
        pileCol = [80, 80, 80]
        pileObj = self.game.pileObj

        p = self.pixels

        for i in range(0, 64):
            if pileObj[i] == 1:
                p[i] = pileCol

        return
