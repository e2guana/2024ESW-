from src.game_start import GameStart
from src.game_situation import GameSituation


while True:
    if GameSituation.getGameReady():
        GameSituation.setGameReady(False)
        game_ready = GameStart()
        game_ready()