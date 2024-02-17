import RPi.GPIO as GPIO
import time
import threading

# colors code in hexadecimal
color_h_code = [
            0xFF0000, 
            0xFFFF00, 
            0x00FF00,
            0x00FFFF, 
            0x0000FF,  
            0xFF00FF
            ]
# GPIO numbers
sel_pin = {'r_color': 25, 'g_color': 24, 'b_color': 23}  

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for selection in sel_pin.values():
    GPIO.setup(selection, GPIO.OUT)
    GPIO.output(selection, GPIO.HIGH)

# PWM
color_red = GPIO.PWM(sel_pin['r_color'], 2000)
color_green = GPIO.PWM(sel_pin['g_color'], 2000)
color_blue = GPIO.PWM(sel_pin['b_color'], 2000)
color_red.start(0)
color_green.start(0)
color_blue.start(0)

# control the main loop
running = True

def key_interrupt():
    global running
    input("Press Ctrl+C to stop the program...\n")
    running = False

# keyboard input
key_signal = threading.Thread(target=key_interrupt)
key_signal.start()

def calc_ratio(x, input_min, input_max, output_min, output_max):
    ratio = (x - input_min) / (input_max - input_min)
    mapped_value = ratio * (output_max - output_min) + output_min
    
    return mapped_value


def color_setup(set_col):
    r_v = (set_col & 0xFF0000) >> 16
    g_v = (set_col & 0x00FF00) >> 8
    b_v = (set_col & 0x0000FF) >> 0
    
    r_v = calc_ratio(r_v, 0, 255, 0, 100)
    g_v = calc_ratio(g_v, 0, 255, 0, 100)
    b_v = calc_ratio(b_v, 0, 255, 0, 100)
    
    color_red.ChangeDutyCycle(r_v)
    color_green.ChangeDutyCycle(g_v)
    color_blue.ChangeDutyCycle(b_v)

try:
    while running:
        for col in color_h_code:
            if not running:  # Check the flag
                break
            color_setup(col)
            time.sleep(1)
finally:
    color_red.stop()
    color_green.stop()
    color_blue.stop()
    for pin in sel_pin.values():
        GPIO.output(pin, GPIO.HIGH)  # off all LEDs
    GPIO.cleanup()
    print("GPIO cleanup....")
