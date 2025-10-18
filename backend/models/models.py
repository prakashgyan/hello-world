from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

DATABASE_URL = "sqlite:///./flashcards.db"

Base = declarative_base()

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    meanings = relationship("Meaning", back_populates="word")
    card = relationship("Card", uselist=False, back_populates="word")

class Meaning(Base):
    __tablename__ = "meanings"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    word_id = Column(Integer, ForeignKey("words.id"))
    word = relationship("Word", back_populates="meanings")

class AnswerLog(Base):
    __tablename__ = "answer_logs"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    quality = Column(Integer)
    card = relationship("Card", back_populates="answer_logs")


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), unique=True)
    due_date = Column(DateTime, default=datetime.datetime.utcnow)
    interval = Column(Integer, default=1)
    ease_factor = Column(Float, default=2.5)
    repetitions = Column(Integer, default=0)
    word = relationship("Word", back_populates="card")
    answer_logs = relationship("AnswerLog", back_populates="card")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db():
    Base.metadata.create_all(bind=engine)
