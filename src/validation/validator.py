import pandas as pd
from src.validation.schemas import match_schema
from src.utils.logger import get_logger

logger = get_logger()


class DataValidator:

    def validate_schema(self, df: pd.DataFrame):
        logger.info("Validating schema...")

        try:
            match_schema.validate(df, lazy=True)
        except Exception as e:
            logger.error(f"Schema validation failed: {e}")
            raise

        logger.info("Schema validation passed")
        return True

    def validate_no_duplicates(self, df: pd.DataFrame):
        logger.info("Checking duplicates...")

        if df["match_id"].duplicated().any():
            raise ValueError("Duplicate match_id detected")

        logger.info("No duplicates found")
        return True

    def validate_goals(self, df: pd.DataFrame):
        logger.info("Validating goals...")

        if (df["home_goals"] < 0).any() or (df["away_goals"] < 0).any():
            raise ValueError("Negative goals detected")

        return True

    def validate_teams(self, df: pd.DataFrame):
        logger.info("Validating teams consistency...")

        if df["home_team"].isna().any() or df["away_team"].isna().any():
            raise ValueError("Missing team names detected")

        return True

    def run_all(self, df: pd.DataFrame):
        logger.info("Running full validation pipeline...")

        self.validate_schema(df)
        self.validate_no_duplicates(df)
        self.validate_goals(df)
        self.validate_teams(df)

        logger.info("ALL VALIDATIONS PASSED")
        return df
