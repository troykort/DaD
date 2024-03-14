from pathlib import Path
from loguru import logger

class Settings():
    basedir=Path.cwd()
    rawdir=Path("Raw_data")
    processeddir=Path("processed_data")
    logdir= basedir/"log"

    house_Activity_colums= [
        "hier all attributes inzetten in de script.py file"
    ]

    settings = Settings()
    logger.add("logfile.log")
    
