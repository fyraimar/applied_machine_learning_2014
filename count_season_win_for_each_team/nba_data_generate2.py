import csv
import sys

game_dict = {}
score_dict = {}
po_dict = {}

fieldnames = {'Season', 'Team', 'HomeScore', 'AwayScore', 'ifPO'}

with open(sys.argv[1], 'rb') as f:
    reader = csv.DictReader(f);
    lines = [x for x in reader]
    for item in lines:
        score_dict[(item['Season'], item['HomeTeam'], 'home')] = score_dict.get((item['Season'], item['HomeTeam'], 'home'), 0.0) + float(item['HomeTeamScore'])
        score_dict[(item['Season'], item['AwayTeam'], 'away')] = score_dict.get((item['Season'], item['AwayTeam'], 'away'), 0.0) + float(item['AwayTeamScore'])
        game_dict[(item['Season'], item['HomeTeam'], 'home')] = game_dict.get((item['Season'], item['HomeTeam'], 'home'), 0) + 1
        game_dict[(item['Season'], item['AwayTeam'], 'away')] = game_dict.get((item['Season'], item['AwayTeam'], 'away'), 0) + 1
        po_dict[(item['Season'], item['HomeTeam'])] = 'true' if item['RegularSeason'] == '0' else 'false'
        po_dict[(item['Season'], item['AwayTeam'])] = 'true' if item['RegularSeason'] == '0' else 'false'


for x in game_dict:
    score_dict[(x[0], x[1], x[2])] = float(score_dict.get((x[0], x[1], x[2]), 0.0)) / float(game_dict.get((x[0], x[1], x[2]), 0))

with open(sys.argv[2], 'wb') as f:
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()

    for (k, v) in game_dict.items():
        if k[2] == 'home':
            print k[0], k[1]
            print po_dict.get((k[0], k[1]))
            writer.writerow({'Season' : k[0], 'Team' : k[1], 'HomeScore' : score_dict.get((k[0], k[1], 'home'), 0.0), 'AwayScore' : score_dict.get((k[0], k[1], 'away'), 0.0), 'ifPO' : po_dict.get((k[0], k[1]))})


