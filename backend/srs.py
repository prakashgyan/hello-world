import datetime
from backend.models.models import Card

def update_card(card: Card, quality: int):
    """
    Update the card's review schedule based on the user's performance.
    This function implements a simplified version of the SM-2 algorithm.
    """
    if quality < 0 or quality > 5:
        raise ValueError("Quality must be an integer between 0 and 5.")

    if quality < 3:
        # If the answer was incorrect, reset the card.
        card.repetitions = 0
        card.interval = 1
    else:
        # Update the ease factor.
        ease_factor = card.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        if ease_factor < 1.3:
            ease_factor = 1.3
        card.ease_factor = ease_factor

        # Update the interval.
        if card.repetitions == 0:
            card.interval = 1
        elif card.repetitions == 1:
            card.interval = 6
        else:
            card.interval = round(card.interval * card.ease_factor)

        card.repetitions += 1

    # Update the due date.
    card.due_date = datetime.datetime.utcnow() + datetime.timedelta(days=card.interval)
