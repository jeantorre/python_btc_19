from datetime import datetime

from pytz import timezone
from sqlalchemy import Column, DateTime, Float, Integer, String

from db import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco = Column(Float)
    em_oferta = Column(String, nullable=True)
    ultima_alteracao = Column(
        DateTime, default=lambda: datetime.now(timezone("America/Sao_Paulo"))
    )
