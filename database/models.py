# database/models.py
from sqlalchemy import Column, BigInteger, Text, Integer, TIMESTAMP, Float, ForeignKey
from sqlalchemy.sql import func
from database.engine import Base

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(BigInteger, primary_key=True)
    username = Column(Text, nullable=True, index=True)
    full_name = Column(Text, nullable=False)
    balance = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

class Donation(Base):
    __tablename__ = 'donations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_id = Column(Text, unique=True, nullable=False, index=True)
    status = Column(Text, nullable=False)
    method = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

class Valentine(Base):
    __tablename__ = 'valentines'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    recipient_username = Column(Text, nullable=False, index=True)
    message_text = Column(Text, nullable=False)
    delivery_slot = Column(Text, nullable=False, index=True)
    status = Column(Text, nullable=False, default='pending', index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())