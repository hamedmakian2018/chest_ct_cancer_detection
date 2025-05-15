import zipfile
from pathlib import Path

import gdown

from src.config_entity import DataIngestionConfig
from src.config_reader import read_config
from src.Iterative_functions import mk_dir
from src.logger import get_logger

logger = get_logger(__name__)


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.data_ingestion = config.data_ingestion

    def download_unzip_file(self) -> str:
        data_ingestion = self.data_ingestion
        try:
            dataset_url = data_ingestion.source_url
            artifacts = data_ingestion.artifact_dir
            raw = data_ingestion.raw_dir
            zipfile_name = data_ingestion.local_data_file

            artifact_dir = mk_dir(artifacts)
            logger.info(f"Folder name {artifact_dir} was created")

            ROW_DIR = Path(artifacts) / raw
            raw_dir = mk_dir(ROW_DIR)
            logger.info(f"Folder name {ROW_DIR} was created")

            zip_path = ROW_DIR / zipfile_name
            logger.info(f"Downloading data from {dataset_url} into file {ROW_DIR}")
            file_id = dataset_url.split("/")[-2]
            prefix = "https://drive.google.com/uc?/export=download&id="

            gdown.download(prefix + file_id, str(zip_path), quiet=False)
            logger.info(f"Downloaded data from {dataset_url} into file {zipfile}")

            logger.info(f"Unzipping data from {zip_path} into folder {ROW_DIR}")
            with zipfile.ZipFile(str(zip_path), "r") as zip_ref:
                zip_ref.extractall(ROW_DIR)
                logger.info(f"Extracted data into folder {ROW_DIR}")

        except Exception as e:
            logger.error(f"Error during file download or extraction: {e}")
