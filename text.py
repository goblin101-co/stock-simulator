import sys, subprocess

def clear_screen():
    operating_system=sys.platform

    if operating_system == 'win32':
        subprocess.run('cls', shell = True)
    elif operating_system == 'linux' or operating_system == 'darwin':
        subprocess.run('cls', shell = True)