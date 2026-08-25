import great_expectations as gx
from src_production_deployment.logger.logging import setup_logging
log = setup_logging()
from src_production_deployment.configs.schema import SALES_SCHEMA, CALENDAR_SCHEMA , SELL_PRICES_SCHEMA
import pandas as pd
from src_production_deployment.data_ingestion_processing.validation.validation_report import ValidationReport

class GXValidator:

    def validate (self,df:pd.DataFrame, dataset_name:str,report:ValidationReport)-> None:
        """GX Validation"""

        SCHEMA = { "sales" : SALES_SCHEMA,
                   "calendar" : CALENDAR_SCHEMA,
                   "price" : SELL_PRICES_SCHEMA
                 }

        schema = SCHEMA[dataset_name]

        results = []    

        gx_df = gx.dataset.PandasDataset(df)

        all_success = True

        # -------------------------
        # Common Validations
        # -------------------------

        required_columns = SCHEMA[dataset_name]["required_columns"]
        column_types = SCHEMA[dataset_name]["column_types"]

        non_nullable_columns = schema.get("non_nullable_columns",[])
        non_negative_columns = schema.get("non_negative_columns", [])

        for column in required_columns:

            # results.append(gx_df.expect_column_to_exist(column)) # schema expectation # already have this so removing
            results.append(gx_df.expect_column_values_to_be_of_type(column, column_types[column])) # Data type expectation

            # Missing Value Validation
            if column in non_nullable_columns:
                results.append(gx_df.expect_column_values_to_not_be_null(column)) # missing value expectation

            # Non-negative Validation
            if column in non_negative_columns:
                results.append(gx_df.expect_column_values_to_be_between(column,min_value=0))

        # -------------------------
        # Prefix-based Validations
        # (Sales d_* columns)
        # --------

        if "non_negative_prefixes" in schema:

            prefix = schema["non_negative_prefixes"]

            sales_columns = [c for c in df.columns if c.startswith(prefix) ]

            for column in sales_columns:

                results.append(gx_df.expect_column_values_to_be_between(column, min_value=0))

 

        # -------------------------
        # Process Results
        # -------------------------

        for result in results:

            if not result["success"]:

                all_success = False

                column = result["expectation_config"]["kwargs"]["column"]
                expectation = result["expectation_config"]["expectation_type"]

                report.add_errors(
                                    f"[{dataset_name}] "
                                    f"Column '{column}' failed "
                                    f"expectation '{expectation}'."
                                )

        if all_success:
            report.add_infm(
                            f"[{dataset_name}] Great Expectations validation passed."
                            )


''' 
   Validation	                 GX Expectation	                         Needed?
Column exists	                expect_column_to_exist()	             ❌ Already handled by SchemaValidator
No NULLs	                 expect_column_values_to_not_be_null()	           ✅
Correct datatype	         expect_column_values_to_be_of_type()	          ✅
Unique ID	                 expect_column_values_to_be_unique("id")	       ✅
Sales values >= 0	          expect_column_values_to_be_between()	            ✅
'''



