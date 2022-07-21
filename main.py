# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import requests
import pandas as pd
import csv
import pickle

from nba_api.stats import endpoints
from nba_api.stats.endpoints import shotchartdetail

dunk_score = 2;
points_per_foot = 0.08;

max_shot_distance = 40


def get_player_pts_per_fga(player_id):
    response = shotchartdetail.ShotChartDetail(
        context_measure_simple='FGA',
        team_id=0,
        player_id=player_id,
        season_nullable='2021-22',
        season_type_all_star='Regular Season'
    )
    content = json.loads(response.get_json())

    # transform contents into dataframe
    results = content['resultSets'][0]
    headers = results['headers']
    rows = results['rowSet']
    df = pd.DataFrame(rows)
    df.columns = headers

    df = df.reset_index()  # make sure indexes pair with number of rows

    number_shots = 0
    total_score = 0
    for index, row in df.iterrows():
        # print(row['SHOT_DISTANCE'], row['SHOT_TYPE'], row['SHOT_MADE_FLAG'])
        number_shots = number_shots + 1
        # total_score = total_score + (1 * row['SHOT_MADE_FLAG'])
        total_score = total_score + ((dunk_score + row['SHOT_DISTANCE'] * points_per_foot) * row['SHOT_MADE_FLAG'])
        player_name = row['PLAYER_NAME']

    points_per_shot = total_score / number_shots
    outp = (player_id, player_name, points_per_shot)
    print(outp)
    return outp


def get_player_shots_per_distance(player_id):
    response = shotchartdetail.ShotChartDetail(
        context_measure_simple='FGA',
        team_id=0,
        player_id=player_id,
        season_nullable='2021-22',
        season_type_all_star='Regular Season'
    )
    content = json.loads(response.get_json())

    # transform contents into dataframe
    results = content['resultSets'][0]
    headers = results['headers']
    rows = results['rowSet']
    df = pd.DataFrame(rows)
    df.columns = headers

    df = df.reset_index()  # make sure indexes pair with number of rows

    shot_lst = [(0, 0)] * (max_shot_distance + 2)
    for index, row in df.iterrows():
        shot_distance = row['SHOT_DISTANCE']
        if shot_distance > max_shot_distance:
            shot_distance = max_shot_distance
        (num_made, num_attempted) = shot_lst[shot_distance]
        shot_lst[shot_distance] = (num_made + row['SHOT_MADE_FLAG'], num_attempted + 1)
    shot_lst[max_shot_distance + 1] = row['PLAYER_NAME']
    print(row['PLAYER_NAME'])
    return shot_lst


def write_shot_lst_array(player_ids):
        print (player_ids)
        lst_of_lsts = []
        for index in range (0, 50):
            print('test')
            shot_lst = get_player_shots_per_distance(player_ids[index])
            lst_of_lsts.append(shot_lst)

        fptr = open('Top_players_shot_distance_data.txt', 'wb')
        pickle.dump(lst_of_lsts, fptr)
        fptr.close()


def pts_per_fga_from_shot_lst(shot_lst):
    total_points = 0
    total_fga = 0
    for index in range(0, max_shot_distance):
        (shots_made, shots_attempted) = shot_lst[index]
        total_points = total_points + shots_made * (dunk_score + index * points_per_foot)
        total_fga = total_fga + shots_attempted
    return total_points / total_fga


# # Iterate over columns using DataFrame.iteritems()
# for (colname,colval) in df.iteritems():
# 	if (colname == "SHOT_DISTANCE"):
# 		print(colname, colval.values)

# for index, row in df.iterrows():

def list_of_top_players():
    # Here we access the leagueleaders module through endpoints & assign the class to "data"
    player_lst = []
    data = endpoints.leagueleaders.LeagueLeaders(
        league_id="00",
        per_mode48="PerGame",
        scope="S",
        season="2021-22",
        season_type_all_star="Regular Season",
        stat_category_abbreviation="PTS")

    # Our "data" variable now has built in functions such as creating a dataframe for our data
    df = data.league_leaders.get_data_frame()
    for index, row in df.iterrows():
        player_lst.append(row['PLAYER_ID'])
    print(player_lst)
    return player_lst


def get_shot_distance_data_from_file():
    fptr = open("Players_shot_distance_data.txt", "rb")  # open file in read binary mode
    test_list = pickle.load(fptr)  # read binary data from file and store in list
    fptr.close()
    return test_list

def get_top_players_pts_per_fga(test_list):
    list_players_pts_per_fga = []
    for row in test_list:
        list_players_pts_per_fga.append((pts_per_fga_from_shot_lst(row), row[max_shot_distance + 1]))
    list_players_pts_per_fga.sort(reverse=True)
    print(list_players_pts_per_fga)



# write_shot_lst_array([201935])
# get_shot_distance_data_from_file()
# get_player_pts_per_fga([201935])
write_shot_lst_array(list_of_top_players())
# get_top_players_pts_per_fga(get_shot_distance_data_from_file())