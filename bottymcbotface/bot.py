import random
from bottymcbotface.builds.one_base_stim import OneBaseStim
from bottymcbotface.builds.two_base_tank import TwoBaseTank
from bottymcbotface.builds.three_base_marine_viking import ThreeBaseMarineViking

# num = random.random()
num = 1
if num  > 0.66:
    print('THREE_BASE_MARINE_VIKING')
    BottyMcBotFace = ThreeBaseMarineViking
elif num > 0.33:
    print('TWO_BASE_TANKS_ALL_IN')
    BottyMcBotFace = TwoBaseTank
else:
    print('ONE_BASE_STIM_ALL_IN')
    BottyMcBotFace = OneBaseStim
