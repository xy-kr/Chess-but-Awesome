import _Choices as Choices
import random

class Piece:
    '''Class for placing pieces on the board.'''
    
    def __init__(self, colour, type, x, y, id):
        self.colour = colour
        self.type = type
        self.pos = [x, y]
        
        self.id = id

class Board:
    '''Class which handles things directly on the board.'''
    
    def __init__(self, game_ref):
        self.game = game_ref
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.pieces_created = 0
    
    def display_board(self):
        '''Returns a string of the current board.'''
        
        board_string = ''
        if self.game.active_choices:
            for choice in self.game.active_choices:
                board_string += f"\n\n>> {choice.name} ({'Infinite' if choice.length == -2 else choice.length} Turns Left)\n   {choice.desc}"
        
        '''
        board_string += '\n\n   A B C D E F G H\n\n'
        for y in range(8):
            row = str(8 - y) + '  '
            for x in range(8):
                piece = self.get_tile(x, y)
                bgcolour = '' 
                fgcolour = ''
                text = ''
                
                if piece is None:
                    text = '-'
                    fgcolour = self.game.COLOURS['dark_grey']
                else:
                    text = piece.type
                    
                    if piece.id in (self.game.res5_pieces + self.game.hobbAsc_pieces):
                        bgcolour = self.game.BGCOLOURS['green']
                    
                    elif piece.id in self.game.marked_pieces:
                        bgcolour = self.game.BGCOLOURS['pink']
                    
                    if piece.colour == 'W':
                        fgcolour = self.game.COLOURS['white']
                    elif piece.colour == 'B':
                        fgcolour = self.game.COLOURS['grey']
                    
                    elif piece.colour == 'WB':
                        fgcolour = self.game.COLOURS['red']
                    
                    elif piece.colour == 'H':
                        fgcolour = self.game.COLOURS['black']
                    elif piece.colour == 'M':
                        fgcolour = self.game.COLOURS['red']
                
                if [x, y] in self.game.wwyw_tiles:
                    bgcolour = self.game.BGCOLOURS['blue']
                        
                row += f'{bgcolour}{fgcolour}{text}\x1b[0m '
            board_string += f'{row}\n'
        
        '''
        return board_string

    def get_tile(self, x, y):
        '''Returns the object currently on coordinate (x, y).'''
        
        if 0 <= x < 8 and 0 <= y < 8:
            return self.board[y][x]
        return None
    
    def random_tile(self, n=0, count=1):
        '''Returns a list of positions of tiles of type n which are occupied/unoccupied.
    n = 0: Both occupied and unoccupied.
    n = 1: Unoccupied only.
    n = 2: Occupied only.'''
        
        tiles = []
        for i in range(count):
            while True:                
                x, y = random.randint(0, 7), random.randint(0, 7)
                tile = self.get_tile(x, y)
                        
                if [x, y] not in tiles:
                    if n == 0:
                        tiles.append([x, y])
                        break
                    
                    elif n == 1 and tile == None:
                        tiles.append([x, y])
                        break
                    
                    elif n == 2 and tile != None:
                        tiles.append([x, y])
                        break
        
        return tiles

    def add_piece(self, _colour, _type, x, y):
        '''Adds a piece onto the board.'''
        
        self.board[y][x] = Piece(_colour, _type, x, y, self.pieces_created)
        self.pieces_created += 1

    def move_piece(self, start_x, start_y, dest_x, dest_y):
        '''Moves a pieces from (start_x, start_y) to (dest_x, dest_y).'''
        
        piece = self.get_tile(start_x, start_y)
        destination = self.get_tile(dest_x, dest_y)
        
        if piece is None:
            return False
            
        self.board[start_y][start_x] = None
        
        piece.pos = [dest_x, dest_y]
        self.board[dest_y][dest_x] = piece
        
        if destination != None:
            # Capture-based effects
            for choice in self.game.active_choices:
                match choice.name.lower():
                    case 'hot potato':
                        if destination.id in self.game.hotPotato_pieces:
                            choice.length = 7
                            
                            self.game.hotPotato_pieces[self.game.hotPotato_pieces.index(destination.id)] = piece.id
                    
                    case 'level up':
                        if destination.type in 'PNBRQK':
                            piece.type = 'PNBRQQ'['PNBRQQ'.index(piece.type) + 1]
                    
                    case 'soul link':
                        for x in range(8):
                            for y in range(8):
                                _piece = self.get_tile(x, y)
                                
                                if _piece != None and _piece.type == destination.type:
                                    self.remove_piece(x, y)
                    
                    case 'down with the ship':
                        self.remove_piece(dest_x, dest_y)
                    
                    case 'kamikaze':
                        for i in self.game.BOMBEXPLOSIONRADIUS:
                            if 0 <= piece.pos[0] + i[0] < 8 and 0 <= piece.pos[1] + i[1] < 8:
                                
                                if i[0] != 0 or i[1] != 0:
                                    self.remove_piece(piece.pos[0] + i[0], piece.pos[1] + i[1])
                    
                    case '+parry':
                        if random.random() < 0.25:
                            self.add_piece(destination.colour, destination.type, dest_x, dest_y)
                    
                    case 'summoning ritual':
                        self.game.active_choices.remove(self.game.get_choice('Summoning Ritual'))
                    
                    case 'curse of the tower':
                        for i in self.random_tile(1, 6):
                            self.add_piece('M', 'M', i[0], i[1])
                    
                    case 'killstreak':
                        self.game.total_turns -= 1; self.game.turn -= 1
                        self.game.choice_cooldown += (1 if self.game.choice_cooldown != 0 else 2)
            
            # Spawn a new cheese when one is captured
            if destination.type == 'C':
                pos = self.random_tile(1)[0]
                self.add_piece('C', 'C', pos[0], pos[1])
        
        # General movement effects
        for choice in self.game.active_choices:
            match choice.name.lower():
                case 'cardiac arrest':
                    if random.random() < 0.2:
                        self.remove_piece(dest_x, dest_y)
                
                case 'dead god cult':
                    if random.random() < 0.2:
                        self.add_piece(piece.colour, 'B', dest_x, dest_y)
                    
                case 'russian roulette':
                    if random.randint(1, 6) == 1:
                        self.add_piece(piece.colour, 'Q', dest_x, dest_y)
                    
                    if random.randint(1, 6) == 1:
                        self.remove_piece(dest_x, dest_y)
        
        if destination != None and destination.type == 'M' and piece.type != 'A':
            for i in self.game.BOMBEXPLOSIONRADIUS:
                if 0 <= destination.pos[0] + i[0] < 8 and 0 <= destination.pos[1] + i[1] < 8:
                    self.board[destination.pos[1] + i[1]][destination.pos[0] + i[0]] = None
        
        return True
    
    def remove_piece(self, x, y):
        '''Removes a piece from the board.'''
        
        self.board[y][x] = None

    def setup(self):
        '''Automatically sets up the board as a normal chess board.'''
        
        self.board = [[None for _ in range(8)] for _ in range(8)]
        
        for pawn in range(8):
            self.add_piece('B', 'P', pawn, 1) 
            self.add_piece('W', 'P', pawn, 6)

        self.add_piece('B', 'R', 0, 0); self.add_piece('B', 'R', 7, 0)
        self.add_piece('B', 'N', 1, 0); self.add_piece('B', 'N', 6, 0)
        self.add_piece('B', 'B', 2, 0); self.add_piece('B', 'B', 5, 0)
        self.add_piece('B', 'Q', 3, 0); self.add_piece('B', 'K', 4, 0)

        self.add_piece('W', 'R', 0, 7); self.add_piece('W', 'R', 7, 7)
        self.add_piece('W', 'N', 1, 7); self.add_piece('W', 'N', 6, 7)
        self.add_piece('W', 'B', 2, 7); self.add_piece('W', 'B', 5, 7)
        self.add_piece('W', 'Q', 3, 7); self.add_piece('W', 'K', 4, 7)


class Game:
    '''Class which contains any variables / constants.'''
    
    def __init__(self):
        self.COLOURS = {
            'black': '\x1b[30m',
            'grey': '\x1b[90m',
            'dark_grey': '\x1b[90m' + '\x1b[2m',
            'white': '\x1b[37m',
            'red': '\x1b[31m'
        }
        self.BGCOLOURS = {
            'green': '\x1b[42m',
            'blue': '\x1b[44m',
            'pink': '\x1b[45m',
            'reset': '\x1b[49m' + '\x1b[0m'
        }
        self.PIECES = {
            'P': 'Pawn',
            'R': 'Rook',
            'N': 'Knight',
            'B': 'Bishop',
            'Q': 'Queen',
            'K': 'King',
            'V': 'Viking',
            'A': 'Rat',
            'C': 'Cheese',
            'S': 'Snake',
            'F': 'Forest',
            'H': 'Black Hole',
            'M': 'Mine',
        }
        
        self.NUMERICCOORDS = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
            'F': 5,
            'G': 6,
            'H': 7
        }
        
        self.BOMBEXPLOSIONRADIUS = [
            [-1,  1], [ 0,  1], [ 1,  1],
            [-1,  0], [ 0,  0], [ 1,  0],
            [-1, -1], [ 0, -1], [ 1, -1]
        ]
        
        self.game_finished = False
        
        self.CHOICES = Choices.choices()
        self.choice_frequency = 3
        self.choice_count = 3
        self.active_choices = []
        self.choice_cooldown = 0
        
        self.res5_pieces = []
        self.hobbAsc_pieces = []
        self.marked_pieces = []
        self.wwyw_tiles = []
        self.hotPotato_pieces = []
        
        self.horse_active = False
        
        self.total_turns = 1
        self.turn = 1
    
    def get_choice(self, name):
        '''Returns choice with given name. Returns -1 if choice is not found.'''
        
        for choice in self.CHOICES:
            if choice.name.lower() == name.lower():
                return choice
        
        return -1