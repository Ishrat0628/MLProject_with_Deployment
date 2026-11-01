import os
import sys
from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


class TrainPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):
        try:
            logging.info(">>>>> Starting Data Ingestion <<<<<")
            data_ingestion = DataIngestion()
            train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed: train={train_data_path}, test={test_data_path}")

            logging.info(">>>>> Starting Data Transformation <<<<<")
            data_transformation = DataTransformation()
            train_arr, test_arr, preprocessor_path = data_transformation.initiate_data_transformation(
                train_path=train_data_path,
                test_path=test_data_path
            )
            logging.info(f"Data Transformation completed: preprocessor saved at {preprocessor_path}")

            logging.info(">>>>> Starting Model Trainer <<<<<")
            model_trainer = ModelTrainer()
            r2_square = model_trainer.initiate_model_trainer(
                train_array=train_arr,
                test_array=test_arr
            )
            logging.info(f">>>>> Model Training Pipeline Completed. Best Model R2 Score: {r2_square} <<<<<")
            return r2_square

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        pipeline = TrainPipeline()
        r2_score_result = pipeline.run_pipeline()
        print(f"Training Pipeline completed successfully! Best Model R2 Score: {r2_score_result}")
    except Exception as e:
        print(f"Error during training pipeline: {e}")
        sys.exit(1)

