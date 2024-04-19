import random
from bottymcbotface.builds.one_base_stim import OneBaseStim
from bottymcbotface.builds.two_base_tanks import TwoBaseTanks

if random.random() > 0.5:
    print('TWO_BASE_TANKS_ALL_IN')
    BottyMcBotFace = TwoBaseTanks
else:
    print('ONE_BASE_STIM_ALL_IN')
    BottyMcBotFace = OneBaseStim
