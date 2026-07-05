from src.preprocessing.clean_matches import clean_matches
from src.preprocessing.normalize_teams import apply_team_normalization
from src.preprocessing.merge_sources import merge_datasets
from src.utils.logger import get_logger

logger = get_logger()


class SilverBuilder:

    def build(self, datasets: list):

        logger.info("Building Silver dataset...")

        df = merge_datasets(datasets)

        df = clean_matches(df)

        df = apply_team_normalization(df)

        logger.info(f"Silver dataset ready: {len(df)} rows")

        return df
