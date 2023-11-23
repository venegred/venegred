import sys
import pygame
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
Base = declarative_base()
# Initialize Pygame
pygame.init()

# Constants and game states
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (255, 255, 143)
RED = (255, 0, 0)
FONT_SIZE = 20
FONT = pygame.font.SysFont("Arial", FONT_SIZE)

MAIN_MENU = 0
GAME_PLAYING = 1

current_state = MAIN_MENU

python_code_snippets = [
    "\nprint('Hello, World!')",
    "\na = 5\nb = 3\nsum = a + b\nproduct = a * b\nprint('Sum:', sum)\nprint('Product:', product)",
    "\nname = input('Enter your name: ')\nprint('Hello, ' + name + '!')\n(Name: John)",
    "\nnum = int(input('Enter a number: '))\nif num > 0:\n    print('Positive number')\nelif num < 0:\n    print('Negative number')\nelse:\n    print('Zero')\n(If Input:7)",
    "\nfor i in range(5):\n    print('Iteration:', i)",
    "\nfruits = ['apple', 'banana', 'orange']\nprint('Fruit:', fruits[1])\n\nperson = {'name': 'John', 'age': 25}\nprint('Name:', person['name'])",
    "\ndef add_numbers(a, b):\n    return a + b\n\nresult = add_numbers(3, 5)\nprint('Result:', result)",
    "\n# Write to a file\nwith open('example.txt', 'w') as file:\n    file.write('Hello, File!')\n\n# Read from a file\nwith open('example.txt', 'r') as file:\n    content = file.read()\n    print('File Content:', content)"
]

python_outputs = [
    ["Hello, World!", "Hello,World!"],
    ["Sum: 8 Product: 15", "Product:15 Sum:8"],
    ["Enter your name: John\nHello, John!", "Hello, John!", "Enter your name:John\nHello, John!"],
    ["Positive number"],
    ["0\n1\n2\n3\n4", "0 1 2 3 4", "Iteration: 0\nIteration: 1\nIteration: 2\nIteration: 3\nIteration: 4"],
    ["Fruit: banana"],
    ["Result: 8"],
    ["File Content: Hello, File!"]
]

level_names = [
    "Level 1: Introduction to Python",
    "Level 2: Basic Arithmetic Operations",
    "Level 3: User Input and Output",
    "Level 4: Conditional Statements",
    "Level 5: Loops",
    "Level 6: Lists and Dictionaries",
    "Level 7: Functions",
    "Level 8: File Handling"
]

current_level = 0

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Code Guessing Game")

# Load main menu background image and scale it to match the window size
main_menu_background_image = pygame.image.load("main_menu_background1.jpeg")
main_menu_background_image = pygame.transform.scale(main_menu_background_image, (WIDTH, HEIGHT))

# Load game background image and scale it to match the window size
game_background_image = pygame.image.load("game_background1.jpeg")
game_background_image = pygame.transform.scale(game_background_image, (WIDTH, HEIGHT))

# Database setup
Base = declarative_base()


class UserScore(Base):
    __tablename__ = 'user_scores'
    id = Column(Integer, primary_key=True)
    score = Column(Integer)


engine = create_engine('sqlite:///user_scores.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

highest_score = session.query(UserScore).order_by(UserScore.score.desc()).first()
if highest_score:
    highest_score_value = highest_score.score
else:
    highest_score_value = 0

# Add this line to define the "Try Again" button rectangle
try_again_button_rect = pygame.Rect(WIDTH // 2 - 260, HEIGHT // 2 + 100, 100, 50)
submit_button_rect = pygame.Rect(WIDTH // 2 + 160, HEIGHT // 2 + 100, 100, 50)

running = True
clock = pygame.time.Clock()
user_input = ""
user_score = 0
show_try_again_button = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif current_state == MAIN_MENU and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if WIDTH // 2 + 240 <= event.pos[0] <= WIDTH // 2 + 340 and HEIGHT // 2 - 3 <= event.pos[
                1] <= HEIGHT // 2 + 47:
                current_state = GAME_PLAYING
        elif current_state == GAME_PLAYING and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pass  # Do nothing when the Enter key is pressed
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.unicode.isprintable():
                user_input += event.unicode
        elif current_state == GAME_PLAYING and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if show_try_again_button and try_again_button_rect.collidepoint(event.pos):
                user_input = ""
                user_score = 0
                current_level = 0
                show_try_again_button = False
            elif submit_button_rect.collidepoint(event.pos):
                if any(user_input == valid_output for valid_output in python_outputs[current_level]):
                    user_input = ""
                    current_level += 1
                    user_score += 10
                    show_try_again_button = False
                    if current_level >= len(python_code_snippets):
                        current_level = 0
                        if user_score > highest_score_value:
                            highest_score_value = user_score
                            user_score_db = UserScore(score=highest_score_value)
                            session.add(user_score_db)
                            session.commit()
                else:
                    user_score = 0
                    show_try_again_button = True

    # Draw background based on the current state
    if current_state == MAIN_MENU:
        screen.blit(main_menu_background_image, (0, 0))
        pygame.draw.rect(screen, GREEN, (WIDTH // 2 + 240, HEIGHT // 2 - 3, 100, 50))
        play_button_text = FONT.render("Play", True, BLACK)
        screen.blit(play_button_text, (
            WIDTH // 2 + 20 + (550 - play_button_text.get_width()) // 2,
            HEIGHT // 2 - (5 - play_button_text.get_height()) // 2
        ))
    elif current_state == GAME_PLAYING:
        screen.blit(game_background_image, (0, 0))

        # Inserting line breaks manually in display_text
        lines = level_names[current_level].split('\n')
        total_height = FONT_SIZE * len(lines)
        y_offset = HEIGHT // 5 - total_height // 2

        for i, line in enumerate(lines):
            line_surface = FONT.render(line, True, GREEN)
            display_text_rect = line_surface.get_rect(center=(WIDTH // 2, y_offset + i * FONT_SIZE))
            screen.blit(line_surface, display_text_rect)

        # Draw code snippet
        code_snippet_lines = python_code_snippets[current_level].split('\n')
        code_snippet_height = FONT_SIZE * len(code_snippet_lines)
        code_snippet_y_offset = HEIGHT // 3 - code_snippet_height // 2

        for i, line in enumerate(code_snippet_lines):
            code_line_surface = FONT.render(line, True, GREEN)
            code_display_rect = code_line_surface.get_rect(center=(WIDTH // 2, code_snippet_y_offset + i * FONT_SIZE))
            screen.blit(code_line_surface, code_display_rect)

        # Draw user's input feedback
        user_input_text = FONT.render("Output: {}".format(user_input), True, WHITE)
        input_text_rect = user_input_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + code_snippet_height + 65))
        screen.blit(user_input_text, input_text_rect)

        # Draw "Try Again" button
        if show_try_again_button:
            pygame.draw.rect(screen, RED, try_again_button_rect)
            try_again_button_text = FONT.render("Try Again", True, BLACK)
            screen.blit(try_again_button_text, (
                try_again_button_rect.centerx - try_again_button_text.get_width() // 2,
                try_again_button_rect.centery - try_again_button_text.get_height() // 2
            ))

        # Draw "Submit" button
        pygame.draw.rect(screen, GREEN, submit_button_rect)
        submit_button_text = FONT.render("Submit", True, BLACK)
        screen.blit(submit_button_text, (
            submit_button_rect.centerx - submit_button_text.get_width() // 2,
            submit_button_rect.centery - submit_button_text.get_height() // 2
        ))

    # Draw user's score and highest score
    user_score_text = FONT.render("Score: {}".format(user_score), True, WHITE)
    highest_score_text = FONT.render("Highest Score: {}".format(highest_score_value), True, WHITE)
    screen.blit(user_score_text, (10, 10))
    screen.blit(highest_score_text, (WIDTH - highest_score_text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(30)

    if user_score > highest_score_value:
        highest_score_value = user_score

# Save the highest score before quitting the game
if highest_score_value > 0:
    user_score_db = UserScore(score=highest_score_value)
    session.add(user_score_db)
    session.commit()

# Close the database session
session.close()

pygame.quit()
sys.exit()
