# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json

from nba_api.stats.endpoints import shotchartdetail

dunk_score = 2;
points_per_foot = 0.045;

response = shotchartdetail.ShotChartDetail(
	context_measure_simple='FGA',
	team_id=0,
	player_id=201566,
	season_nullable='2021-22',
	season_type_all_star='Regular Season'
)

content = json.loads(response.get_json())

import pandas as pd

# transform contents into dataframe
results = content['resultSets'][0]
headers = results['headers']
rows = results['rowSet']
df = pd.DataFrame(rows)
df.columns = headers

print(headers)

df = df.reset_index()  # make sure indexes pair with number of rows

number_shots = 0
total_score = 0
for index, row in df.iterrows():
	print(row['SHOT_DISTANCE'], row['SHOT_TYPE'], row['SHOT_MADE_FLAG'])
	number_shots = number_shots + 1
	# total_score = total_score + (1 * row['SHOT_MADE_FLAG'])
	total_score = total_score + ((dunk_score + row['SHOT_DISTANCE'] * points_per_foot) * row['SHOT_MADE_FLAG'])

points_per_shot = total_score / number_shots
print(number_shots)
print(points_per_shot)


# # Iterate over columns using DataFrame.iteritems()
# for (colname,colval) in df.iteritems():
# 	if (colname == "SHOT_DISTANCE"):
# 		print(colname, colval.values)


# write to csv file
# df.to_csv( "jamesharden", index=False)

