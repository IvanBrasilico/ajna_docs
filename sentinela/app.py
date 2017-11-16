import logging
import os

from sentinela.models.models import (Base, Filtro, MySession, ParametroRisco,
                                     ValorParametro)
from sentinela.utils.csv_handlers import muda_titulos_csv
from sentinela.utils.gerente_risco import GerenteRisco

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


mysession = MySession(Base)
session = mysession.session
engine = mysession.engine


