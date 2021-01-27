from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SimVats(Base):
    __tablename__ = 'vats'
    id = Column(Integer, primary_key=True)
    provider = Column(String(20))
    contract = Column(String(30))
    trank_login = Column(String(20))
    phone = Column(BigInteger)

    def __init__(self, provider, contract, trank_login, phone):
        self.provider = provider
        self.contract = contract
        self.trank_login = trank_login
        self.phone = phone