import pandas as pd
from src.utils.logger import get_logger

logger = get_logger()


class QualityReport:

    def generate(self, df: pd.DataFrame):

        report = {
            "rows": len(df),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": df.duplicated().sum(),
            "columns": list(df.columns),
        }

        logger.info(f"Quality Report: {report}")

        return report
