from pathlib import Path
from loguru import logger

class Settings():
    basedir=Path.cwd()
    rawdir=Path("Raw_data")
    processeddir=Path("processed_data")
    logdir= basedir/ "log"

    colums= [

    ]

    settings = Settings()
    logger.add(settings.logdir / "logfile.log")
    logger.info("voorbeeld logbericht")
    
