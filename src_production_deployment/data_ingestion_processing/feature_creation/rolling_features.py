from src_production_deployment.logger.logging import setup_logging
log = setup_logging()
import pandas as pd

class RollingFeatureGenerator:
    def transform(self,df:pd.DataFrame) -> pd.DataFrame:
        try:


            #print("ID column tpe", df["id"].dtype)
            #print("Type of columns itemid", df["item_id"].dtype)
            
            df = df.sort_values(by = ["id","date"], kind="mergesort")

            grouped = df.groupby("id", observed = True)

            df["rolling_mean_7"] = grouped["sales"].transform(lambda x:x.shift(1).rolling(window=7).mean())
            df["rolling_mean_28"] = grouped["sales"].transform(lambda x:x.shift(1).rolling(window=28).mean())
            df["rolling_std_7"] = grouped["sales"].transform(lambda x: x.shift(1).rolling(window=7).std())

            return df
        
        except Exception:
            log.exception("Error while generating rolling mean")
            raise

''' 
VERY Important Line

This:

x.shift(1).rolling(7)

is CRITICAL.

Why shift BEFORE rolling?

Because otherwise:

current day's sales would leak into feature creation.

That causes: data leakage

One of the MOST important forecasting mistakes.

We are intentionally preventing leakage.

Important Interview Insight

If interviewer asks:

Why shift before rolling?

Strong answer:

To ensure rolling statistics use only past information and avoid target leakage from current observations.

Very strong AI Engineer answer.
''' 
''' 
Without observed=True
df.groupby("id", observed=False).size()

Output:

A    2
B    0
C    2
D    0
E    0
With observed=True
df.groupby("id", observed=True).size()

Output:

A    2
C    2

Only the observed categories are included.

Does it matter for your M5 project?

Most likely, your id column is an object (string) unless you've explicitly converted it:

df["id"] = df["id"].astype("category")

If id is an object (string), then:

grouped = df.groupby("id", observed=True)

and

grouped = df.groupby("id")

will produce the same result.

observed=True has essentially no effect for non-categorical columns.
'''