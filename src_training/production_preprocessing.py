from src_production_deployment.data_ingestion_processing.main import DataLoader
from src_production_deployment.data_ingestion_processing.validation.schema import ValidationError
from configs.project_config import AZURE_ACCOUNT_NAME , AZURE_FILESYSTEM
from src_production_deployment.data_ingestion_processing.validation.validation_report import ValidationReport
from logger.logging import setup_logging
log = setup_logging()


# Data Loading

try:

    loader = DataLoader(account_name = AZURE_ACCOUNT_NAME, filesystem = AZURE_FILESYSTEM)

except Exception:
    log.exception("Application startup failed.")
    raise

# Data Validation
try:
    
    report = ValidationReport()
    
    loader.data_validation(report) 

    report_path = report.save_report_first_validation() # Python automatically converts this into: ValidationReport.save_report(report) . The object report is automatically passed as the first argument, which is called self.
    
    if report.has_errors():


        log.warning(f"Initial validation found issues. "
                    f"Report saved at: {report_path}"
                    )


        # Try to fix the issues
        loader.data_preprocessing()

        # Re-validation
        
        loader.data_validation(report)

        report_path = report.save_report_re_validation()

        if report.has_errors():

            raise ValidationError(
                f"Validation failed after preprocessing. "
                f"Report saved at: {report_path}"
            )

        else:
            log.info("No errors reported during second validation.Proceeding with Data Massage")
            pass


    else:
        log.info("No errors reported during first validation.Proceeding with Data Massage")
        pass

except ValidationError as e:
    log.error(e)
    raise

except Exception:
    log.exception("Unexpected error during validation")
    raise


# Data massaging (Temporal Feature Engineering Pipeline)

try:

    featured = loader.data_massaging() #Joining Sales, calendar and sell price

    log.info("Data massaging completed successfully")
    
except Exception:
    log.exception("Error occured during data massaging")
    raise


# Drop unwanted or redundancy columns

try:

    final_infrence_dataset = loader.prepare_inference_features(featured)

    log.info(f"{final_infrence_dataset.dtypes}")

    X_inference = final_infrence_dataset.drop(columns = ["sales"]).reset_index(drop = True)

    Y_inference = final_infrence_dataset[["sales"]]

    log.info("X_inference_shape :%s", X_inference.shape)

    log.info("Y_inference_shape :%s", Y_inference.shape)

    X_inference.to_parquet("artifacts/production/X_inference.parquet", index = False)

    Y_inference.to_parquet("artifacts/production/Y_inference.parquet", index = False)

    log.info("Inference processing completed successfully")

except Exception:

    log.exception("Error occured during prepare_inference_features")

    raise









