from sqlalchemy import Column, Integer, String, BigInteger, JSON, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Trunk(Base):
    __tablename__ = 'vats'
    id = Column(Integer, primary_key=True)
    provider = Column(String(20))
    obj = Column(String(30))
    trunk_username = Column(String(20))
    trunk_password = Column(String(20))
    phone = Column(String(20))
    active = Column(Boolean)
    attributes = Column(JSON)
    lines = Column(Integer)
    updated = Column(DateTime)

    def __init__(self, provider, obj, trunk_username, trunk_password, phone, active, updated, lines, attributes=None):
        self.provider = provider
        self.obj = obj
        self.trunk_username = trunk_username
        self.trunk_password = trunk_password
        self.phone = phone
        self.active = active
        self.attributes = attributes
        self.lines = lines
        self.updated = updated
