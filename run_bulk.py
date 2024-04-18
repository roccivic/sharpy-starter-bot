import subprocess

for n in range(1,10):
    subprocess.call("python run_custom.py -m sc2-ai-cup-2022 -p1 bottymcbotface -p2 ai.terran.easy.rush".split(" "))
    subprocess.call("python run_custom.py -m sc2-ai-cup-2022 -p1 bottymcbotface -p2 ai.terran.medium.rush".split(" "))
    subprocess.call("python run_custom.py -m sc2-ai-cup-2022 -p1 bottymcbotface -p2 ai.terran.hard.rush".split(" "))
    subprocess.call("python run_custom.py -m sc2-ai-cup-2022 -p1 bottymcbotface -p2 ai.terran.veryhard.rush".split(" "))
