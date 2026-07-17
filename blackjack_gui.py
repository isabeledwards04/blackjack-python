""" 
Blackjack - Pygame GUI Edition

I built the inital project for the assignment, and then made it into a GUI version once everything was 
working. The cards, buttons and sound effects are generated in code (removes the risks of files not 
loading on someone else's computer).

The aim of the game is to beat the dealer by getting as close to 21 as possible without going over. 

King, Queen and Jack are worth 10 points, Aces can be worth 1 or 11 points, and all other cards are worth their face value.

How to play:
- Click HIT to take another card 
- Click STAND to end your turn and let the dealer play
- Click PLAY AGAIN to start a new round
- Click QUIT to exit the game

Best of luck! :)
"""

import sys
import random
import numpy as np
import pygame

# pygame.mixer.pre_init() must be run before pygame.init() to avoid sound lag. 

SAMPLE_RATE = 44100
pygame.mixer.pre_init(SAMPLE_RATE, -16, 1, 512)
pygame.init()

# Window setup 
WIDTH, HEIGHT = 900, 650
FPS = 60

# Colour palette RGB codes. I went for a deep emerald colour scheme to make it feel more like a real 
# casino table table. 

COLOR_BG = (13, 74, 58)
COLOR_BG_DARK = (8, 48, 38)
COLOR_CARD = (250, 247, 240)
COLOR_CARD_BACK = (30, 42, 74)
COLOR_RED = (196, 60, 66)
COLOR_BLACK = (33, 33, 38)
COLOR_WHITE = (240, 237, 228)
COLOR_GOLD = (212, 165, 89)
COLOR_BUTTON = (24, 94, 78)
COLOR_BUTTON_HOVER = (37, 130, 106)
COLOR_BUTTON_DISABLED = (60, 66, 63)
COLOR_WIN = (168, 199, 130)
COLOUR_LOSE = (196, 60, 66)

# Font sizes for different text elements

FONT_BIG = pygame.font.SysFont("arial", 48, bold=True)
FONT_MED = pygame.font.SysFont("arial", 28, bold=True)
FONT_SMALL = pygame.font.SysFont("arial", 20)
FONT_CARD = pygame.font.SysFont("arial", 26, bold=True)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()

# GLOBAL COUNTERS
# I kept them outisde every function so they are there the whole time the game is open and doesn't 
# reset every round.

games_played = 0
player_wins = 0
dealer_wins = 0
pushes = 0
blackjacks_hit = 0

# SOUND EFFECTS 

# Rather than downloading sound files, I found a way to use make them using soundwaves, so I can build one 
# with a sine function and give it to pygame. This was not something I knew how to do, so I did use AI 
# to help me with this part. I wanted to me honest rather than making the unrealistic claim that I did it all myself.

# However I did read up on it and make sure I understood it, and can explain why and how everything works.

def make_tone(frequency, duration, volume=0.4):
    """Build one plain beep at a specific pitch / length
    frequency is in Hz (higher number is a higher pitch). The audio
    fades in and out to make it less harsh."""

    n_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n_samples, False)
    wave = np.sin(frequency * t * 2 * np.pi)
    fade_len = max(1, int(n_samples * 0.08))
    fade = np.linspace(0, 1, fade_len)
    wave[:fade_len] *= fade
    wave[-fade_len:] *= fade[::-1]
    audio = (wave * volume * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(audio)


def make_chime(frequencies, note_duration=0.13, volume=0.35):
    """Create a short melody by chaining tones. 
    Used this for win/lose/blackjack jingles """
    pieces = []
    for freq in frequencies:
        n_samples = int(SAMPLE_RATE * note_duration)
        t = np.linspace(0, note_duration, n_samples, False)
        wave = np.sin(freq * t * 2 * np.pi)
        fade_len = max(1, int(n_samples * 0.1))
        fade = np.linspace(0, 1, fade_len)
        wave[:fade_len] *= fade
        wave[-fade_len:] *= fade[::-1]
        pieces.append(wave)
    audio = np.concatenate(pieces)
    audio = (audio * volume * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(audio)


def make_background_loop():
    """Background music to create a nice atmosphere"""
    notes = [220, 261, 220, 196]
    return make_chime(notes, note_duration=0.9, volume=0.10)

# Every action backes a sound effect, so the player gets feedback on what is happening. 
# Doing a full sine wave was causing a lag so the shorter sound was more effective. 

SND_FLIP = make_tone(300, 0.07, 0.3)
SND_HIT = make_tone(250, 0.09, 0.3)
SND_BUST = make_tone(110, 0.35, 0.5)
SND_WIN = make_chime([523, 659, 784, 1047])
SND_BLACKJACK = make_chime([523, 659, 784, 1047, 1319])
SND_LOSE = make_chime([392, 330, 262])
SND_PUSH = make_tone(440, 0.18, 0.3)
SND_CLICK = make_tone(600, 0.04, 0.25)
BG_MUSIC = make_background_loop()
BG_MUSIC.play(loops=-1)

# CARD SUITS AND VALUES

SUIT_SYMBOLS = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
RED_SUITS = {"Hearts", "Diamonds"}


def create_deck():
    """Build a standard 52-card deck and shuffle it"""
    
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = list(SUIT_SYMBOLS.keys())
    deck = [(rank, suit) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck


def card_value(card):
    """Value of each card, face cards are worth 10, Aces are worth 11 (or 1 if the total is over 21)."""
    rank = card[0]
    if rank in ('J', 'Q', 'K'):
        return 10
    if rank == 'A':
        return 11
    return int(rank)


def calculate_hand_value(hand):
    """An ace will have a value of 11 unless the total is over 21, in which case it will be worth 1"""
    total = sum(card_value(c) for c in hand)
    aces = sum(1 for c in hand if c[0] == 'A')
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

# Buttons!! 

class Button:
    """A simple button class for the GUI so you can Hit/Stand/Play Again/Quit without repeating the code for each button. """
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.enabled = True

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if not self.enabled:
            color = COLOR_BUTTON_DISABLED
        elif self.rect.collidepoint(mouse_pos):
            color = COLOR_BUTTON_HOVER
        else:
            color = COLOR_BUTTON
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_WHITE, self.rect, width=2, border_radius=10)
        label = FONT_MED.render(self.text, True, COLOR_WHITE)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def is_clicked(self, event):
        """Only can be clicked if button is usable, stops a play again button being clicked mid game"""
        return (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


# DRAWING 

CARD_W, CARD_H = 90, 130


def draw_card(surface, x, y, card, hidden=False):
    """Draw a single card on the surface. If hidden is True, draw the back of the card."""
    rect = pygame.Rect(x, y, CARD_W, CARD_H)
    if hidden:
        pygame.draw.rect(surface, COLOR_CARD_BACK, rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_WHITE, rect, width=2, border_radius=10)
        # To make the back of the card actually look like a card. 
        pygame.draw.line(surface, COLOR_WHITE, rect.topleft, rect.bottomright, 2)
        pygame.draw.line(surface, COLOR_WHITE, rect.topright, rect.bottomleft, 2)
        return
    pygame.draw.rect(surface, COLOR_CARD, rect, border_radius=10)
    pygame.draw.rect(surface, COLOR_BLACK, rect, width=2, border_radius=10)
    rank, suit = card
    color = COLOR_RED if suit in RED_SUITS else COLOR_BLACK
    symbol = SUIT_SYMBOLS[suit]
    rank_label = FONT_CARD.render(rank, True, color)
    surface.blit(rank_label, (x + 8, y + 6))
    symbol_label = FONT_BIG.render(symbol, True, color)
    symbol_rect = symbol_label.get_rect(center=(x + CARD_W // 2, y + CARD_H // 2 + 10))
    surface.blit(symbol_label, symbol_rect)


def draw_hand(surface, hand, x, y, hide_first=False):
    """Lay out the cards evenly left to right and evenly spaced"""
    for i, card in enumerate(hand):
        hidden = hide_first and i == 0
        draw_card(surface, x + i * (CARD_W + 15), y, card, hidden=hidden)


def draw_text_center(surface, text, font, color, center_pos):
    label = font.render(text, True, color)
    rect = label.get_rect(center=center_pos)
    surface.blit(label, rect)


def draw_stats_panel(surface):
    """Stats box in the top right thats always visible so the player can see how they are doing over time"""
    panel = pygame.Rect(WIDTH - 230, 15, 215, 140)
    pygame.draw.rect(surface, COLOR_BG_DARK, panel, border_radius=10)
    pygame.draw.rect(surface, COLOR_GOLD, panel, width=2, border_radius=10)
    lines = [
        f"Games: {games_played}",
        f"Wins: {player_wins}",
        f"Losses: {dealer_wins}",
        f"Pushes: {pushes}",
        f"Blackjacks: {blackjacks_hit}",
    ]
    for i, line in enumerate(lines):
        label = FONT_SMALL.render(line, True, COLOR_WHITE)
        surface.blit(label, (panel.x + 12, panel.y + 12 + i * 24))

# GAME STATE

# The game has three states: the player's turn, the dealer's turn, and the round being over.

STATE_INSTRUCTIONS = "instructions"
STATE_PLAYER_TURN = "player_turn"
STATE_DEALER_TURN = "dealer_turn"
STATE_ROUND_OVER = "round_over"

state = STATE_INSTRUCTIONS
deck = []
player_hand = []
dealer_hand = []
result_text = ""
result_color = COLOR_WHITE

# Short pause between dealer's actions so you can actually see what is happening,
# rather than it being instant. Makes it feel more like a real game.
DEALER_HIT_DELAY_MS = 700
last_dealer_action_time = 0

hit_button = Button(230, 520, 150, 55, "HIT")
stand_button = Button(420, 520, 150, 55, "STAND")
play_again_button = Button(210, 520, 220, 55, "PLAY AGAIN")
quit_button = Button(450, 520, 150, 55, "QUIT")
start_button = Button(WIDTH // 2 - 100, 560, 200, 55, "START GAME")


# list of lines rather than one long string so I can loop over it and
# draw each line with its own y position instead of dealing with
# manual line wrapping.
INSTRUCTION_LINES = [
    "Try to get as close to 21 as possible without going over.",
    "Number cards = face value   J / Q / K = 10   Ace = 1 or 11",
    "",
    "You go first. Click HIT to take another card, or STAND to stop.",
    "If your total goes over 21, you bust and lose the round.",
    "",
    "Once you stand, the dealer reveals their hidden card and must",
    "keep hitting until their total reaches 17 or higher.",
    "",
    "Closest to 21 without going over wins. A two-card 21 is a",
    "natural Blackjack - an automatic win.",
]
 
 
def draw_instructions_screen(surface):
    """Draw the rules screen that's shown before the first round.
 
    This is its own state (STATE_INSTRUCTIONS) rather than just a
    pop-up, so the main loop's draw step handles it the same way it
    handles every other screen - fill background, draw content, draw
    the relevant button(s) for this state.
    """
    surface.fill(COLOR_BG)
    pygame.draw.rect(surface, COLOR_BG_DARK, (0, 0, WIDTH, 90))
    draw_text_center(surface, "BLACKJACK", FONT_BIG, COLOR_GOLD, (WIDTH // 2, 45))
 
    draw_text_center(surface, "How to play", FONT_MED, COLOR_GOLD, (WIDTH // 2, 140))
 
    line_y = 190
    for line in INSTRUCTION_LINES:
        if line:  # skip drawing anything for blank spacer lines
            draw_text_center(surface, line, FONT_SMALL, COLOR_WHITE, (WIDTH // 2, line_y))
        line_y += 28
 
    start_button.draw(surface)
 

def start_new_round():
    """"Reset the game state and deal new hands to the player and dealer."""
    global deck, player_hand, dealer_hand, state, result_text
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    state = STATE_PLAYER_TURN
    result_text = ""
    SND_FLIP.play()


def determine_winner():
    """Work out who won and update the stats to match, and make sure the right message shows"""
    global games_played, player_wins, dealer_wins, pushes, blackjacks_hit
    global result_text, result_color
    games_played += 1
    p_total = calculate_hand_value(player_hand)
    d_total = calculate_hand_value(dealer_hand)
    player_natural = (p_total == 21 and len(player_hand) == 2)

    if p_total > 21:
        dealer_wins += 1
        result_text, result_color = "YOU BUSTED - DEALER WINS", COLOR_RED
        SND_BUST.play()
    elif d_total > 21:
        player_wins += 1
        result_text, result_color = "DEALER BUSTED - YOU WIN!", COLOR_GOLD
        SND_WIN.play()
    elif p_total > d_total:
        player_wins += 1
        if player_natural:
            blackjacks_hit += 1
            result_text, result_color = "BLACKJACK! YOU WIN!", COLOR_GOLD
            SND_BLACKJACK.play()
        else:
            result_text, result_color = "YOU WIN!", COLOR_GOLD
            SND_WIN.play()
    elif d_total > p_total:
        dealer_wins += 1
        result_text, result_color = "DEALER WINS", COLOR_RED
        SND_LOSE.play()
    else:
        pushes += 1
        result_text, result_color = "PUSH (TIE)", COLOR_WHITE
        SND_PUSH.play()


def handle_hit():
    """Player takes another card and check straight away if its busted"""
    global state
    player_hand.append(deck.pop())
    SND_HIT.play()
    if calculate_hand_value(player_hand) > 21:
        # no point in waiting for the dealer to play if the player has already busted, 
        # so go straight to the round over state
        state = STATE_DEALER_TURN


def handle_stand():
    """If player sticks the turn will go straight to the dealer, who will play their turn automatically 
    (minus the little delay to make it feel more like a real game)"""
    global state, last_dealer_action_time
    state = STATE_DEALER_TURN
    last_dealer_action_time = pygame.time.get_ticks()


def update_dealer_turn():
    """Runs every frame while the dealer is playing their turn, and will automatically determine the winner 
    when the dealer is done."""
    global state, last_dealer_action_time
    if calculate_hand_value(player_hand) > 21:
        determine_winner()
        state = STATE_ROUND_OVER
        return
    now = pygame.time.get_ticks()
    if now - last_dealer_action_time < DEALER_HIT_DELAY_MS:
        return
    if calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        SND_HIT.play()
        last_dealer_action_time = now
    else:
        determine_winner()
        state = STATE_ROUND_OVER


def main():
    """Main game loop - handles events, updates the game state, and draws everything to the screen."""
    global state
    running = True

    while running:
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == STATE_INSTRUCTIONS:
                if start_button.is_clicked(event):
                    SND_CLICK.play()
                    start_new_round()

            elif state == STATE_PLAYER_TURN:
                if hit_button.is_clicked(event):
                    SND_CLICK.play()
                    handle_hit()
                elif stand_button.is_clicked(event):
                    SND_CLICK.play()
                    handle_stand()
            elif state == STATE_ROUND_OVER:
                if play_again_button.is_clicked(event):
                    SND_CLICK.play()
                    start_new_round()
                elif quit_button.is_clicked(event):
                    running = False

        # Update
        if state == STATE_DEALER_TURN:
            update_dealer_turn()

        # Draw
        if state == STATE_INSTRUCTIONS:
            draw_instructions_screen(screen)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        screen.fill(COLOR_BG)
        pygame.draw.rect(screen, COLOR_BG_DARK, (0, 0, WIDTH, 90))
        draw_text_center(screen, "BLACKJACK", FONT_BIG, COLOR_GOLD, (WIDTH // 2, 45))
        draw_stats_panel(screen)
        # Keeping the dealer's first card hidden until games done
        hide_first = state == STATE_PLAYER_TURN
        draw_text_center(screen, "Dealer", FONT_MED, COLOR_WHITE, (150, 150))
        draw_hand(screen, dealer_hand, 60, 170, hide_first=hide_first)
        if not hide_first:
            d_total = calculate_hand_value(dealer_hand)
            draw_text_center(screen, f"Total: {d_total}", FONT_SMALL, COLOR_WHITE, (150, 320))
        draw_text_center(screen, "Player", FONT_MED, COLOR_WHITE, (150, 360))
        draw_hand(screen, player_hand, 60, 380, hide_first=False)
        p_total = calculate_hand_value(player_hand)
        draw_text_center(screen, f"Total: {p_total}", FONT_SMALL, COLOR_WHITE, (150, 530))

        if state == STATE_PLAYER_TURN:
            hit_button.draw(screen)
            stand_button.draw(screen)
        elif state == STATE_ROUND_OVER:
            result_rect = pygame.Rect(WIDTH - 500, 300, 320, 70)
            pygame.draw.rect(screen, COLOR_BG_DARK, result_rect, border_radius=10)
            pygame.draw.rect(screen, COLOR_GOLD, result_rect, width=2, border_radius=10)
            draw_text_center(screen, result_text, FONT_MED, result_color, result_rect.center)
            play_again_button.draw(screen)
            quit_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
