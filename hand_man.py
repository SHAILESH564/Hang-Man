import pygame, sys, random

pygame.init()
WIDTH = 820
HEIGHT = 800
FPS = 60
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HANGMAN GAME")

font = pygame.font.SysFont("arial", 20)
SCREEN.fill("white")

words_used = []
wrong_answer = 0
mouse_pos = (0, 0)
lose_var = won_var = False

def select_word():
    # Select random word from file
    with open("words.txt", "r") as f:
        word_list = f.read().splitlines()
        return random.choice(word_list)

def draw():
    SCREEN.fill("white")
    # Outline
    pygame.draw.rect(SCREEN, "red", (1,1, WIDTH-1, HEIGHT -1), 2)
    pygame.draw.line(SCREEN, "red", (WIDTH //2, 0), (WIDTH //2, HEIGHT))
    # Frame
    pygame.draw.line(SCREEN, "red", (100, 200), (100, 700)) # Vertical
    pygame.draw.line(SCREEN, "red", (100, 200), (250, 200)) # Horizontal
    pygame.draw.line(SCREEN, "red", (75, 700), (200, 700)) # Base
    pygame.draw.line(SCREEN, "red", (250, 200), (250, 250)) # rope
    if wrong_answer > 0:
        pygame.draw.circle(SCREEN, "red", (250, 300), 50, 2) # Head
    if wrong_answer > 1:
        pygame.draw.line(SCREEN, 'red', (250, 350), (250, 550)) # Body
    if wrong_answer > 2:
        pygame.draw.line(SCREEN, "red", (250, 400), (200, 450)) # left Hand
    if wrong_answer > 3:
        pygame.draw.line(SCREEN, "red", (250, 400), (300, 450)) # right Hand
    if wrong_answer > 4:
        pygame.draw.line(SCREEN, "red", (250, 550), (200, 600)) # Left Leg
    if wrong_answer > 5:
        pygame.draw.line(SCREEN, "red", (250, 550), (300, 600)) # Right Leg


    if not (lose_var or won_var):
        dash_length = 25
        spacing = 50
        if word_count > 0:
            start_posx, start_posy = WIDTH // 2 + 25, HEIGHT // 2
            var = 0

            for word_real in word_draw:
                if start_posx + dash_length + spacing * var > WIDTH:
                    start_posx = WIDTH // 2 + 25
                    start_posy += 25
                    var = 0

                if word_real != '0':
                    text_surface = font.render(word_real, True, "blue")
                    SCREEN.blit(text_surface, (start_posx + spacing * var + 10, start_posy - 25))
                pygame.draw.line(SCREEN, "blue", ((start_posx + spacing * var, start_posy )), ((start_posx + dash_length + spacing * var, start_posy)))

                var += 1

        if len(words_used) > 0:
            start_posx, start_posy = WIDTH // 2 + 25, HEIGHT // 2 + 100
            start_posy_d = start_posy + 75

            text_surface = font.render("USED LETTERS: ", True, "red")
            SCREEN.blit(text_surface, (start_posx, start_posy))

            var = 0
            for word_in_used in (words_used):
                if start_posx + dash_length + spacing * var > WIDTH:
                    start_posx = WIDTH // 2 + 25
                    start_posy_d += 25
                    var = 0

                text_surface = font.render(word_in_used, True, "blue")
                SCREEN.blit(text_surface, (start_posx + spacing * var, start_posy_d - 25))

                pygame.draw.line(SCREEN, "blue", ((start_posx + spacing * var, start_posy_d )), ((start_posx + dash_length + spacing * var, start_posy_d )))
                var += 1
        
def check_if_closed(events):
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)

def lose_won():
    # Display it won or lost
    global lose_var, mouse_pos, won_var

    TRANSPARENT_SCREEN = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    TRANSPARENT_SCREEN.fill((0,0,0,220))

    message = "YOU LOST!!!" if lose_var else "YOU WON!!!"

    msg_render = font.render(message, True, "blanchedalmond")
    msg_rect = msg_render.get_rect(center=(WIDTH // 2 , HEIGHT // 2 - 50))
    TRANSPARENT_SCREEN.blit(msg_render, msg_rect)
        
    # Restart game
    restart_render = font.render("RESTART", True, "blanchedalmond")
    restart_rect = restart_render.get_rect(center=(WIDTH // 2 , HEIGHT // 2 ))
    TRANSPARENT_SCREEN.blit(restart_render, restart_rect)

    # Quit Game
    quit_render = font.render("QUIT", True, "blanchedalmond")
    quit_rect = quit_render.get_rect(center=(WIDTH // 2 , HEIGHT // 2 + 50 ))
    TRANSPARENT_SCREEN.blit(quit_render, quit_rect)

    SCREEN.blit(TRANSPARENT_SCREEN,  (0, 0))

    if restart_rect.collidepoint(mouse_pos):
        lose_var = won_var = False
        mouse_pos = (0, 0)
        hangman()
        draw()
        return
    elif quit_rect.collidepoint(mouse_pos):
        sys.exit(0)

def hangman():
    # Initialize the game 
    global word_draw, word_count, word, wrong_answer
    wrong_answer = 0
    words_used.clear()
    word = select_word().upper()
    word_count = len(word)
    word_draw = ['0'] * word_count
    print(word)

def check(word_typed):
    # word logic
    global wrong_answer
    
    if word_typed in words_used:
        return

    words_used.append(word_typed)

    if word_typed in word:
        for i in range(word_count):
            if word_typed == word[i]:
                word_draw[i] = word_typed
    else:
        wrong_answer += 1
    print(words_used, wrong_answer)

def check_inputs(events):
    global mouse_pos
    
    for event in events: 
        if event.type == pygame.KEYDOWN:
            if not (lose_var or won_var):
                if pygame.K_a <= event.key <= pygame.K_z:
                    word_typed = chr(event.key).upper()
                    check(word_typed)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

# < -------------------------      main block        ---------------------- >
hangman()
while True:
    events = pygame.event.get()
    check_if_closed(events)
    check_inputs(events)
    draw()
    if wrong_answer >= 6:
        lose_var = True
        lose_won()
    if '0' not in word_draw:
        won_var = True
        lose_won()

    clock.tick(FPS)

    pygame.display.flip()