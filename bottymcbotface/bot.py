import random
from bottymcbotface.builds.one_base_reaper import OneBaseReaper
from bottymcbotface.builds.one_base_stim import OneBaseStim
from bottymcbotface.builds.two_base_tank import TwoBaseTank
from bottymcbotface.builds.three_base_tank_viking import ThreeBaseTankViking

num = random.random()
if num  > 0.75:
    print('ONE_BASE_REAPER')
    BottyMcBotFace = OneBaseReaper
elif num  > 0.50:
    print('THREE_BASE_TANK_VIKING')
    BottyMcBotFace = ThreeBaseTankViking
elif num > 0.25:
    print('TWO_BASE_TANKS_ALL_IN')
    BottyMcBotFace = TwoBaseTank
else:
    print('ONE_BASE_STIM_ALL_IN')
    BottyMcBotFace = OneBaseStim
