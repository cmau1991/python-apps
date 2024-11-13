import pygame
import sys
import random
import requests
import os
import os.path
from pygame.locals import *
from pygame import mixer

# Initialise pygame
pygame.init()
mixer.init()

WIDTH = 1200
HEIGHT = 1000

# Create the screen & responsive-style surface
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
surface = pygame.Surface((WIDTH, HEIGHT), pygame.RESIZABLE)
scaled_surface = pygame.transform.smoothscale(surface, screen.get_size())
screen.blit(scaled_surface, (0, 0))

# Screen background
bg_img = pygame.image.load('images/battle.png')
bg_img = pygame.transform.smoothscale(bg_img, (WIDTH, HEIGHT))

# Screen music
mixer.music.load('sounds/battle_music.ogg')
mixer.music.play(-1)

# Load sound effects
win_round = pygame.mixer.Sound('sounds/you_win.wav')
lose_round = pygame.mixer.Sound('sounds/you_lose.wav')
card_selected = pygame.mixer.Sound('sounds/card_selected.wav')

# Define FPS
clock = pygame.time.Clock()
fps = 60

# Set Window title and the associated icon for the Game app
pygame.display.set_caption('Pokemon Battleground')
icon = pygame.image.load('images/pokeball.png')
pygame.display.set_icon(icon)

# Colours for the game play
black = (0, 0, 0)
white = (255, 255, 255)
grey1 = (210, 210, 210)
grey2 = (85, 85, 85)
grey3 = (40, 40, 40)

# Fonts for the entire game
welcome_font = pygame.font.Font('fonts/Pokefont.ttf', 60)
end_font = pygame.font.Font('fonts/Pokefont.ttf', 45)
instructions_font = pygame.font.Font('fonts/ThinItalic.ttf', 24)
titles_font = pygame.font.Font('fonts/Thin.ttf', 25)
card_font = pygame.font.Font('fonts/Thin.ttf', 20)
mini_card_font = pygame.font.Font('fonts/Thin.ttf', 18)

pokemon = requests.get('https://pokeapi.co/api/v2/pokemon').json()

class MAIN:
    def __init__(self):
        self.game_running = False
        self.menu_buttons = []
        self.player_score = 0
        self.opponent_score = 0
        self.round_winner = None
        self.opponent_wait = False
        self.end_round_wait = False
        self.game_over = None
        self.loading = False
        self.bg = 0

    # Reset game parameters and begin a new game
    def start_game(self):
        self.game_running = True
        self.player_score = 0
        self.opponent_score = 0
        self.round_winner = None
        self.opponent_wait = False
        self.end_round_wait = False
        self.game_over = False
        self.deck = Deck()
        self.player = Player()
        self.opponent = opponent()
        self.deal_cards()
        self.loading = False
        pygame.mixer.music.fadeout(1000)

    # Deal cards to each player
    def deal_cards(self):
        self.player.draw(self.deck)
        self.opponent.draw(self.deck)

    # Screen elements
    def draw_elements(self):
        if self.game_running == True:
            self.draw_board()
            self.player.draw_cards()
            self.opponent.draw_cards()
            self.player.draw_selected_card()
            self.opponent.draw_selected_card()
            self.draw_score()
            self.draw_instructions()
            self.draw_round_result()
        else:
            self.draw_game_result()
            self.draw_start_screen()
            self.draw_loading()

    def draw_background(self):
        if self.game_running == True:
            screen.fill(black)
        else:
            screen.fill(black)
            screen.blit(bg_img, (self.bg, 0))
            screen.blit(bg_img, (WIDTH + self.bg, 0))
            if (self.bg == -WIDTH):
                screen.blit(bg_img, (WIDTH + self.bg, 0))
                self.bg = 0
            self.bg -= 1

    def draw_board(self):
        bottom_menu = pygame.draw.rect(screen, grey3, [0, 0, WIDTH, 40])

        opponent_container = pygame.draw.rect(screen, white, [15, 50, 1175, 295], width=1)
        opponent_text = titles_font.render('Opponent', True, white)
        opponent_text_rect = opponent_text.get_rect(center=(WIDTH / 2, 68))
        screen.blit(opponent_text, opponent_text_rect)

        player_container = pygame.draw.rect(screen, white, [15, 670, 1175, 295],width=1)
        player_text = titles_font.render('Player', True, white)
        player_text_rect = player_text.get_rect(center=(WIDTH / 2, 685))
        screen.blit(player_text, player_text_rect)

    def draw_start_screen(self):
        # Draw welcome message when the program starts
        if self.game_over == None:
            welcome_text = welcome_font.render('Welcome to the Pokemon Battleground!', True, white)
            welcome_text_rect = welcome_text.get_rect(center=(600, 200))
            screen.blit(welcome_text, welcome_text_rect)

        # New game and exit game buttons on the start screen / replay screen
        mouse_pos = pygame.mouse.get_pos()
        start = pygame.Rect([450, 650, 140, 50])
        start_text = titles_font.render('New Game', True, white)
        start_text_rect = start_text.get_rect(center=(520, 675))
        if start.collidepoint(mouse_pos):
            pygame.draw.rect(screen, grey2, start, border_radius=6)
            if pygame.mouse.get_pressed()[0]:
                self.loading = True
        else:
            pygame.draw.rect(screen, white, start, width=1, border_radius=6)
        screen.blit(start_text, start_text_rect)

        exit = pygame.Rect([610, 650, 140, 50])
        exit_text = titles_font.render('Exit Game', True, white)
        exit_text_rect = exit_text.get_rect(center=(680, 675))
        if exit.collidepoint(mouse_pos):
            pygame.draw.rect(screen, grey2, exit, border_radius=6)
        else:
            pygame.draw.rect(screen, white, exit, width=1, border_radius=6)
        screen.blit(exit_text, exit_text_rect)

        self.menu_buttons.append(start)
        self.menu_buttons.append(exit)

    # "loading" message will appear on screen when a player presses the "New Game" button
    def draw_loading(self):
        if self.loading == True:
            loading_text = titles_font.render('Loading...', True, white)
            loading_text_rect = loading_text.get_rect(center=(600, 600))
            screen.blit(loading_text, loading_text_rect)

    # show the running total score on the screen (upper right hand side of the screen)
    def draw_score(self):
        score_text = titles_font.render(f'Player: {self.player_score} | Opponent: {self.opponent_score}', True, white)
        score_rect = score_text.get_rect()
        score_rect.topright = (1100, 5)
        screen.blit(score_text, score_rect)

    # Display the game instructions on the screen - in the game play zone
    def draw_instructions(self):
        if self.player.turn == True:
            if self.player.selected_card is None and self.player.selected_attribute is None:
                instructions_text = instructions_font.render('You are up: pick a card!', True, white)
                screen.blit(instructions_text, (150, 400))
            elif self.player.selected_card is not None and self.player.selected_attribute is None:
                instructions_text = instructions_font.render(
                    'Which stat would you like to use on your opponent? Enter h for height, i for id, or w for weight. Pick now!', True,
                    white)
                screen.blit(instructions_text, (150, 400))
        elif self.player.turn == False:
            if self.opponent.selected_attribute is None:
                instructions_text = instructions_font.render('Your opponent is choosing a card, please wait...', True, white)
                screen.blit(instructions_text, (50, 400))

    # Update main game after each game event
    def update(self):
        self.player.check_played()
        self.check_opponent_turn()
        self.check_end_round()
        self.opponent_timer()
        self.round_timer()

    # Perform an automated check to see if the game player's turn is complete.
    # If true, initiate the timer for the opponent to pick their card and stat.
    def check_opponent_turn(self):
        if self.player.turn == False and self.opponent.selected_attribute is None:
            self.opponent_wait = True

    # The timer will run down, the opponent will select their card and stat.
    # Stats are then compared and the winner is displayed on screen.
    def opponent_timer(self):
        if self.opponent_wait == True:
            current_time = pygame.time.get_ticks()
            if current_time - self.player.time_played >= 2000:
                self.opponent_wait = False
                self.opponent.play_hand(self.player.selected_attribute[0])
                self.round_winner = self.set_round_winner(self.opponent.selected_attribute, self.player.selected_attribute)

    # Assign the round winner and add one point to their running total - update in upper right hand side of screen
    def set_round_winner(self, opponent, player):
        if opponent[1] > player[1]:
            self.opponent_score += 1
            pygame.mixer.Sound.play(lose_round)
            return 'Opponent'
        elif opponent[1] < player[1]:
            self.player_score += 1
            pygame.mixer.Sound.play(win_round)
            return 'Player'
        else:
            pygame.mixer.Sound.play(lose_round)
            return 'Tie'

    # Check if opponent's turn is finished.
    # If true, a timer is activated.
    def check_end_round(self):
        if self.opponent.selected_attribute is not None:
            self.end_round_wait = True

    # Timer to run down before resetting round and starting again.
    def round_timer(self):
        if self.end_round_wait == True:
            current_time = pygame.time.get_ticks()
            if current_time - self.opponent.time_played >= 2000:
                self.end_round_wait = False
                self.reset_round()

    # Reset round parameters and check if game should finish
    def reset_round(self):
        self.player.turn = True
        self.player.selected_card = None
        self.player.selected_attribute = None
        self.opponent.turn = False
        self.opponent.selected_card = None
        self.opponent.selected_attribute = None
        self.round_winner = None
        self.check_end_game()

    # Perform a check to determine if all the cards in the deck have been used, or not.
    def check_end_game(self):
        if not any(d['used'] == False for d in self.opponent.cards):
            self.game_over = True
            self.game_running = False
            pygame.mixer.music.play(-1)

    # Display the round result on the screen.
    def draw_round_result(self):
        if self.round_winner is not None:
            if self.round_winner == 'Opponent':
                result_text = titles_font.render('Your opponent won this round!', True, white)
            elif self.round_winner == 'Player':
                result_text = titles_font.render('You won this round!', True, white)
            else:
                result_text = titles_font.render('Tie!', True, white)
            result_rect = result_text.get_rect()
            result_rect.center = (600, 655)
            screen.blit(result_text, result_rect)

    # Display the game result on the screen.
    def draw_game_result(self):
        if self.game_running == False and self.game_over == True:
            if self.player_score > self.opponent_score:
                result_text = end_font.render('Congratulations! You won!', True, white)
            elif self.player_score < self.opponent_score:
                result_text = end_font.render('Bad luck! Your opponent won.', True, white)
            else:
                result_text = end_font.render('Tie!', True, white)
            result_rect = result_text.get_rect()
            result_rect.center = (600, 400)
            screen.blit(result_text, result_rect)


class opponent:
    def __init__(self):
        self.cards = []
        self.card_rects = []
        self.create_card_rects()
        self.turn = False
        self.selected_card = None
        self.selected_attribute = None
        self.time_played = 0

    # Dealing of cards to opponent
    def draw(self, deck):
        for _ in range(7):
            card = deck.deal()
            self.cards.append(card)

    # opponent is programmed to select a random card from their deck.
    def play_hand(self, attribute_name):
        played_card = random.choice([x for x in self.cards if x['used'] != True])
        self.selected_card = self.cards.index(played_card)
        self.cards[self.selected_card]['used'] = True
        self.time_played = pygame.time.get_ticks()
        self.selected_attribute = (attribute_name, played_card[attribute_name])

    def create_card_rects(self):
        for i in range(7):
            card = pygame.Rect((i * 160 + 50, 90), (140, 240))
            self.card_rects.append(card)

    def draw_cards(self):
        for card in self.card_rects:
            i = self.card_rects.index(card)
            if self.cards[i]['used'] == True:
                pygame.draw.rect(screen, black, card)
            else:
                pygame.draw.rect(screen, grey3, card, border_radius=12)

    def draw_selected_card(self):
        # Once opponent card and attribute are selected,
        # draw selected card and render images and text in the battleground zone
        if self.selected_attribute is not None:
            selected_card = pygame.Rect((625, 380), (4, 240))
            pygame.draw.rect(screen, grey2, selected_card, border_radius=12)

            name_text = card_font.render(self.cards[self.selected_card]['name'].capitalize(), True, white)
            id_text = mini_card_font.render(f'ID: {self.cards[self.selected_card]["id"]}', True, white)
            height_text = mini_card_font.render(f'Height: {self.cards[self.selected_card]["height"]}', True, white)
            weight_text = mini_card_font.render(f'Weight: {self.cards[self.selected_card]["weight"]}', True, white)
            image = pygame.image.load(f'images/pokemon/{self.cards[self.selected_card]["image"]}').convert_alpha()
            image_resized = pygame.transform.scale(image, (140, 140))

            screen.blit(name_text, (630, 385))
            screen.blit(image_resized, (625, 415))
            screen.blit(id_text, (630, 555))
            screen.blit(height_text, (630, 575))
            screen.blit(weight_text, (630, 595))

            played_text = titles_font.render(f'Opponent played: {self.cards[self.selected_card]["name"].capitalize()}!', True,
                                             white)
            played_text_rect = played_text.get_rect()
            played_text_rect.topleft = (795, 440)
            screen.blit(played_text, played_text_rect)

            attribute_text = titles_font.render(
                f'{self.selected_attribute[0].capitalize()}: {self.selected_attribute[1]}', True, white)
            attribute_text_rect = attribute_text.get_rect()
            attribute_text_rect.topleft = (795, 480)
            screen.blit(attribute_text, attribute_text_rect)


class Player:
    def __init__(self):
        self.cards = []
        self.card_rects = []
        self.create_card_rects()
        self.card_clicked = False
        self.turn = True
        self.selected_card = None
        self.selected_attribute = None
        self.time_played = 0
        self.sound_played = False

    # Dealing of cards to the game player.
    def draw(self, deck):
        for _ in range(7):
            card = deck.deal()
            self.cards.append(card)

    def create_card_rects(self):
        for i in range(7):
            card = pygame.Rect((i * 160 + 50, 710), (140, 240))
            self.card_rects.append(card)

    def draw_cards(self):
        for card in self.card_rects:
            i = self.card_rects.index(card)
            mouse_pos = pygame.mouse.get_pos()
            if card.collidepoint(mouse_pos) and self.turn == True and self.cards[i][
                'used'] == False and self.selected_card == None or self.turn == True and self.selected_card == i:
                pygame.draw.rect(screen, grey2, card, border_radius=12)
            elif self.cards[i]['used'] == True:
                pygame.draw.rect(screen, black, card)
            else:
                pygame.draw.rect(screen, grey3, card, border_radius=12)

            name_text = card_font.render(self.cards[i]['name'].capitalize(), True, white)
            image = pygame.image.load(f'images/pokemon/{self.cards[i]["image"]}').convert_alpha()
            image_resized = pygame.transform.scale(image, (140, 140))
            id_text = mini_card_font.render(f'ID: {self.cards[i]["id"]}', True, white)
            height_text = mini_card_font.render(f'Height: {self.cards[i]["height"]}', True, white)
            weight_text = mini_card_font.render(f'Weight: {self.cards[i]["weight"]}', True, white)

            if self.cards[i]['used'] == False or self.cards[i][
                'used'] == True and self.selected_card == i and self.selected_attribute is None:
                screen.blit(name_text, (i * 160 + 55, 715))
                screen.blit(image_resized, (i * 160 + 50, 745))
                screen.blit(id_text, (i * 160 + 55, 885))
                screen.blit(height_text, (i * 160 + 55, 905))
                screen.blit(weight_text, (i * 160 + 55, 925))

    # Once the game player has selected both their card & stat,
    # the selected card will be drawn &
    # displayed in the battleground zone of the screen.
    def draw_selected_card(self):
        if self.selected_attribute is not None:
            selected_card = pygame.Rect((435, 380), (140, 240))
            pygame.draw.rect(screen, grey2, selected_card, border_radius=12)

            name_text = card_font.render(self.cards[self.selected_card]['name'].capitalize(), True, white)
            id_text = mini_card_font.render(f'ID: {self.cards[self.selected_card]["id"]}', True, white)
            height_text = mini_card_font.render(f'Height: {self.cards[self.selected_card]["height"]}', True, white)
            weight_text = mini_card_font.render(f'Weight: {self.cards[self.selected_card]["weight"]}', True, white)
            image = pygame.image.load(f'images/pokemon/{self.cards[self.selected_card]["image"]}').convert_alpha()
            image_resized = pygame.transform.scale(image, (140, 140))

            screen.blit(name_text, (440, 385))
            screen.blit(image_resized, (435, 415))
            screen.blit(id_text, (440, 555))
            screen.blit(height_text, (440, 575))
            screen.blit(weight_text, (440, 595))

            played_text = titles_font.render(f'You played: {self.cards[self.selected_card]["name"].capitalize()}!',
                                             True, white)
            played_text_rect = played_text.get_rect()
            played_text_rect.topright = (420, 450)
            screen.blit(played_text, played_text_rect)

            attribute_text = titles_font.render(
                f'{self.selected_attribute[0].capitalize()}: {self.selected_attribute[1]}', True, white)
            attribute_text_rect = attribute_text.get_rect()
            attribute_text_rect.topright = (420, 480)
            screen.blit(attribute_text, attribute_text_rect)

    # Perform a check to confirm whether the game player has selected their card & stat
    # If true, then the game player turn ends and switches to the opponent.
    def check_played(self):
        if self.turn == True and self.selected_attribute is not None:
            self.time_played = pygame.time.get_ticks()
            pygame.mixer.Sound.play(card_selected)
            self.turn = False

# Generation of a list containing a dictionary for each Poke-card.
# Each dictionary will contain details relating to: id, name, height, weight, image.
class Deck:
    def __init__(self):
        self.deck = []
        self.build_deck()

    def build_deck(self):
        for _ in range(14):
            pokemon = dict()
            while True:
                id = random.randint(1, 898)
                if not any(d['id'] == id for d in self.deck):
                    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id}').json()
                    image_path = 'images/pokemon/' + response["name"] + '.png'
                    if os.path.isfile(image_path):
                        break
                    else:
                        continue
                else:
                    print('id already exists')
                    continue

            # Create a dictionary that will store Pokemon stats for use in game play.
            pokemon['id'] = id
            pokemon['name'] = response['name']
            pokemon['height'] = response['height']
            pokemon['weight'] = response['weight']
            pokemon['image'] = f'{pokemon["name"]}.png'
            pokemon['used'] = False
            self.deck.append(pokemon)

    # Python to call the deal method when cards are dealt on screen.
    def deal(self):
        return self.deck.pop()


# New game
main_game = MAIN()

# Create a game loop whilst cards are still present in the deck.
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if main_game.game_running == False:
                if main_game.menu_buttons[1].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if main_game.menu_buttons[0].collidepoint(event.pos):
                    main_game.start_game()
            if main_game.game_running == True:
                if main_game.player.selected_card is None and main_game.player.selected_attribute is None:
                    for card in main_game.player.card_rects:
                        if card.collidepoint(event.pos) and \
                                main_game.player.cards[main_game.player.card_rects.index(card)]['used'] == False:
                            main_game.player.selected_card = main_game.player.card_rects.index(card)
                            main_game.player.cards[main_game.player.selected_card]['used'] = True
        if event.type == pygame.KEYDOWN:
            if main_game.game_running == True:
                if main_game.player.selected_card is not None and main_game.player.selected_attribute is None:
                    if event.key == pygame.K_i:
                        main_game.player.selected_attribute = (
                        'id', main_game.player.cards[main_game.player.selected_card]['id'])
                    if event.key == pygame.K_h:
                        main_game.player.selected_attribute = (
                        'height', main_game.player.cards[main_game.player.selected_card]['height'])
                    if event.key == pygame.K_w:
                        main_game.player.selected_attribute = (
                        'weight', main_game.player.cards[main_game.player.selected_card]['weight'])

    main_game.draw_background()
    main_game.draw_elements()
    clock.tick(fps)

    if main_game.game_running == True:
        main_game.update()

    pygame.display.update()
