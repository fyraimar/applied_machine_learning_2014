import csv
import sys

home_dict = {}
away_dict = {}
hometotal_game = {}
awaytotal_game = {}
team_dict = {}
playoff_dict = {}

min_year = 1947
max_year = 2006
stride = 1
start_year = min_year + stride
inputFile = 'NBA-Game-Results-2.csv'
outputFile = 'NBA.csv'
fieldname = ['Season', 'Team', str(stride) + 'HisotryHomeWinRatio', str(stride) + 'HistoryAwayWinRatio',
str(stride) + 'homeGainPoins', str(stride) + 'homeLosePoins', str(stride) + 'awayGainPoins', str(stride) + 'awayLosePoins',
 'firstPlay', 'inPlayoff']

with open(inputFile, 'rU') as f:
    reader = csv.DictReader(f);
    lines = [x for x in reader]
    for item in lines:
        if item['RegularSeason'] == '1':
            home_dict[(item['Season'], item['HomeTeam'], 'win')] = home_dict.get((item['Season'], item['HomeTeam'], 'win'), 0) + int(item['HomeWin'])
            away_dict[(item['Season'], item['AwayTeam'], 'win')] = away_dict.get((item['Season'], item['AwayTeam'], 'win'), 0) + int(item['AwayWin'])

            home_dict[(item['Season'], item['HomeTeam'], 'lose')] = home_dict.get((item['Season'], item['HomeTeam'], 'lose'), 0) + 1 - int(item['HomeWin'])
            away_dict[(item['Season'], item['AwayTeam'], 'lose')] = away_dict.get((item['Season'], item['AwayTeam'], 'lose'), 0) + 1 - int(item['AwayWin'])
            #home_dict[(item['Season'], item['HomeTeam'])] = home_dict.get((item['Season'], item['HomeTeam']), 0) + int(item['HomeWin'])
            #away_dict[(item['Season'], item['AwayTeam'])] = away_dict.get((item['Season'], item['AwayTeam']), 0) + int(item['AwayWin'])
            if item['HomeWin'] == '1':
                home_dict[(item['Season'], item['HomeTeam'], 'gainPoins')] =  home_dict.get((item['Season'], item['HomeTeam'], 'gainPoins'), 0) + int(item['HomeTeamScore']) - int(item['AwayTeamScore']);
                away_dict[(item['Season'], item['AwayTeam'], 'losePoins')] =  away_dict.get((item['Season'], item['AwayTeam'], 'losePoins'), 0) + int(item['HomeTeamScore']) - int(item['AwayTeamScore']);
            elif item['AwayWin'] == '1':
                home_dict[(item['Season'], item['HomeTeam'], 'losePoins')] =  home_dict.get((item['Season'], item['HomeTeam'], 'gainPoins'), 0) - int(item['HomeTeamScore']) + int(item['AwayTeamScore']);
                away_dict[(item['Season'], item['AwayTeam'], 'gainPoins')] =  away_dict.get((item['Season'], item['AwayTeam'], 'losePoins'), 0) - int(item['HomeTeamScore']) + int(item['AwayTeamScore']);
           
            if not team_dict.has_key(item['Season']):
               team_dict[item['Season']] = []

            if item['HomeTeam'] not in team_dict[item['Season']]:
                team_dict[item['Season']].append(item['HomeTeam'])
            if item['AwayTeam'] not in team_dict[item['Season']]:
                team_dict[item['Season']].append(item['AwayTeam'])

            if item['Neutral'] != '1':
                hometotal_game[(item['Season'], item['HomeTeam'])] = hometotal_game.get((item['Season'], item['HomeTeam']), 0) + 1
                awaytotal_game[(item['Season'], item['AwayTeam'])] = awaytotal_game.get((item['Season'], item['AwayTeam']), 0) + 1
        else:
            if not playoff_dict.has_key(item['Season']):
                playoff_dict[item['Season']] = []
            if item['HomeTeam'] not in playoff_dict[item['Season']]:
                playoff_dict[item['Season']].append(item['HomeTeam'])

#print team_dict['1950']

for year in range(start_year, max_year + 1):
        total_Home_game = {}
        total_Away_game = {}
        for past_year in range(1, stride + 1):
            for team in team_dict[str(year)]:
                home_dict[(str(year), team, 'winRatio')] =  home_dict.get((str(year), team, 'winRatio'), 0) + home_dict.get((str(year - past_year), team, 'win'),0)
                total_Home_game[team] = total_Home_game.get(team, 0) + hometotal_game[(str(year), team)]
                away_dict[(str(year), team, 'winRatio')] =  away_dict.get((str(year), team, 'winRatio'), 0) + away_dict.get((str(year - past_year), team, 'win'),0)
                total_Away_game[team] = total_Away_game.get(team, 0) + awaytotal_game[(str(year), team)]

                home_dict[(str(year), team, str(stride) + 'gainPoins')] = home_dict.get((str(year), team, str(stride) + 'gainPoins'), 0) + home_dict.get((str(year - past_year), team, 'gainPoins'),0)
                home_dict[(str(year), team, str(stride) + 'losePoins')] = home_dict.get((str(year), team, str(stride) + 'losePoins'), 0) + home_dict.get((str(year - past_year), team, 'losePoins'),0)
                away_dict[(str(year), team, str(stride) + 'gainPoins')] = away_dict.get((str(year), team, str(stride) + 'gainPoins'), 0) + away_dict.get((str(year - past_year), team, 'gainPoins'),0)
                away_dict[(str(year), team, str(stride) + 'losePoins')] = away_dict.get((str(year), team, str(stride) + 'losePoins'), 0) + away_dict.get((str(year - past_year), team, 'losePoins'),0)
                #print home_dict[(str(year), team, str(stride) + 'gainPoins')]
        for team in team_dict[str(year)]: 
                home_dict[(str(year), team, 'winRatio')] /= (float(total_Home_game[team]) / 100)
                away_dict[(str(year), team, 'winRatio')] /= (float(total_Away_game[team]) / 100)

                home_dict[(str(year), team, str(stride) + 'gainPoins')] /= float(total_Home_game[team])
                home_dict[(str(year), team, str(stride) + 'losePoins')] /= float(total_Home_game[team])
                away_dict[(str(year), team, str(stride) + 'gainPoins')] /= float(total_Away_game[team])
                away_dict[(str(year), team, str(stride) + 'losePoins')] /= float(total_Away_game[team])
#for x in home_dict:
#    win_dict[(x[0], x[1])] = float(home_dict.get((x[0], x[1]), 0) + away_dict.get((x[0], x[1]), 0)) / float(total_game.get((x[0], x[1]), 0))

with open(outputFile, 'wb') as f:
    writer = csv.DictWriter(f, fieldnames = fieldname )
    writer.writeheader()
#    for key, value in win_dict.items():
#        if value >= 0.5:
#            out = 'True'
#        else:
#            out = 'False'
    for year in range(start_year, max_year): 
        for team in team_dict[str(year)]:

            homewinRatio = home_dict[(str(year), team, 'winRatio')]
            awaywinRatio = away_dict[(str(year), team, 'winRatio')]
            writer.writerow({'Season' : year, 'Team' : team, str(stride) + 'HisotryHomeWinRatio' :homewinRatio,  str(stride) + 'HistoryAwayWinRatio' : awaywinRatio ,
                str(stride) + 'homeGainPoins': home_dict[(str(year), team, str(stride) + 'gainPoins')],
                str(stride) + 'homeLosePoins': home_dict[(str(year), team, str(stride) + 'losePoins')], 
                str(stride) + 'awayGainPoins': away_dict[(str(year), team, str(stride) + 'gainPoins')],
                str(stride) + 'awayLosePoins': away_dict[(str(year), team, str(stride) + 'losePoins')],
                 'firstPlay': awaywinRatio == 0 and homewinRatio == 0, 'inPlayoff':team in playoff_dict[str(year)]})
