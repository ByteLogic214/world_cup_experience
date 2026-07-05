import pandas as pd


def rolling_form(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values("date")

    df["home_points_last5"] = 0
    df["away_points_last5"] = 0
    df["home_goal_diff_last5"] = 0
    df["away_goal_diff_last5"] = 0

    teams = pd.unique(df[["home_team", "away_team"]].values.ravel())

    for team in teams:
        team_matches = df[(df["home_team"] == team) | (df["away_team"] == team)]

        points = []
        goal_diff = []

        for _, row in team_matches.iterrows():
            if row["home_team"] == team:
                points.append(3 if row["home_goals"] > row["away_goals"] else 1 if row["home_goals"] == row["away_goals"] else 0)
                goal_diff.append(row["home_goals"] - row["away_goals"])
            else:
                points.append(3 if row["away_goals"] > row["home_goals"] else 1 if row["away_goals"] == row["home_goals"] else 0)
                goal_diff.append(row["away_goals"] - row["home_goals"])

        for i in range(len(team_matches)):
            idx = team_matches.index[i]

            df.loc[idx, "home_points_last5"] = sum(points[max(0, i-window):i])
            df.loc[idx, "away_points_last5"] = sum(points[max(0, i-window):i])
            df.loc[idx, "home_goal_diff_last5"] = sum(goal_diff[max(0, i-window):i])
            df.loc[idx, "away_goal_diff_last5"] = sum(goal_diff[max(0, i-window):i])

    return df
