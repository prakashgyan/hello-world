import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Card {
    word: string;
    meanings: string[];
    card_id: number;
}

const Flashcard: React.FC = () => {
    const [card, setCard] = useState<Card | null>(null);
    const [showAnswer, setShowAnswer] = useState(false);

    const fetchNextCard = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/next-card`);
            setCard(response.data);
            setShowAnswer(false);
        } catch (error) {
            console.error('Error fetching next card:', error);
            setCard(null);
        }
    };

    const handleAnswer = async (quality: number) => {
        if (!card) {
            return;
        }
        try {
            await axios.post(`${process.env.REACT_APP_API_URL}/answer`, {
                card_id: card.card_id,
                quality,
            });
            fetchNextCard();
        } catch (error) {
            console.error('Error submitting answer:', error);
        }
    };

    useEffect(() => {
        fetchNextCard();
    }, []);

    if (!card) {
        return <div>No cards to review.</div>;
    }

    return (
        <div>
            <h2>Flashcard</h2>
            <h3>{card.word}</h3>
            {showAnswer && (
                <ul>
                    {card.meanings.map((meaning, index) => (
                        <li key={index}>{meaning}</li>
                    ))}
                </ul>
            )}
            <button onClick={() => setShowAnswer(!showAnswer)}>
                {showAnswer ? 'Hide' : 'Show'} Answer
            </button>
            {showAnswer && (
                <div>
                    <button onClick={() => handleAnswer(5)}>Easy</button>
                    <button onClick={() => handleAnswer(3)}>Good</button>
                    <button onClick={() => handleAnswer(1)}>Hard</button>
                </div>
            )}
        </div>
    );
};

export default Flashcard;
