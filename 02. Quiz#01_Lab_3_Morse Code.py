import RPi.GPIO as GPIO
import time

# Define Morse code mapping
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
    'Y': '-.--', 'Z': '--..', 
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', 
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', 
    ' ': ' '
}

# GPIO setup
selected_pin = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(selected_pin, GPIO.OUT)

def led_on():
    GPIO.output(selected_pin, GPIO.HIGH)

def led_off():
    GPIO.output(selected_pin, GPIO.LOW)

def blink(duration):
    led_on()
    time.sleep(duration)
    led_off()
    time.sleep(duration)               # Pause between blinks

def morse_to_led(text, dot_length= 1):
    for char in text.upper():
        if char in morse_code:
            code = morse_code[char]
            for symbol in code:
                if symbol == '.':
                    blink(dot_length)
                elif symbol == '-':
                    blink(2.5)
                else:                   # Space between words
                    time.sleep(4)
                time.sleep(dot_length)  # Pause between symbols within a character
            time.sleep(2)               # Pause between characters
        else:
            time.sleep(8 * dot_length)  # Space not in Morse code dictionary

try:
    # Prompt user for input
    input_text = input("Enter a word to convert: ")
    morse_to_led(input_text)
except KeyboardInterrupt:
    print("\nConcersion finished.")
finally:
    GPIO.cleanup()
    print("GPIO cleanup completed.")
