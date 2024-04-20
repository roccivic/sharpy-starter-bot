import random
from bottymcbotface.builds.one_base_reaper import OneBaseReaper
from bottymcbotface.builds.one_base_stim import OneBaseStim
from bottymcbotface.builds.two_base_tank import TwoBaseTank

num = random.random()
if num  > 0.66:
    print('ONE_BASE_REAPER')
    BottyMcBotFace = OneBaseReaper
elif num > 0.33:
    print('TWO_BASE_TANKS_ALL_IN')
    BottyMcBotFace = TwoBaseTank
else:
    print('ONE_BASE_STIM_ALL_IN')
    BottyMcBotFace = OneBaseStim
