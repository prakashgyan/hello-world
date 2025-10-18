from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import json
import datetime

from backend.models.models import Word, Meaning, Card, AnswerLog, SessionLocal, create_db
from backend.schemas import WordSchema, CardSchema, AnswerSchema, StatsSchema
from backend.srs import update_card

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    create_db()


@app.post("/upload")
async def upload_word_list(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JSON file.")

    contents = await file.read()
    data = json.loads(contents)

    new_words = []
    for item in data:
        word_text = item.get("word")
        meanings_text = item.get("meanings")

        if not word_text or not meanings_text:
            continue

        # Check if the word already exists
        db_word = db.query(Word).filter(Word.text == word_text).first()
        if not db_word:
            db_word = Word(text=word_text)
            db.add(db_word)

            # Add meanings
            for meaning_text in meanings_text:
                db_meaning = Meaning(text=meaning_text, word=db_word)
                db.add(db_meaning)

            # Create a card for the new word
            db_card = Card(word=db_word)
            db.add(db_card)

    db.commit()

    return {"message": "Word list uploaded successfully"}


@app.get("/next-card", response_model=CardSchema)
def get_next_card(db: Session = Depends(get_db)):
    now = datetime.datetime.utcnow()
    card = db.query(Card).filter(Card.due_date <= now).order_by(Card.due_date).first()
    if not card:
        raise HTTPException(status_code=404, detail="No cards due for review.")

    return {
        "word": card.word.text,
        "meanings": [meaning.text for meaning in card.word.meanings],
        "due_date": card.due_date.isoformat(),
        "card_id": card.id
    }


@app.post("/answer")
def submit_answer(answer: AnswerSchema, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == answer.card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found.")

    # Log the answer
    answer_log = AnswerLog(card_id=card.id, quality=answer.quality)
    db.add(answer_log)

    update_card(card, answer.quality)
    db.commit()

    return {"message": "Answer submitted successfully."}


@app.get("/stats", response_model=StatsSchema)
def get_stats(db: Session = Depends(get_db)):
    total_words = db.query(Word).count()

    # Calculate correct percentage
    total_answers = db.query(AnswerLog).count()
    if total_answers > 0:
        correct_answers = db.query(AnswerLog).filter(AnswerLog.quality >= 3).count()
        correct_percentage = (correct_answers / total_answers) * 100
    else:
        correct_percentage = 0.0

    # Calculate trend
    today = datetime.datetime.utcnow().date()
    yesterday = today - datetime.timedelta(days=1)

    today_answers = db.query(AnswerLog).filter(func.date(AnswerLog.timestamp) == today).count()
    yesterday_answers = db.query(AnswerLog).filter(func.date(AnswerLog.timestamp) == yesterday).count()

    if today_answers > yesterday_answers:
        trend = "increasing"
    elif today_answers < yesterday_answers:
        trend = "decreasing"
    else:
        trend = "steady"

    return {
        "total_words": total_words,
        "correct_percentage": correct_percentage,
        "trend": trend,
    }
