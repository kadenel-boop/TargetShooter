# Target Shooter

## About the Project

Target Shooter is a 2D target-shooting game developed using Python and Pygame for the Creative Coding A2 assessment at the University of Technology Sydney (UTS).

The project was developed using James Clark's Pygame Target Shooter tutorial as a starting point. I expanded the original concept by implementing additional features, including a main menu, instructions screen, target health system, changing target colours, moving targets and a victory screen.

The project demonstrates my developing understanding of Python programming, object-oriented programming, event-driven programming, variables, functions, conditionals, loops, testing and debugging.

## Game Features

- **Main Menu:** Provides options to play, view instructions or quit the game.
- **Instructions Screen:** Explains the game mechanics.
- **Target Shooting:** Players use the mouse to shoot targets.
- **Target Health System:** Each target requires three hits to be destroyed.
- **Traffic Light Colour System:** Targets change from green to yellow to red as their health decreases.
- **Moving Targets:** Targets move around the game window and bounce off its boundaries.
- **Remaining Target Counter:** Displays how many targets are left to destroy.
- **Victory Screen:** Appears when all targets have been destroyed.
- **Play Again Option:** Allows the player to start a new game.
- **Main Menu Navigation:** Allows the player to return to the main menu.

## Controls

| Control | Action |
|---|---|
| Left Mouse Button | Shoot targets |
| Play Game button | Start a new game |
| How to Play button | Open the instructions |
| Back to Menu button | Return to the main menu |
| Play Again button | Restart the game |
| Main Menu button | Return to the main menu |
| Quit Game button | Close the game |

## Technologies Used

- Python
- Pygame
- NumPy
- Visual Studio Code

## Installation and Setup

### Requirements

- Python 3
- Pygame
- NumPy

### Installation Instructions

1. Download or clone this repository.
2. Ensure Python 3 is installed.
3. Open a terminal in the project directory.
4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Run the game using:

```bash
python main.py
```

The game will open in an 800 × 600 window.

## Project Structure

```text
TargetShooter/
├── main.py
├── README.md
└── requirements.txt
```

### File Descriptions

- `main.py` — Contains the game logic, target classes, interface screens, event handling and main game loop.
- `requirements.txt` — Lists the external Python libraries required to run the game.
- `README.md` — Provides project information, controls and installation instructions.

## Development Process

The project was developed through tutorial-based learning, experimentation and repeated testing.

The original tutorial provided a foundation for understanding Pygame. I expanded the project by creating additional screens, implementing target health and colour changes, adding target movement and improving the overall user interface.

Throughout development, I encountered technical challenges involving Python and Pygame compatibility, understanding code structure and the importance of correct Python syntax and capitalisation.

The project helped me develop my programming skills and confidence in using code as a creative tool.

## References

Clark, J. (n.d.). *Pygame target shooter tutorial* [Video]. YouTube. https://www.youtube.com/watch?v=KUOYyJFTFnQ

Pygame. (n.d.). *Pygame documentation*. https://www.pygame.org/docs/

NumPy. (n.d.). *NumPy documentation*. https://numpy.org/doc/

## Assessment Information

**Unit:** Creative Coding  
**Assessment:** Assessment 2 — Target Shooter  
**Institution:** University of Technology Sydney (UTS)
