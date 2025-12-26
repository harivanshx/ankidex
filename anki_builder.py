"""
Anki Deck Builder Module
Creates Anki-compatible .apkg files using genanki
"""

import random
import genanki


# Define a custom model for our flashcards
FLASHCARD_MODEL = genanki.Model(
    random.randrange(1 << 30, 1 << 31),
    'AnkiDex Basic',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '''
                <div class="card question">
                    {{Question}}
                </div>
            ''',
            'afmt': '''
                <div class="card question">
                    {{Question}}
                </div>
                <hr id="answer">
                <div class="card answer">
                    {{Answer}}
                </div>
            ''',
        },
    ],
    css='''
        .card {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 20px;
            text-align: center;
            color: #333;
            background-color: #fafafa;
            padding: 20px;
            line-height: 1.5;
        }
        .question {
            font-weight: bold;
            color: #1a73e8;
        }
        .answer {
            color: #2e7d32;
        }
        hr#answer {
            border: none;
            border-top: 2px solid #ddd;
            margin: 20px 0;
        }
    '''
)


def create_deck(flashcards: list, deck_name: str = "AnkiDex Deck") -> genanki.Deck:
    """
    Create an Anki deck from flashcards.
    
    Args:
        flashcards: List of dicts with 'question' and 'answer' keys
        deck_name: Name for the Anki deck
        
    Returns:
        genanki.Deck object
    """
    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, deck_name)
    
    for card in flashcards:
        note = genanki.Note(
            model=FLASHCARD_MODEL,
            fields=[card['question'], card['answer']]
        )
        deck.add_note(note)
    
    return deck


def export_to_apkg(flashcards: list, output_path: str, deck_name: str = "AnkiDex Deck"):
    """
    Export flashcards to an Anki .apkg file.
    
    Args:
        flashcards: List of dicts with 'question' and 'answer' keys
        output_path: Path for the output .apkg file
        deck_name: Name for the Anki deck
    """
    deck = create_deck(flashcards, deck_name)
    package = genanki.Package(deck)
    package.write_to_file(output_path)


def export_to_bytes(flashcards: list, deck_name: str = "AnkiDex Deck") -> bytes:
    """
    Export flashcards to .apkg bytes (for web downloads).
    
    Args:
        flashcards: List of dicts with 'question' and 'answer' keys
        deck_name: Name for the Anki deck
        
    Returns:
        .apkg file content as bytes
    """
    import tempfile
    import os
    
    deck = create_deck(flashcards, deck_name)
    package = genanki.Package(deck)
    
    # Write to temp file and read bytes
    with tempfile.NamedTemporaryFile(suffix='.apkg', delete=False) as tmp:
        tmp_path = tmp.name
    
    package.write_to_file(tmp_path)
    
    with open(tmp_path, 'rb') as f:
        apkg_bytes = f.read()
    
    os.unlink(tmp_path)
    
    return apkg_bytes
