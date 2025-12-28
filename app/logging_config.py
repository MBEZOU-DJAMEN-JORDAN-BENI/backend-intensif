import logging
import sys
from pathlib import Path

def setup_logging():
    # Creer un dossier logs
    Path("logs").mkdir(exist_ok=True)
    
    # Configuration du logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Console
            logging.StreamHandler(sys.stdout),
            # Fichier
            logging.FileHandler('logs/app.log', endcoding='utf-8')
        ]
    )
    # Logger pour SQLAlchemy (moins verbeux)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
   
    return logging.getLogger(__name__)
    
    