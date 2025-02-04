import sys, subprocess
import time

def clear_screen():
    operating_system=sys.platform

    if operating_system == 'win32':
        subprocess.run('cls', shell = True)
    elif operating_system == 'linux' or operating_system == 'darwin':
        subprocess.run('cls', shell = True)

def typewriter_effect(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line after the text is printed

def typewriter_input(prompt, delay=0.05):
    typewriter_effect(prompt, delay)
    return input()