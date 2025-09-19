import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pymysql
import requests
conn = pymysql.connect(
            host='mydb.c1eg6mc4azh2.ap-south-1.rds.amazonaws.com',
            user='admin',
            password='kreupai123',
            database='kreupai',
        )
cursor = conn.cursor(pymysql.cursors.DictCursor)

# Use matchid to join and filter
query = """
    select * from teamid
"""
cursor.execute(query)
results = cursor.fetchall()
cursor.close()
conn.close()

# Build mapping for quick lookup
team_map = {item['teamname']: item['teamid'] for item in results}
team_names = list(team_map.keys())

# Select home team
home_team_name = st.selectbox("Select Home Team", team_names,index=None,placeholder="Select Home Team")

# Filter opponent list to exclude the home team
opponent_choices = [t for t in team_names if t != home_team_name]
opponent_team_name = st.selectbox("Select Opponent Team", opponent_choices,index=None,placeholder="Select Away Team")
if home_team_name and opponent_team_name:
    home_team_id = team_map[home_team_name]
    opponent_team_id = team_map[opponent_team_name]
    # st.write(f"Home team ID: {home_team_id}, Opponent team ID: {opponent_team_id}")
else:
    st.info("Please select both teams to continue.")

# Get IDs
home_team_id = team_map[home_team_name]
opponent_team_id = team_map[opponent_team_name]
url=f"http://fastapi-env.eba-nhjpadgm.ap-south-1.elasticbeanstalk.com/team_stats/{home_team_id}/{opponent_team_id}"
response=requests.get(url)
data=response.json()
# st.write(data)
loaded_gs_model = joblib.load('catboost_goals_scored_model.pkl')
loaded_gc_model = joblib.load('catboost_goals_conceded_model.pkl')
sample_input = np.array([[home_team_id, opponent_team_id, 1, data['team_avg_goals_last5'], data['team_avg_conceded_last5'],
                           data['team_home_goals_avg'], data['opponent_away_goals_avg'],
                           data['opponent_avg_conceded_last5'],data['opponent_avg_goals_last5']]])
predicted_goals_scored = loaded_gs_model.predict(sample_input)
predicted_goals_conceded = loaded_gc_model.predict(sample_input)
st.write(f"Predicted Goals For Home Team {home_team_name}: {round(predicted_goals_scored[0])}")
st.write(f"Predicted Goals For Away Team {opponent_team_name}: {round(predicted_goals_conceded[0])}")

# # Display selections
# st.write(f"Home Team: {home_team_name} (ID: {home_team_id})")
# st.write(f"Opponent Team: {opponent_team_name} (ID: {opponent_team_id})")




