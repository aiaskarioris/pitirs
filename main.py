
from mainstate import MainState

if __name__ == "__main__":
    print("Starting...")
    mainState = MainState()
    try:
        mainState.run()
    except KeyboardInterrupt:
        mainState.renderer.clear()
