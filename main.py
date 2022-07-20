# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json

from nba_api.stats.endpoints import shotchartdetail

response = shotchartdetail.ShotChartDetail(
	context_measure_simple='FGA',
	team_id=0,
	player_id=201935,
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

# Iterate over columns using DataFrame.iteritems()
for (colname,colval) in df.iteritems():
    print(colname, colval.values)

# write to csv file
# df.to_csv( "jamesharden", index=False)

