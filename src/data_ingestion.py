import zipfile
from pathlib import Path

import gdown

from src.Iterative_functions import mk_dir
from src.logger import get_logger

logger = get_logger(__name__)


class DataIngestion:
    def __init__(self, config):
        self.config = config
        self.data_ingestion = self.config.data_ingestion
        self.directories = self.config.directories
        self.files = self.config.files

    def download_unzip_file(self) -> str:
        data_ingestion = self.data_ingestion
        directories = self.directories
        files = self.files
        try:
            dataset_url = data_ingestion.source_url
            artifacts = directories.artifact_dir
            raw = directories.raw_dir
            zipfile_name = files.local_data_file

            artifact_dir = mk_dir(artifacts)
            # logger.info(f"Folder name {artifact_dir} was created")

            ROW_DIR = Path(artifacts) / raw
            raw_dir = mk_dir(ROW_DIR)
            # logger.info(f"Folder name {ROW_DIR} was created")

            logger.info(f"Downloading data from {dataset_url} into file {zipfile_name}")
            file_id = dataset_url.split("/")[-2]
            prefix = "https://drive.google.com/uc?/export=download&id="

            gdown.download(prefix + file_id, zipfile_name, quiet=False)
            logger.info(f"Downloaded data from {dataset_url} into file {zipfile}")

            logger.info(f"Unzipping data from {zipfile_name} into folder {ROW_DIR}")
            with zipfile.ZipFile(zipfile_name, "r") as zip_ref:
                zip_ref.extractall(ROW_DIR)
                logger.info(f"Extracted data into folder {ROW_DIR}")

        except Exception as e:
            logger.error(f"Error during file download or extraction: {e}")
