# Import the modules needed for the game
import pygame, sys, math, pygame.gfxdraw
from random import randint
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from numpy import array

# Set the width and height of the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Initialise Pygame and create the game window
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Target Shooter')

# Create a clock to control the game's frame rate
clock = pygame.time.Clock()

# Define the colours used throughout the game
RED = pygame.Color(220, 50, 50)
YELLOW = pygame.Color(255, 220, 0)
GREEN = pygame.Color(50, 200, 50)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

# Calculate the distance between two points
# Used to check whether the player has clicked a target
def getLength(vec):
    return (vec[0]**2 + vec[1]**2)**(0.5)


# Class responsible for creating and controlling each target
class Target():

    # Colours used to show the target's remaining health
    mainColours = [
        RED,
        YELLOW,
        GREEN
    ]

    # The colour used for the middle circle of the target
    secondaryColour = WHITE

    # Set up a new target when it is created
    def __init__(self):

        # Give the target a random movement speed and size
        self.speed = randint(2, 4)
        self.radius = randint(15, 25)

        # Choose a random starting position inside the window
        x = float(randint(self.radius, WINDOW_WIDTH - self.radius))
        y = float(randint(self.radius, WINDOW_HEIGHT - self.radius))

        # Store the target's position as an array
        self.pos = array((x, y))

        # Choose a random direction for the target to move
        angle = math.radians(randint(0, 360))

        # Calculate horizontal and vertical movement
        vx = self.speed * math.cos(angle)
        vy = self.speed * math.sin(angle)

        # Store the target's movement direction and speed
        self.vel = array((vx, vy))

        # Give each target three health points
        self.hp = 3

        # Set the starting colour based on its health
        self.mainColour = self.mainColours[self.hp - 1]

    # Draw the target on the screen
    def draw(self):

        # Convert the target's position and size to integers
        x, y = int(self.pos[0]), int(self.pos[1])
        r = int(self.radius)

        # Draw the filled outer circle and smooth its edges
        pygame.gfxdraw.filled_circle(
            DISPLAYSURF, x, y, r, self.mainColour
        )
        pygame.gfxdraw.aacircle(
            DISPLAYSURF, x, y, r, self.mainColour
        )

        # Draw the white middle circle
        pygame.gfxdraw.filled_circle(
            DISPLAYSURF, x, y, int(r * 2 / 3), self.secondaryColour
        )
        pygame.gfxdraw.aacircle(
            DISPLAYSURF, x, y, int(r * 2 / 3), self.secondaryColour
        )

        # Draw the smaller inner circle
        pygame.gfxdraw.filled_circle(
            DISPLAYSURF, x, y, max(1, int(r / 3)), self.mainColour
        )
        pygame.gfxdraw.aacircle(
            DISPLAYSURF, x, y, max(1, int(r / 3)), self.mainColour
        )

    # Move the target and check whether it hits a wall
    def update(self):
        self.wallBounce()
        self.pos += self.vel

    # Reverse the target's direction when it reaches a wall
    def wallBounce(self):

        # Reverse horizontal movement at the left or right wall
        if self.pos[0] < self.radius or self.pos[0] > WINDOW_WIDTH - self.radius:
            self.vel[0] *= -1

        # Reverse vertical movement at the top or bottom wall
        if self.pos[1] < self.radius or self.pos[1] > WINDOW_HEIGHT - self.radius:
            self.vel[1] *= -1

    # Check whether the player's click hits this target
    def didClick(self, loc):
        return getLength(loc - self.pos) <= self.radius

    # Remove one health point when the target is hit
    def onClick(self):
        self.hp -= 1

        # Change the target's colour to represent its remaining health
        self.mainColour = self.mainColours[self.hp - 1]


# Class responsible for displaying text on the screen
class Text():

    # Set up the text, its position, size and colour
    def __init__(self, text, pos, size=30, colour=BLACK):
        self.fontSize = size
        self.fontColour = colour
        self.pos = pos

        # Create the font used to display the text
        self.font = pygame.font.Font(None, self.fontSize)

        # Render the initial text
        self.update(text)

    # Display the text at its assigned position
    def draw(self):
        DISPLAYSURF.blit(self.renderedText, self.rect)

    # Update the text and recreate its rendered image
    def update(self, text):
        self.text = text
        self.renderedText = self.font.render(
            self.text, True, self.fontColour
        )

        # Position the text using its top-left corner
        self.rect = self.renderedText.get_rect()
        self.rect.topleft = self.pos


# Class responsible for managing the main gameplay
class Main():

    # Number of targets created at the start of each game
    startingTargets = 10

    # Set up a new game
    def __init__(self):

        # Create a list containing ten new targets
        self.targets = [
            Target() for _ in range(self.startingTargets)
        ]

        # Create the counter showing how many targets remain
        self.scoreText = Text(
            f"Targets Remaining: {self.startingTargets}",
            (10, 10)
        )

    # Draw the gameplay screen
    def draw(self):

        # Clear the screen with a white background
        DISPLAYSURF.fill(WHITE)

        # Draw every target currently in the game
        for target in self.targets:
            target.draw()

        # Display the remaining-target counter
        self.scoreText.draw()

    # Update the targets and the counter
    def update(self):

        # Move every target
        for target in self.targets:
            target.update()

        # Update the number of targets remaining
        self.scoreText.update(
            f"Targets Remaining: {len(self.targets)}"
        )

# Define the different screens in the game
MENU = "menu"
PLAYING = "playing"
INSTRUCTIONS = "instructions"
GAME_OVER = "game_over"

# Start the game on the main menu
gameState = MENU

# No gameplay object exists until the player starts a game
main = None


# Define colours used for the menu and buttons
DARK = pygame.Color(18, 25, 40)
BUTTON_COLOUR = pygame.Color(40, 55, 80)
BUTTON_HOVER = pygame.Color(55, 100, 180)
ACCENT = pygame.Color(70, 150, 255)

# Create fonts for the title, buttons and smaller text
titleFont = pygame.font.SysFont("arial", 56, bold=True)
buttonFont = pygame.font.SysFont("arial", 25)
smallFont = pygame.font.SysFont("arial", 20)


# Display text at a specified centre position
def drawText(text, font, colour, centre):

    # Render the text with anti-aliasing enabled
    surface = font.render(text, True, colour)

    # Centre the text at the requested position
    rect = surface.get_rect(center=centre)

    # Draw the text onto the game window
    DISPLAYSURF.blit(surface, rect)


# Draw a button and change its colour when the mouse hovers over it
def drawButton(text, rect, mousePos):

    # Highlight the button when the mouse is over it
    colour = (
        BUTTON_HOVER
        if rect.collidepoint(mousePos)
        else BUTTON_COLOUR
    )

    # Draw the button's background with rounded corners
    pygame.draw.rect(
        DISPLAYSURF, colour, rect, border_radius=12
    )

    # Draw an outline around the button
    pygame.draw.rect(
        DISPLAYSURF, ACCENT, rect, 2, border_radius=12
    )

    # Display the button's label in the centre
    drawText(text, buttonFont, WHITE, rect.center)


# Display the main menu and return the button positions
def drawMenu():

    # Set the menu background colour
    DISPLAYSURF.fill(DARK)

    # Get the current position of the mouse
    mousePos = pygame.mouse.get_pos()

    # Display the game title
    drawText(
        "TARGET SHOOTER",
        titleFont,
        WHITE,
        (WINDOW_WIDTH // 2, 150)
    )

    # Display a short description underneath the title
    drawText(
        "Test your aim. Hit every target.",
        smallFont,
        pygame.Color(180, 195, 215),
        (WINDOW_WIDTH // 2, 205)
    )

    # Create rectangles defining each button's position and size
    buttons = {
        "play": pygame.Rect(275, 275, 250, 55),
        "instructions": pygame.Rect(275, 350, 250, 55),
        "quit": pygame.Rect(275, 425, 250, 55)
    }

    # Draw each menu button
    drawButton("PLAY GAME", buttons["play"], mousePos)
    drawButton("HOW TO PLAY", buttons["instructions"], mousePos)
    drawButton("QUIT GAME", buttons["quit"], mousePos)

    # Return the buttons so the main loop can detect clicks
    return buttons


# Display the instructions screen
def drawInstructions():

    # Set the background colour
    DISPLAYSURF.fill(DARK)

    # Display the instructions heading
    drawText(
        "HOW TO PLAY",
        titleFont,
        WHITE,
        (WINDOW_WIDTH // 2, 140)
    )

    # Store the instructions in a list
    instructions = [
        "Click on a target to damage it.",
        "Each target requires three hits.",
        "Targets move and bounce off the walls.",
        "Destroy all targets to win!"
    ]

    # Display each instruction on a separate line
    for i, line in enumerate(instructions):
        drawText(
            line,
            smallFont,
            WHITE,
            (WINDOW_WIDTH // 2, 245 + i * 45)
        )

    # Create and draw the back button
    backButton = pygame.Rect(275, 450, 250, 55)
    drawButton(
        "BACK TO MENU",
        backButton,
        pygame.mouse.get_pos()
    )

    # Return the button so the main loop can detect clicks
    return backButton


# Display the victory screen when all targets are destroyed
def drawGameOver():

    # Set the background colour
    DISPLAYSURF.fill(DARK)

    # Display the victory message in green
    drawText(
        "YOU WIN!",
        titleFont,
        pygame.Color(80, 220, 120),
        (WINDOW_WIDTH // 2, 200)
    )

    # Display a message underneath the heading
    drawText(
        "All targets destroyed.",
        smallFont,
        WHITE,
        (WINDOW_WIDTH // 2, 270)
    )

    # Create the Play Again and Main Menu buttons
    buttons = {
        "play": pygame.Rect(275, 340, 250, 55),
        "menu": pygame.Rect(275, 415, 250, 55)
    }

    # Draw both buttons
    drawButton(
        "PLAY AGAIN",
        buttons["play"],
        pygame.mouse.get_pos()
    )
    drawButton(
        "MAIN MENU",
        buttons["menu"],
        pygame.mouse.get_pos()
    )

    # Return the buttons so the main loop can detect clicks
    return buttons


# Main game loop: runs continuously until the player quits
while True:

    # Reset the click flag at the start of each frame
    mouseClicked = False

    # Get the mouse's current position
    mousePos = pygame.mouse.get_pos()

    # Process events such as closing the window or clicking
    for event in pygame.event.get():

        # Close Pygame and exit the program
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Register left mouse-button clicks
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouseClicked = True
            mousePos = event.pos

    # MAIN MENU: display the menu and process button clicks
    if gameState == MENU:

        # Draw the menu and get its button positions
        buttons = drawMenu()

        # Only check buttons when the player clicks
        if mouseClicked:

            # Start a new game
            if buttons["play"].collidepoint(mousePos):
                main = Main()
                gameState = PLAYING

            # Open the instructions screen
            elif buttons["instructions"].collidepoint(mousePos):
                gameState = INSTRUCTIONS

            # Quit the game
            elif buttons["quit"].collidepoint(mousePos):
                pygame.quit()
                sys.exit()

    # INSTRUCTIONS: display the instructions and back button
    elif gameState == INSTRUCTIONS:

        # Draw the instructions screen
        backButton = drawInstructions()

        # Return to the main menu when the back button is clicked
        if mouseClicked and backButton.collidepoint(mousePos):
            gameState = MENU

    # PLAYING: run the actual target-shooting game
    elif gameState == PLAYING:

        # Move targets and update the remaining-target counter
        main.update()

        # Check whether the player clicked during this frame
        if mouseClicked:

            # Convert the mouse position into an array
            loc = array(mousePos)

            # Check whether the click hits any target
            for target in main.targets:

                if target.didClick(loc):

                    # Destroy the target if only one health point remains
                    if target.hp == 1:
                        main.targets.remove(target)

                    # Otherwise, damage the target
                    else:
                        target.onClick()

                    # Stop checking after the first target is hit
                    break

        # Draw the updated gameplay screen
        main.draw()

        # Switch to the victory screen when no targets remain
        if len(main.targets) == 0:
            gameState = GAME_OVER

    # GAME OVER: display the victory screen and its buttons
    elif gameState == GAME_OVER:

        # Draw the victory screen
        buttons = drawGameOver()

        # Check whether the player clicks a button
        if mouseClicked:

            # Start a fresh game with ten new targets
            if buttons["play"].collidepoint(mousePos):
                main = Main()
                gameState = PLAYING

            # Return to the main menu
            elif buttons["menu"].collidepoint(mousePos):
                gameState = MENU

    # Update the display so the latest frame becomes visible
    pygame.display.flip()

    # Limit the game to 60 frames per second
    clock.tick(60)