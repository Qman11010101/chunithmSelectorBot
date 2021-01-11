import random
import json

from .log import logger

def random_select(music_number=3, difficulty=None, dif_range=None, category=None, artist=None, notes=None, notes_range=None, bpm=None, bpm_range=None):
    logger("あ", "debug")
