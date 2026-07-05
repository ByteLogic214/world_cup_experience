import pandera as pa
from pandera import Column, DataFrameSchema

match_schema = DataFrameSchema(
    {
        "match_id": Column(str, nullable=False),
        "date": Column(str, nullable=False),
        "competition": Column(str, nullable=False),
        "home_team": Column(str, nullable=False),
        "away_team": Column(str, nullable=False),
        "home_goals": Column(int, nullable=False),
        "away_goals": Column(int, nullable=False),
        "venue": Column(str, nullable=True),
        "status": Column(str, nullable=False),
        "source": Column(str, nullable=False),
    }
)
