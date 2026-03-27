from src.components.data_ingestion import DataIngestion
from src.components.model_trainer import ModelTrainer

def run_training_pipeline():
    print(" Starting Training Pipeline...")

    # step 1: Data Ingestion
    ingestion = DataIngestion()
    train_path, test_path = ingestion.initiate_data_ingestion()

    # step 2: Model Training
    trainer = ModelTrainer()
    trainer.initiate_model_training()

    print("Training Pipeline Completed")

if __name__ == "__main__":
    run_training_pipeline()