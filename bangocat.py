import sys
import time
import os
import random
import argparse

import numpy as np
import contextlib
import librosa

with contextlib.redirect_stdout(None):
    import pygame


def get_beat_times(audio_file):
    y, sr = librosa.load(audio_file)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
    beats_plp = np.flatnonzero(librosa.util.localmax(pulse))
    times = librosa.times_like(onset_env, sr=sr)
    beat_times = times[beats_plp]
    return beat_times


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", default="nyancat.mp3", type=str, help="File")
    parser.add_argument("-s", "--size", default=600, type=int, help="Size")
    parser.add_argument("-l", "--length", default=200,
                        type=int, help="Tap length in ms")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"{args.file} doesn't exist !")
        parser.print_help()
        exit()

    size = width, height = args.size, args.size
    black = (0, 0, 0)
    tap_length_ms = args.length / 1000

    img0 = pygame.image.load("00.png")
    imgs = [pygame.image.load("01.png"), pygame.image.load(
        "10.png"), pygame.image.load("11.png")]
    img0 = pygame.transform.scale(img0, size)
    imgs = [pygame.transform.scale(i, size) for i in imgs]

    pygame.mixer.init()
    pygame.mixer.music.load(args.file)

    beat_times = get_beat_times(args.file)

    pygame.init()
    pygame.display.set_caption("Bangocat")
    pygame.display.set_icon(img0)
    screen = pygame.display.set_mode(size)

    music_start = time.time()
    pygame.mixer.music.play()
    last_img = random.choice(imgs)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(black)

        delta_music_start = time.time() - music_start
        dists = [delta_music_start - i for i in beat_times]
        min_dists = min(dists, key=lambda x: abs(x))
        # always after the start of a beat (for tap_length_ms)
        should_tap = min_dists < tap_length_ms and min_dists > 0

        if should_tap:
            img = last_img
        else:
            img = img0
            last_img = random.choice(imgs)

        screen.blit(img, (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    run()
