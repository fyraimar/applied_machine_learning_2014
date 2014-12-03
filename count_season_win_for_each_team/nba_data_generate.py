import csv
import sys

home_dict = {}
away_dict = {}
total_game = {}
win_dict = {}

fieldnames = {'Season', 'Team', 'AboveHalf', 'HomeWin', 'AwayWin'}

with open(sys.argv[1], 'rb') as f:
    reader = csv.DictReader(f);
    lines = [x for x in reader]
    for item in lines:
        home_dict[(item['Season'], item['HomeTeam'])] = home_dict.get((item['Season'], item['HomeTeam']), 0) + int(item['HomeTeamWin'])
        away_dict[(item['Season'], item['AwayTeam'])] = away_dict.get((item['Season'], item['AwayTeam']), 0) + int(item['AwayTeamWin'])
        total_game[(item['Season'], item['HomeTeam'])] = total_game.get((item['Season'], item['HomeTeam']), 0) + 1;
        total_game[(item['Season'], item['AwayTeam'])] = total_game.get((item['Season'], item['AwayTeam']), 0) + 1;

for x in home_dict:
    win_dict[(x[0], x[1])] = float(home_dict.get((x[0], x[1]), 0) + away_dict.get((x[0], x[1]), 0)) / float(total_game.get((x[0], x[1]), 0))

with open(sys.argv[2], 'wb') as f:
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()
    for key, value in win_dict.items():
        if value >= 0.5:
            out = 'True'
        else:
            out = 'False'

        writer.writerow({'Season' : key[0], 'Team' : key[1], 'AboveHalf' : out, 'HomeWin' : home_dict.get((key[0], key[1])), 'AwayWin' : away_dict.get((key[0], key[1]))})

