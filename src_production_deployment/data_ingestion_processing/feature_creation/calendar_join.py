from src_production_deployment.logger.logging import setup_logging
log = setup_logging()
import pandas as pd

class CalendarJoiner:
    def transform(self, df:pd.DataFrame,calendar_df:pd.DataFrame) -> pd.DataFrame:
        try:

            merged = df.merge(calendar_df,left_on = "day", right_on = "d",how = "left")
            return merged

        except Exception:
            log.exception("Error occured while joing sales_price_validation and calendar file")
            raise