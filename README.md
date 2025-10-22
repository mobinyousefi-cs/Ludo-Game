# Ludo Game (Tkinter + Pillow)

A polished, extensible Ludo implementation in Python with a Tkinter GUI and optional computer players. Follows a clean `src/` layout, comes with tests, and is MIT-licensed.

## Features
- 2–4 players (any mix of human and simple AI)
- Classic Ludo rules: roll 6 to enter, extra turn on 6, captures send tokens back to yard
- Smooth Canvas rendering with scalable board
- Keyboard shortcuts and accessible buttons
- Deterministic mode for testing

## Project Layout
```
.
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── .editorconfig
├── .gitignore
├── src/
│   └── ludo/
│       ├── __init__.py
│       ├── main.py
│       ├── ui.py
│       ├── game.py
│       ├── board.py
│       ├── dice.py
│       ├── player.py
│       ├── constants.py
│       └── utils.py
└── tests/
    └── test_imports.py
```

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -U pip
pip install -e .  # or: pip install -r requirements.txt
python -m ludo
```

### Run tests
```bash
pytest -q
```

## How to Play
- Choose number of players (2–4) and which are human/AI.
- Click **Roll** or press `r` to roll the die. If you roll a 6 and have tokens in the yard, one may enter.
- Click a highlighted token to move. The UI enforces legal moves.
- First to move all 4 tokens to **Home** wins.

## Notes
- Pillow (PIL) is used to render crisp dice images; the board is drawn vectorially with Tkinter Canvas.
- The code is modular and ready for your future enhancements (smarter AI, sounds, network play, etc.).

## License
MIT — see [LICENSE](LICENSE).

