from src.features.elo_features import compute_elo_difference
from src.features.form_features import rolling_form
from src.features.match_features import compute_match_features
from src.features.rest_features import compute_rest_days
from src.utils.logger import get_logger

logger = get_logger()


class GoldBuilder:

    def build(self, df):

        logger.info("Building Gold dataset...")

        df = compute_elo_difference(df)

        df = compute_match_features(df)

        df = compute_rest_days(df)

        df = rolling_form(df)

        logger.info(f"Gold dataset ready: {len(df)} rows")

        return df
