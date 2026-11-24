import random


'''

CHOICES TO ADD:

'''


class Choice:
    def __init__(self, name, desc, length):
        self.name = name
        self.desc = desc
        self.length = length

NEWLINE = '\n   '
CHOICES = [
    Choice(
        name = 'Nothing',
        desc = 'Does nothing.',
        length = 0
    ),
    Choice(
        name = 'Hot Potato',
        desc = f'A random non-pawn/king piece gets a live bomb.{NEWLINE}' \
               f'When this piece is captured, pass the bomb over and reset this choice\'s length.{NEWLINE}' \
                'When this choice expires, blow up the piece with the bomb.',
        length = 7
    ),
    Choice(
        name = 'Sagittarius A*',
        desc = f'Adds a black hole to a random unoccupied space.{NEWLINE}' \
                'The Black hole cannot be captured. If a piece is adjacent to the black hole, it is captured.',
        length = 0
    ),
    Choice(
        name = 'Absolute Bliss',
        desc = 'Adds a bomb to a random unoccupied space.',
        length = 0
    ),
    Choice(
        name = 'Minesweeper',
        desc = 'Adds 2-5 bombs to unoccupied spaces.',
        length = 0
    ),
    Choice(
        name = 'Curse of the Tower',
        desc = 'When a piece is captured, add 6 bombs to random unoccupied spaces.',
        length = [3, 7]
    ),
    Choice(
        name = 'Ragnarok',
        desc = f'Converts a random non-king piece into a viking.{NEWLINE}' \
                'A viking can move either 1 or 2 spaces left, right, up or down, or 1 space diagonally.',
        length = 0
    ),
    Choice(
        name = 'Schrodinger\'s Piece',
        desc = f'Adds a knight to a random unoccupied space. This knight can be controlled by both teams.{NEWLINE}(Knight shown in red)',
        length = 0
    ),
    Choice(
        name = 'Bomb Defusal Expert',
        desc = f'Adds a rat and cheese to the board.{NEWLINE}The rat will move towards the cheese every turn, capturing any pieces in its way.',
        length = 0
    ),
    Choice(
        name = 'Original Sin',
        desc = 'Adds a snake to the board. The snake cannot be captured.',
        length = 0
    ),
    Choice(
        name = 'Bone Meal',
        desc = 'A random unoccupied tile grows a forest. No piece can enter/cross this tile.',
        length = 0
    ),
    Choice(
        name = 'Switcharoo',
        desc = 'Swaps two random pieces.',
        length = 0
    ),
    Choice(
        name = 'Mind Control',
        desc = 'A random enemy piece is converted into your colour.',
        length = 0
    ),
    Choice(
        name = 'Level Up',
        desc = f'Capturing a piece converts the capturer upwards in quality.{NEWLINE}(Pawn > Knight > Bishop > Rook > Queen)',
        length = [4, 9]
    ),
    Choice(
        name = 'Wizard of Teleportation and Cruelty',
        desc = 'Every turn, a random piece is teleported to a random unoccupied tile.',
        length = [5, 10]
    ),
    Choice(
        name = 'Oestrogen',
        desc = 'Kings can move like queens.',
        length = [3, 7]
    ),
    Choice(
        name = 'Testostorone',
        desc = 'The other team\'s queen(s) can only move like kings.',
        length = [3, 7]
    ),
    Choice(
        name = 'Exercise',
        desc = 'Pawns can move 2 spaces forward at any point.',
        length = [4, 8]
    ),
    Choice(
        name = 'Resistance V',
        desc = f'Two random pieces on your team become immortal, excluding the king.{NEWLINE}(Immortality shown in green)',
        length = [2, 4]
    ),
    Choice(
        name = 'Standoff',
        desc = f'Two random non-king pieces become marked. From now on, those pieces can only be killed by each other.{NEWLINE}(Marked pieces shown in pink)',
        length = -2
    ),
    Choice(
        name = 'March of the Pawnguins',
        desc = 'All pawns move forwards one space, if possible.',
        length = 0
    ),
    Choice(
        name = 'Hobbit Battle',
        desc = 'Only pawns can be moved.',
        length = [2, 4]
    ),
    Choice(
        name = 'Hobbit Slaughter',
        desc = 'Only pawns can be killed.',
        length = [2, 4]
    ),
    Choice(
        name = 'Hobbit Terror',
        desc = 'Pawns can move backwards.',
        length = [5, 9]
    ),
    Choice(
        name = 'Hobbit Dance',
        desc = 'All pawns are moved to random spaces on the board.',
        length = 0
    ),
    Choice(
        name = 'Hobbit Conglomerate',
        desc = '5 of your pawns are killed and replaced by a queen.',
        length = 0
    ),
    Choice(
        name = 'Hobbit Tragedy',
        desc = 'All pawns die.',
        length = 0
    ),
    Choice(
        name = 'Hobbit Revolution',
        desc = 'All non-king pieces are converted into pawns.',
        length = 0
    ),
    Choice(
        name = 'Hobbit Lobotomy',
        desc = 'Pawns move diagonally and capture vertically.',
        length = [4, 7]
    ),
    Choice(
        name = 'Hobbit Undercover',
        desc = 'All pawns are converted into a rook, bishop or knight.',
        length = 0
    ),
    Choice(
        name = 'Hobbit Ascendance',
        desc = 'All pawns become immortal.',
        length = [3, 6]
    ),
    Choice(
        name = 'Watch Where You Walk',
        desc = f'5 tiles are selected (Shown in blue).{NEWLINE}When this expires, pieces on those tiles die.',
        length = [4, 7]
    ),
    Choice(
        name = 'Row Swap',
        desc = 'Two rows are swapped.',
        length = 0
    ),
    Choice(
        name = 'THE ROOOOOOOK',
        desc = 'A friendly rook is added to an unoccupied space.',
        length = 0
    ),
    Choice(
        name = 'Sacrifice the Rook',
        desc = 'All rooks are killed.',
        length = 0
    ),
    Choice(
        name = 'Regicide',
        desc = 'All queens are killed.',
        length = 0
    ),
    Choice(
        name = '45-Degree Rotation',
        desc = 'All rooks are converted into bishops, and bishops into rooks.',
        length = 0
    ),
    Choice(
        name = 'Ice Physics',
        desc = 'Bishops, rooks and queens must move their maxiumum distance.',
        length = [5, 9]
    ),
    Choice(
        name = 'Ice Age',
        desc = 'You cannot move or capture any pieces on the outer ring of the board.',
        length = [3, 4]
    ),
    Choice(
        name = 'No Cowards',
        desc = 'No moves that move pieces backwards.',
        length = [3, 5]
    ),
    Choice(
        name = 'Long Arms',
        desc = 'Pawns can capture directly left and right.',
        length = [4, 7]
    ),
    Choice(
        name = 'They Deserved It',
        desc = 'One random non-king piece is killed.',
        length = 0
    ),
    Choice(
        name = 'Promotion',
        desc = '2-4 Random pawns are converted into knights.',
        length = 0
    ),
    Choice(
        name = 'General Election',
        desc = 'One random non-king piece is converted into a queen.',
        length = 0
    ),
    Choice(
        name = 'Soul Link',
        desc = 'When a piece is captured, all pieces of that type die too, excluding kings.',
        length = [5, 8]
    ),
    Choice(
        name = 'Down With The Ship',
        desc = 'When a piece is captured, the capturing piece dies too.',
        length = [4, 7]
    ),
    Choice(
        name = 'Kamikaze',
        desc = 'Any captured pieces explode. The capturing piece is immune to the explosion.',
        length = [3, 8]
    ),
    Choice(
        name = 'Necromancy',
        desc = 'When you capture a piece, spawn a friendly pawn in an unoccupied space.',
        length = [4, 8]
    ),
    Choice(
        name = 'Vampirism',
        desc = 'When you capture a piece, the capturing piece is converted into the captured piece\'s type.',
        length = [5, 10]
    ),
    Choice(
        name = 'Second Chance',
        desc = 'When a piece is captured, 1/2 chance for it to respawn.',
        length = [5, 10]
    ),
    Choice(
        name = 'Cardiac Arrest',
        desc = 'When a piece moves, 1/5 chance for it to die.',
        length = [3, 6]
    ),
    Choice(
        name = 'Dead God Cult',
        desc = 'When a peice moves, 1/5 chance for it to convert into a bishop.',
        length = [3, 6]
    ),
    Choice(
        name = 'The Royal Family',
        desc = f'Both teams gain a new king in a random empty space.{NEWLINE}All kings must be killed before the game can be won.',
        length = 0
    ),
    Choice(
        name = 'From The Grave',
        desc = 'All enemy queen(s) are killed. When this expires, the enemy team gains a queen.',
        length = 5
    ),
    Choice(
        name = 'Nuke',
        desc = f'Immediately blow up a random piece.{NEWLINE}The explosion will kill any pieces next to the chosen one.',
        length = 0
    ),
    Choice(
        name = 'Gambling',
        desc = f'50% Chance for a free rook in a random empty square.{NEWLINE}Your opponent gets a 25% chance for the same thing.',
        length = 0
    ),
    Choice(
        name = 'Russian Roulette',
        desc = f'When a piece is moved, 1/6 chance to convert it into a queen, and 1/6 chance for it to die.{NEWLINE}Affects kings.',
        length = [4, 7]
    ),
    Choice(
        name = 'Slippery Floor',
        desc = 'When a piece moves, 1/3 chance for it to move somewhere random.',
        length = [3, 6]
    ),
    Choice(
        name = 'The Plague',
        desc = 'One random non-king piece dies every turn.',
        length = [3, 5]
    ),
    Choice(
        name = 'Impending Doom',
        desc = 'When this choice expires, kill EVERY piece.',
        length = [10, 20]
    ),
    Choice(
        name = '+PARRY',
        desc = 'When capturing a piece, 25% chance for the attacker to be killed instead.',
        length = [4, 8]
    ),
    Choice(
        name = 'Earthquake',
        desc = 'Shuffles all rows.',
        length = 0
    ),
    Choice(
        name = 'Mirror Dimension',
        desc = 'Flips the board horizontally.',
        length = 0
    ),
    Choice(
        name = 'Summoning Ritual',
        desc = f'When this expires, add a friendly queen to a random space on the board.{NEWLINE}Disables if any piece dies before this expires.',
        length = 5
    ),
    Choice(
        name = 'Casino Royale',
        desc = 'Every non-king piece is randomly converted into another piece.',
        length = 0
    ),
    Choice(
        name = 'Extinction',
        desc = 'Every piece of a random non-king type dies.',
        length = 0
    ),
    Choice(
        name = 'Trojan Horse',
        desc = 'Destroy a random one of your knights, and replace it with 3-5 pawns.',
        length = 0
    ),
    Choice(
        name = 'Free Will',
        desc = '+1 Option when selecting a choice.',
        length = [5, 13]
    ),
    Choice(
        name = '1984',
        desc = '-1 Option when selecting a choice.',
        length = [5, 13]
    ),
    Choice(
        name = 'Chaos',
        desc = 'Choices will occur every turn.',
        length = [2, 5]
    ),
    Choice(
        name = 'Cheater',
        desc = 'Gain an extra turn.',
        length = 0
    ),
    Choice(
        name = 'Take A Breather',
        desc = 'All choices are paused for the duration of this choice.',
        length = [4, 8]
    ),
    Choice(
        name = 'Killstreak',
        desc = 'If you capture a piece, gain another turn.',
        length = [3, 9]
    ),
    Choice(
        name = 'Evil and Intimidating Horse',
        desc = 'Adds a horse which blocks the board.',
        length = [3, 6]
    ),
    Choice(
        name = 'THE MIMIC!!!!',
        desc = 'Turns into a random other effect.',
        length = 0
    )
]

def choices():
    return CHOICES

if __name__ == '__main__':
    print(len(CHOICES))