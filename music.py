import pygame
import time

def play_music(file_path):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(1)

    except pygame.error as e:
        print(f"Error: {e}")
    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    music_file = ""  # Replace with the path to your music file # no file in there yet, will be added after I figure out API thing
    play_music(music_file)
