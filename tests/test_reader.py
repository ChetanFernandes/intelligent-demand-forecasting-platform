from src_production_deployment.ingestion.blob_reader_initialization import DataLakeReader
reader = DataLakeReader(account_name="stdemandforecastingdev", filesystem="demand-forecasting")
print("Reader_Initialized")

