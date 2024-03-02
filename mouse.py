import json
from pymouse import PyMouse
import time
import RPi.GPIO as GPIO
from pynput.keyboard import Key, Controller

GPIO.setmode(GPIO.BCM)

last_key3_press = 0
current_letter_index = 0
with open('/PRPZD/configs/keys.json') as f:
    w = json.load(f)
letters = w["low"]
low = w["low"]
symbols = w["symbols"]
capital = w["capitals"]

btn_up = 5
btn_down = 26
btn_left = 19
btn_right = 6
btn_press = 13
btn_key1 = 21
btn_key2 = 20
btn_key3 = 16

# Up, Down, left, right, Button
GPIO.setup(btn_up, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(btn_down, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(btn_left, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(btn_right, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(btn_press, GPIO.IN, GPIO.PUD_UP)  # Joystick press
GPIO.setup(btn_key1, GPIO.IN, GPIO.PUD_UP)  # left button
GPIO.setup(btn_key2, GPIO.IN, GPIO.PUD_UP)  # right button
GPIO.setup(btn_key3, GPIO.IN, GPIO.PUD_UP)  # mode toggle

mouse_mode = True  # True for mouse mode, False for text input mode
joystick_arrow_mode = False # ausencia

def cycle_letter(increment):
    global last_key3_press
    global current_letter_index

    now = time.time()
    should_delete = False

    if now - last_key3_press < 2:
        current_letter_index = (current_letter_index + increment) % len(letters)
        should_delete = True
    else:
        current_letter_index = 0

    last_key3_press = now
    return letters[current_letter_index], should_delete
def toggle_joystick_mode():
    global joystick_arrow_mode
    joystick_arrow_mode = not joystick_arrow_mode
    print("Joystick set to Arrow Keys" if joystick_arrow_mode else "Joystick set to Mouse Movement")

def keyboard_input(key, should_delete=False):
    keyboard = Controller()
    if should_delete:
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
    keyboard.press(key)
    keyboard.release(key)

def toggle_mode():
    global mouse_mode
    mouse_mode = not mouse_mode
    print("Switched to Mouse Mode" if mouse_mode else "Switched to Text Input Mode")

def main():
    global letters
    m = PyMouse()
    KEY1_flag = False
    KEY2_flag = False
    KEY3_flag = False
    KEYP_flag = False
    KEYcap = False
    KEYsym = False

    while True:
      nowxy = m.position()

      if (not GPIO.input(btn_key3)) and (not KEY3_flag):
            KEY3_flag = True
            toggle_mode()


      if GPIO.input(btn_key3):
        KEY3_flag = False

      if mouse_mode:
        if (not GPIO.input(btn_press)) and (not KEYP_flag):
            KEYP_flag = True
            print("what")
            toggle_joystick_mode()

        if GPIO.input(btn_press):
            KEYP_flag = False

        if joystick_arrow_mode:
            keyboard = Controller()
            if (not GPIO.input(btn_up)):
                keyboard.press(Key.left)
                keyboard.release(Key.left)

            if (not GPIO.input(btn_down)):
                keyboard.press(Key.right)
                keyboard.release(Key.right)

            if (not GPIO.input(btn_left)):
                keyboard.press(Key.down)
                keyboard.release(Key.down)

            if (not GPIO.input(btn_right)):
                keyboard.press(Key.up)
                keyboard.release(Key.up)
            time.sleep(0.08)
        else:
            if (not GPIO.input(btn_press)) and (not KEYP_flag):
              KEYP_flag = True
              print("what")
              toggle_joystick_mode()

            if GPIO.input(btn_press):
              KEYP_flag = False
            if (not GPIO.input(btn_key1)) and (not KEY1_flag):
                KEY1_flag = True
                m.click(nowxy[0], nowxy[1], 1)

            if GPIO.input(btn_key1):
                KEY1_flag = False

            if (not GPIO.input(btn_key2)) and (not KEY2_flag):
                KEY2_flag = True
                m.click(nowxy[0], nowxy[1], 2)

            if GPIO.input(btn_key2):
                KEY2_flag = False

            if (not GPIO.input(btn_up)):
                m.move(nowxy[0] - 5, nowxy[1])

            if (not GPIO.input(btn_down)):
                m.move(nowxy[0] + 5, nowxy[1])

            if (not GPIO.input(btn_left)):
                m.move(nowxy[0], nowxy[1] +5)

            if (not GPIO.input(btn_right)):
                m.move(nowxy[0], nowxy[1] - 5)
      else:
            time.sleep(0.1)
            if not GPIO.input(btn_key1) and not KEY1_flag:
                KEY1_flag = True
                if KEYcap == False:
                    letters = capital if letters != capital else low
                    print(f"Character set: {'Capital' if letters == capital else 'Low'}")
                    KEYcap = True
                else:
                    KEYcap == False
            if GPIO.input(btn_key1):
                KEY1_flag = False

            if not GPIO.input(btn_key2) and not KEY2_flag:
                KEY2_flag = True
                if KEYsym == False:
                    letters = symbols if letters != symbols else low
                    print(f"Character set: {'Symbols' if letters == symbols else 'Low'}")
                    KEYsym = True
                else:
                    KEYsym = False

            if GPIO.input(btn_key2):
                KEY2_flag = False



            if (not GPIO.input(btn_right)):
                next_letter, should_delete = cycle_letter(1)
                keyboard_input(next_letter, should_delete)

            if (not GPIO.input(btn_left)):
                next_letter, should_delete = cycle_letter(-1)
                keyboard_input(next_letter, should_delete)

            if (not GPIO.input(btn_up)):
                keyboard_input(Key.backspace)

            if (not GPIO.input(btn_down)):
                keyboard_input(' ')

            if (not GPIO.input(btn_press)):
                keyboard = Controller()
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)

      time.sleep(0.02)

if __name__ == "__main__":
    main()

