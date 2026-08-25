from io import BytesIO
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from src_production_deployment.logger.logging import setup_logging
log = setup_logging()

class DataLakeReader:
    """ Reads files from Azure Data Lake"""
    def __init__(self, account_name:str, filesystem:str) -> None:

        log.info("Initializing DataLakeReader")
        
        try:
            self.account_name = account_name
            self.filesystem = filesystem
            self.credential = DefaultAzureCredential()
            self.service = DataLakeServiceClient(
                        account_url=(
                        f"https://"
                        f"{account_name}"
                        ".dfs.core.windows.net"),
                    credential=self.credential
                )
            self.fs = (self.service.get_file_system_client(file_system = filesystem))

            log.info("DataLakeReader initialized successfully")

        except Exception:
            log.exception("Failed to initialize Azure Data Lake connection.")
            raise

    
    def read_file(self,path:str) -> BytesIO:
        """ Download file to memeory"""
        try:

            file_client = self.fs.get_file_client(path)
            data = file_client.download_file().readall()

            return BytesIO(data)
        
        except Exception:
            log.exception(f"Reading the file failed for path {path}")
            raise
        


