import threading, fnmatch, random, time, os
import pygame as py

from copy import copy
from pathlib import Path

import _Game as Game

BOARD_SIZE = 800
PIECE_SIZE = BOARD_SIZE / 8

# Initialise variables and board
G = Game.Game()
board = Game.Board(G)
board.setup()

def clear():
    os.system('cls')
    print('\n'*100)

clear()
seed = input('Enter seed: (Leave blank for random)\n>> ')
random.seed(seed if seed else random.randint(1, 99999999))

close_board = False
def board_thread():
    global screen, win
    
    py.init()
    win = py.Window('Chess but Awesome', size=(BOARD_SIZE, BOARD_SIZE))
    win.always_on_top = True
    win.focus()
    screen = win.get_surface()
    
    base_dir = Path(__file__).resolve().parent
    image_path = base_dir / 'images'
    
    running = True
    try:
        while running and not close_board:
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
            
            # Load the background
            bg = py.image.load(image_path / 'board.png')
            bg = py.transform.scale(bg, (BOARD_SIZE, BOARD_SIZE))
            screen.blit(bg, (0, 0))
            
            for x in range(8):
                for y in range(8):                
                    if [x, y] in G.wwyw_tiles:
                        filename = image_path / 'watch_where_you_walk.png'
                        
                        tile = py.image.load(filename)
                        tile = py.transform.scale(tile, (PIECE_SIZE, PIECE_SIZE))
                        screen.blit(tile, (x*PIECE_SIZE, y*PIECE_SIZE))
                    
                    piece = board.get_tile(x, y)
                    
                    
                    
                    if piece != None:
                        if piece.id in G.res5_pieces + G.hobbAsc_pieces:
                            filename = image_path / 'invincibility.png'
                            
                            tile = py.image.load(filename)
                            tile = py.transform.scale(tile, (PIECE_SIZE, PIECE_SIZE))
                            screen.blit(tile, (x*PIECE_SIZE, y*PIECE_SIZE))
                        
                        if piece.id in G.marked_pieces:
                            filename = image_path / 'marked.png'
                            
                            tile = py.image.load(filename)
                            tile = py.transform.scale(tile, (PIECE_SIZE, PIECE_SIZE))
                            screen.blit(tile, (x*PIECE_SIZE, y*PIECE_SIZE))
                        
                        if piece.id in G.hotPotato_pieces:
                            filename = image_path / 'hot_potato.png'
                            
                            tile = py.image.load(filename)
                            tile = py.transform.scale(tile, (PIECE_SIZE, PIECE_SIZE))
                            screen.blit(tile, (x*PIECE_SIZE, y*PIECE_SIZE))
                        
                        filename = str(image_path / piece.colour.lower()) + '_' + G.PIECES[piece.type].lower() + '.png'
                        
                        piece = py.image.load(filename)
                        piece = py.transform.scale(piece, (PIECE_SIZE, PIECE_SIZE))
                        screen.blit(piece, (x*PIECE_SIZE, y*PIECE_SIZE))    
            
            if G.horse_active:
                filename = image_path / 'horse.png'
                
                tile = py.image.load(filename)
                tile = py.transform.scale(tile, (BOARD_SIZE, BOARD_SIZE))
                screen.blit(tile, (0, 0))
                
            win.flip()
    
    except KeyboardInterrupt:
        py.quit()
        return 0
    
    py.quit()
    return 0

show_board = threading.Thread(target=board_thread)
show_board.start()

while not G.game_finished:
    try:
        # Check if a white and black king exists
        white_king_exists = False
        black_king_exists = False
        
        for i in board.board:
            for j in i:
                if j != None:
                    if j.colour == 'W' and j.type == 'K':
                        white_king_exists = True
                    
                    if j.colour == 'B' and j.type == 'K':
                        black_king_exists = True
        
        # If one player does not have a king, the game ends
        if not all([white_king_exists, black_king_exists]):
            G.game_finished = True
            continue
        
        # Get coords of piece to move
        moved = False
        while not moved:
            clear()
            
            print(board.display_board())
            
            print(f'\nIt is {"WHITE" if G.turn == 1 else "BLACK"}\'s turn.')
            
            choice = input('Enter the coordinate of the piece you would like to move:\n>> ').upper()
            user_input = list(choice)
            
            if len(user_input) == 2 and user_input[0] in 'ABCDEFGH' and user_input[1] in '12345678':
                user_input[0] = G.NUMERICCOORDS[user_input[0]]
                user_input[1] = 8 - int(user_input[1])
                
                if board.get_tile(user_input[0], user_input[1]) != None:
                    if board.get_tile(user_input[0], user_input[1]).colour in [('W' if G.turn == 1 else 'B'), 'WB']:
                        
                        start_coords = user_input
                        selected_piece = board.get_tile(start_coords[0], start_coords[1])
                        
                        # Get coords of destination
                        while not moved:
                            clear()
                            
                            print(board.display_board())
                            
                            print(f'\nIt is {"WHITE" if G.turn == 1 else "BLACK"}\'s turn.')
                            
                            user_input = list(input(f'\nSelected the {G.PIECES[selected_piece.type].upper()} at {choice}.\nEnter the coordinate of the piece you would like to move:\n>> ').upper())
                            if user_input == []:
                                break
                            
                            if len(user_input) == 2 and user_input[0] in 'ABCDEFGH' and user_input[1] in '12345678':
                                user_input[0] = G.NUMERICCOORDS[user_input[0]]
                                user_input[1] = 8 - int(user_input[1])
                                
                                dest_coords = user_input
                                
                                board.move_piece(start_coords[0], start_coords[1], dest_coords[0], dest_coords[1])
                                moved = True
        
        choices = G.active_choices
        for choice in choices:
            choice.length -= 1 if choice.length != -2 else 0
            
            if choice.length == -1:
                # Expiry-based effects
                match choice.name.lower():
                    case 'hot potato':
                        for i in G.hotPotato_pieces:
                            for x in range(8):
                                for y in range(8):
                                    piece = board.get_tile(x, y)
                                    
                                    if piece != None and piece.id == i:
                                        for i in G.BOMBEXPLOSIONRADIUS:
                                            if 0 <= piece.pos[0] + i[0] < 8 and 0 <= piece.pos[1] + i[1] < 8:
                                                board.remove_piece(piece.pos[0] + i[0], piece.pos[1] + i[1])      
                    
                    case 'resistance v':
                        G.res5_pieces = []
                    
                    case 'hobbit ascendance':
                        G.hobbAsc_pieces = []
                    
                    case 'watch where you walk':
                        for i in G.wwyw_tiles:
                            board.remove_piece(i[0], i[1])
                        
                        G.wwyw_tiles.clear()
                        
                    case 'from the grave':
                        piece = board.random_tile(1)[0]
                        board.add_piece('B' if G.turn % 2 == 0 else 'W', 'Q', piece[0], piece[1])
                    
                    case 'impending doom':
                        for x in range(8):
                            for y in range(8):
                                board.remove_piece(x, y)
                    
                    case 'summoning ritual':
                        piece = board.random_tile(1)[0]
                        board.add_piece('B' if G.turn % 2 == 0 else 'W', 'Q', piece[0], piece[1])
                    
                    case 'free will':
                        G.choice_count -= 1
                    
                    case '1984':
                        G.choice_count += 1
                    
                    case 'chaos':
                        G.choice_frequency = 3
                    
                    case 'evil and intimidating horse':
                        G.horse_active = False
                
                G.active_choices.remove(choice)
        
        # Choice time!!
        if G.total_turns % G.choice_frequency == 0 and G.choice_cooldown == 0:
            choices = []
            
            for i in range(G.choice_count):
                while True:
                    selected_choice = copy(random.choice(G.CHOICES))
                    
                    if isinstance(selected_choice.length, list):
                        selected_choice.length = random.randint(selected_choice.length[0], selected_choice.length[1])
                    
                    if selected_choice.name not in [i.name for i in choices + G.active_choices]:
                        choices.append(selected_choice)
                        break
            
            picked_choice = False
            while not picked_choice:
                clear()
                
                print(f'''{'BLACK' if G.turn % 2 == 0 else 'WHITE'}, pick one of the following:\n''')
                for i, choice in enumerate(choices, start=1):
                    print(f'''{i}. {choice.name} ({(str(choice.length) + ' turns') if max(1, choice.length) == choice.length else 'Instant' if choice.length == 0 else 'Permanent'})\n   {choice.desc}\n''')
                    
                choice = input('>> ') + '_.'
                if choice[0] in '123':
                    choice = int(choice[0]) - 1
                    picked_choice = True
                
                elif choice.split('_')[0] == 'd':
                    if G.get_choice(choice.split('_')[1]) != -1:
                        picked_choice = True
            
            if isinstance(choice, str) and choice.split('_')[0] == 'd':
                selected_choice = copy(G.get_choice(choice.split('_')[1]))
                
                if isinstance(selected_choice.length, list):
                    selected_choice.length = random.randint(selected_choice.length[0], selected_choice.length[1])
            else:
                selected_choice = choices[choice]
            
            if selected_choice.name == 'THE MIMIC!!!!':
                while True:
                    selected_choice = copy(random.choice(G.CHOICES))
                    
                    if isinstance(selected_choice.length, list):
                        selected_choice.length = random.randint(selected_choice.length[0], selected_choice.length[1])
                    
                    if selected_choice.name not in [i.name for i in choices + G.active_choices]:
                        choices.append(selected_choice)
                        break
            
            G.active_choices.append(selected_choice)
            
            match selected_choice.name.lower():
                case 'hot potato':
                    while True:
                        pos = board.random_tile(n=2, count=1)[0]
                        piece = board.get_tile(pos[0], pos[1])
                        
                        if piece.type not in 'PK':
                            break
                    
                    G.hotPotato_pieces.append(piece.id)
                
                case 'sagittarius a*':
                    pos = board.random_tile(n=1, count=1)[0]
                    
                    board.add_piece('H', 'H', pos[0], pos[1])
                
                case 'absolute bliss':
                    pos = board.random_tile(n=1, count=1)[0]
                    
                    board.add_piece('M', 'M', pos[0], pos[1])
                
                case 'minesweeper':
                    for i in board.random_tile(n=1, count=random.randint(2, 5)):
                        board.add_piece('M', 'M', i[0], i[1])
                
                case 'viking invasion':
                    while True:
                        pos = board.random_tile(n=2, count=1)[0]
                        piece = board.get_tile(pos[0], pos[1])
                        
                        if piece.type != 'K':
                            break
                    
                    board.add_piece(piece.colour, 'V', piece.pos[0], piece.pos[1])
                
                case 'schrodinger\'s piece':
                    pos = board.random_tile(1, 1)[0]
                    board.add_piece('WB', 'N', pos[0], pos[1])
                
                case 'bomb defusal expert':
                    positions = board.random_tile(n=1, count=2)
                    if len(positions) < 2:
                        break

                    pos1, pos2 = positions[0], positions[1]

                    board.add_piece('A', 'A', pos1[0], pos1[1])
                    board.add_piece('C', 'C', pos2[0], pos2[1])
                
                case 'original sin':
                    pos = board.random_tile(1)[0]
                    board.add_piece('S', 'S', pos[0], pos[1])
                
                case 'bone meal':
                    pos = board.random_tile(1)[0]
                    board.add_piece('F', 'F', pos[0], pos[1])
                
                case 'switcharoo':
                    pieces = board.random_tile(n=2, count=2)
                    piece1 = board.get_tile(pieces[0][0], pieces[0][1])
                    piece2 = board.get_tile(pieces[1][0], pieces[1][1])
                    
                    piece1.pos, piece2.pos = piece2.pos, piece1.pos
                    
                    for piece in [piece1, piece2]:
                        board.add_piece(piece.colour, piece.type, piece.pos[0], piece.pos[1])
                
                case 'resistance v':
                    while True:
                        pieces = board.random_tile(n=2, count=2)
                        pieces = [board.get_tile(i[0], i[1]) for i in pieces]
                    
                        if all([(piece.colour == 'W' if G.turn % 2 == 0 else 'B') for piece in pieces]):
                            if all([(piece.type != 'K') for piece in pieces]):
                                
                                for piece in pieces:
                                    G.res5_pieces.append(piece.id)
                                
                                break
                
                case 'standoff':
                    while True:
                        pieces = board.random_tile(n=2, count=2)
                        pieces = [board.get_tile(i[0], i[1]) for i in pieces]
                        
                        if all([(piece.type != 'K') for piece in pieces]):
                            if pieces[0].colour != pieces[1].colour:
                            
                                for piece in pieces:
                                    G.marked_pieces.append(piece.id)
                                
                                break
                
                case 'march of the pawnguins':
                    moved_pieces = []
                    
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None and piece.type == 'P':
                                if piece.id not in moved_pieces:

                                    if piece.colour == 'W':
                                        if board.get_tile(x, y-1) == None:
                                            board.move_piece(x, y, x, y-1)
                                            
                                            moved_pieces.append(piece.id)
                                    else:
                                        if board.get_tile(x, y+1) == None:
                                            board.move_piece(x, y, x, y+1)
                                        
                                            moved_pieces.append(piece.id)
                
                case 'hobbit dance':
                    pawns = []
                    
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None and piece.type == 'P' and piece.id not in pawns:
                                pawns.append(piece.id)
                                
                                pos = board.random_tile(1)[0]
                                board.move_piece(x, y, pos[0], pos[1])
                
                case 'hobbit conglomerate':
                    pawns = []
                    
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                                
                            if piece != None and piece.type == 'P' and piece.colour == 'W' if G.turn % 2 == 0 else 'B':
                                pawns.append([x, y])
                    
                    for i in random.sample(pawns, 4):
                        board.remove_piece(i[0], i[1])
                    
                    for i in random.sample(pawns, 1):
                        board.add_piece('W' if G.turn % 2 == 0 else 'B', 'Q', i[0], i[1])
                
                case 'hobbit tragedy':
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None and piece.type == 'P':
                                board.remove_piece(x, y)
                
                case 'hobbit revolution':
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None and piece.type not in 'PK':
                                board.add_piece(piece.colour, 'P', piece.pos[0], piece.pos[1])
                
                case 'hobbit undercover':
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None and piece.type == 'P':
                                board.add_piece(piece.colour, random.choice(['R', 'B', 'N']), piece.pos[0], piece.pos[1])
                
                case 'hobbit ascendance':
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None and piece.type == 'P':
                                G.hobbAsc_pieces.append(piece.id)
                
                case 'watch where you walk':
                    G.wwyw_tiles = board.random_tile(0, 5)
                
                case 'row swap':
                    columns = [random.randint(0, 7), random.randint(0, 7)]
                    
                    board.board[columns[0]], board.board[columns[1]] = board.board[columns[1]], board.board[columns[0]]
                
                case 'the roooooook':
                    pos = board.random_tile(1, 1)[0]
                    
                    board.add_piece('W' if G.turn % 2 == 0 else 'B', 'R', pos[0], pos[1])
                
                case 'sacrifice the rook':
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None and piece.type == 'R':
                                board.remove_piece(x, y)
                
                case '45-degree rotation':
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None and piece.type in 'RB':
                                board.add_piece(piece.colour, ('R' if piece.type == 'B' else 'B'), x, y)
                
                case 'they deserved it':
                    while True:
                        pos = board.random_tile(2, 1)[0]
                        
                        if board.get_tile(pos[0], pos[1]).type != 'K':
                            break
                    
                    board.remove_piece(pos[0], pos[1])
                
                case 'promotion':
                    pawns = []
                    
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None and piece.type == 'P':
                                pawns.append(piece)
                    
                    for pawn in random.sample(pawns, random.randint(2, 4)):
                        board.add_piece(pawn.colour, 'N', pawn.pos[0], pawn.pos[1])
                
                case 'general election':
                    while True:
                        pos = board.random_tile(2, 1)[0]
                        
                        if board.get_tile(pos[0], pos[1]).type not in 'KQ':
                            break
                    
                    piece = board.get_tile(pos[0], pos[1])
                    
                    board.add_piece(piece.colour, 'Q', pos[0], pos[1])
                
                case 'the royal family':
                    tiles = board.random_tile(1, 2)
                    
                    for i in tiles:
                        board.add_piece('W' if tiles.index(i) else 'B', 'K', i[0], i[1])
                
                case 'from the grave':
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None and piece.colour == ('B' if G.turn % 2 == 0 else 'W') and piece.type == 'Q':
                                board.remove_piece(x, y)
                
                case 'nuke':
                    piece = board.random_tile(n=2, count=1)[0]
                    
                    for i in G.BOMBEXPLOSIONRADIUS:
                        if 0 <= piece[0] + i[0] < 8 and 0 <= piece[1] + i[1] < 8:
                            board.remove_piece(piece[0] + i[0], piece[1] + i[1])
                
                case 'gambling':
                    if random.random() < 0.5:
                        piece = board.random_tile(1)[0]
                        
                        board.add_piece('W' if G.turn % 2 == 0 else 'B', 'R', piece[0], piece[1])
                    
                    if random.random() < 0.25:
                        piece = board.random_tile(1)[0]
                        
                        board.add_piece('B' if G.turn % 2 == 0 else 'W', 'R', piece[0], piece[1])
                
                case 'earthquake':
                    for i in board.board:
                        random.shuffle(i)
                
                case 'mirror dimension':
                    for i in board.board:
                        i.reverse()
                
                case 'casino royale':
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None and piece.type in 'PRNBQ':
                                board.add_piece(piece.colour, random.choice('PRNBQ'), x, y)
                
                case 'extinction':
                    for i in [random.choice('PRNBQ')]:
                        for x in range(8):
                            for y in range(8):
                                piece = board.get_tile(x, y)
                                
                                if piece != None and piece.type == i:
                                    board.remove_piece(x, y)
                
                case 'trojan horse':
                    knights = []
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None:
                                if piece.colour == ('W' if G.turn % 2 == 0 else 'B') and piece.type == 'N':
                                    knights.append(piece)
                    
                    if knights:
                        piece = random.sample(knights, 1)[0]
                        
                        board.remove_piece(piece.pos[0], piece.pos[1])
                        pos = board.random_tile(1, random.randint(3, 5))
                        
                        for i in pos:
                            board.add_piece('W' if G.turn % 2 == 0 else 'B', 'P', i[0], i[1])
                
                case 'free will':
                    G.choice_count += 1
                
                case '1984':
                    G.choice_count -= 1
                
                case 'chaos':
                    G.choice_frequency = 1
                
                case 'cheater':
                    G.total_turns -= 1; G.turn -= 1
                    G.choice_cooldown = 2
                
                case 'take a breather':
                    G.choice_cooldown = selected_choice.length + 1
                
                case 'evil and intimidating horse':
                    G.horse_active = True
        
        # Special piece code
        moved_rats = []
        moved_snakes = []
        for x in range(8):
            for y in range(8):
                piece = board.get_tile(x, y)
                
                if piece != None and piece.type == 'H':
                    for i in G.BOMBEXPLOSIONRADIUS:
                        if 0 <= piece.pos[0] + i[0] < 8 and 0 <= piece.pos[1] + i[1] < 8:
                            
                            # Black hole doesn't blow up itself
                            if i[0] != 0 or i[1] != 0:
                                board.remove_piece(piece.pos[0] + i[0], piece.pos[1] + i[1])
                
                
                if piece != None and piece.type == 'A' and piece.id not in moved_rats:
                    cheese_positions = []
                    cheese_distances = []
                    
                    for i in range(8):
                        for j in range(8):
                            cheese = board.get_tile(i, j)
                            
                            if cheese != None and cheese.type == 'C':
                                cheese_positions.append([i, j])
                    
                    if cheese_positions:
                        # The formula used here was googled
                        target = min(cheese_positions, key=lambda c: abs(c[0] - x) + abs(c[1] - y))
                        
                        offset = [target[0] - x, target[1] - y]
                        
                        # This was also googled
                        offset[0] = (offset[0] > 0) - (offset[0] < 0)
                        offset[1] = (offset[1] > 0) - (offset[1] < 0)
                        
                        board.move_piece(x, y, x + offset[0], y + offset[1])
                        moved_rats.append(piece.id)
                
                if piece != None and piece.type == 'S':
                    while True:
                        pos = random.choice(G.BOMBEXPLOSIONRADIUS)
                        
                        if (0 <= x + pos[0] <= 7) and (0 <= y + pos[1] <= 7):
                            break
                    
                    board.move_piece(x, y, x + pos[0], y + pos[1])
                    moved_snakes.append(piece.id)
        
        for choice in [choice.name.lower() for choice in G.active_choices]:
            match choice:
                case 'wizard of teleportation and cruelty':
                    pos = board.random_tile(2)[0]
                    pos2 = board.random_tile(1)[0]
                    
                    print(pos)
                    board.move_piece(pos[0], pos[1], pos2[0], pos2[1])
                
                case 'standoff':
                    marked_count = 0
                    for x in range(8):
                        for y in range(8):
                            piece = board.get_tile(x, y)
                            
                            if piece != None and piece.id in G.marked_pieces:
                                marked_count += 1
                    
                    if marked_count < 2:
                        G.marked_pieces.clear()
                        
                        for choice in G.active_choices:
                            if choice.name.lower() == 'standoff':
                                G.active_choices.remove(choice)
                                break
                
                case 'the plague':
                    while True:
                        piece = board.random_tile(2)[0]
                        
                        if board.get_tile(piece[0], piece[1]).type != 'K':
                            break
                    
                    board.remove_piece(piece[0], piece[1])
        
        if G.choice_cooldown > 0:
            G.choice_cooldown -= 1
        
        # Promotion stuff
        for x in range(8):
            for y in range(8):
                piece = board.get_tile(x, y)
                
                if piece != None and piece.type == 'P':
                    if (piece.colour == 'W' and y == 0) or (piece.colour == 'B' and y == 7):
                        board.add_piece(piece.colour, 'Q', x, y)
        
        G.total_turns += 1
        G.turn = (G.total_turns % 2)
        
    except KeyboardInterrupt:
        G.game_finished = True

clear()
if white_king_exists and not black_king_exists:
    print(f'{board.display_board()}\n\nWHITE WINS!')

elif black_king_exists and not white_king_exists:
    print(f'{board.display_board()}\n\nBLACK WINS!')

else:
    print(f'{board.display_board()}\n\nDRAW!')

print('Press ENTER to exit. Thanks for playing!')
input()

close_board = True