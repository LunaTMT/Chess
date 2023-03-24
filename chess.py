#import pygame
import numpy as np
from termcolor import colored
import os
import time

class Player:

    def __init__(self, pawn_pos, knight_pos, rook_pos, bishop_pos, queen_pos, king_pos,  player_name, piece_sym):
        self.piece_sym = piece_sym

        self.P1 = Pawn(pawn_pos[0], player_name, 'P1', piece_sym[0])
        self.P2 = Pawn(pawn_pos[1], player_name, 'P2', piece_sym[0])
        self.P3 = Pawn(pawn_pos[2], player_name, 'P3', piece_sym[0])
        self.P4 = Pawn(pawn_pos[3], player_name, 'P4', piece_sym[0])
        self.P5 = Pawn(pawn_pos[4], player_name, 'P5', piece_sym[0])
        self.P6 = Pawn(pawn_pos[5], player_name, 'P6', piece_sym[0])
        self.P7 = Pawn(pawn_pos[6], player_name, 'P7', piece_sym[0])
        self.P8 = Pawn(pawn_pos[7], player_name, 'P8', piece_sym[0])

        self.KN1 = Knight(knight_pos[0], player_name, 'Kn1', piece_sym[1])
        self.KN2 = Knight(knight_pos[1], player_name, 'Kn2', piece_sym[1])

        self.R1 = Rook(rook_pos[0], player_name, 'R1', piece_sym[2])
        self.R2 = Rook(rook_pos[1], player_name, 'R2', piece_sym[2])

        self.B1 = Bishop(bishop_pos[0], player_name, 'B1', piece_sym[3])
        self.B2 = Bishop(bishop_pos[1], player_name, 'B2', piece_sym[3])

        self.Q = Queen(queen_pos, player_name, 'Q', piece_sym[4])
        self.K = King(king_pos, player_name, 'K', piece_sym[5])

        self.name = player_name
        self.pieces = self.piece_set()
        self.taken = []
        self.checked = False
        self.checkmate = False
        self.all_valid_moves =  [(piece.valid_moves(), piece) for row in self.pieces for piece in row]
        
        self.possibile_attacks = np.zeros((8,8))
    

    def __str__(self):
        return f"Turn: Player {self.name}"

    def piece_set(self):
        if self.name == "1":
            return[
                [self.R1, self.KN1, self.B1, self.K, self.Q, self.B2,  self.KN2,  self.R2],
                [self.P1,  self.P2,  self.P3, self.P4, self.P5, self.P6, self.P7,  self.P8]]
        else:
            return[
                [self.P1,  self.P2,  self.P3, self.P4, self.P5, self.P6, self.P7,  self.P8],
                [self.R1, self.KN1, self.B1, self.K, self.Q, self.B2,  self.KN2,  self.R2]]
    def print_pieces(self):

        if self.checked == True:
            print("\n         You're in Check")
            for row in self.pieces:
                print()
                for piece in row:
                    print(f'  {piece.name} ' if isinstance(piece, King) else f'  _ ', end="")
            print()
        else:
            for row in self.pieces:
                print()
                for piece in row:
                    print(f' {piece.name} ' if isinstance(piece, Piece) else f'  _ ', end="")
            print()

    def valid_piece(self, obj_name):
        if hasattr(self, obj_name) and self.get_piece(obj_name).alive == True:
            for row in self.pieces:
               if obj_name in row:
                   return False
            return True
    def get_valid_moves(self, piece):
        if isinstance(piece, Piece):
            return piece.valid_moves()
        else:
            False
   
    def get_piece(self, piece_name):
        return getattr(self, piece_name)       
    def update_piece(self, piece, position):
        if isinstance(piece, King):
            self.checked = False
            
        piece.position = position 
        piece.movements += 1 
    def remove_piece(self, position):
        for (i, j), piece in np.ndenumerate(self.pieces):
            if isinstance(piece, Piece):
                if  piece.position == position:
                    self.pieces[i][j] = piece.name
                    piece.alive = False
                    return piece.name

    def update_taken(self, piece):
        self.taken.append([piece, getattr(self, piece.upper()).sym])
    def print_taken(self):
        if self.taken:
            print("\n      Taken     ")
            print("----------------")
            print("|  Name | Sym  |")
            for piece in self.taken:
                print(f"|   {piece[0]}  |  {piece[1]}   |")
    
    def win(self):
        if "K" in [x for (x, _) in self.taken]:
            if self.name == "1":
                print("""
                    ██████╗░██╗░░░░░░█████╗░██╗░░░██╗███████╗██████╗░  ░░███╗░░  ░██╗░░░░░░░██╗██╗███╗░░██╗░██████╗
                    ██╔══██╗██║░░░░░██╔══██╗╚██╗░██╔╝██╔════╝██╔══██╗  ░████║░░  ░██║░░██╗░░██║██║████╗░██║██╔════╝
                    ██████╔╝██║░░░░░███████║░╚████╔╝░█████╗░░██████╔╝  ██╔██║░░  ░╚██╗████╗██╔╝██║██╔██╗██║╚█████╗░
                    ██╔═══╝░██║░░░░░██╔══██║░░╚██╔╝░░██╔══╝░░██╔══██╗  ╚═╝██║░░  ░░████╔═████║░██║██║╚████║░╚═══██╗
                    ██║░░░░░███████╗██║░░██║░░░██║░░░███████╗██║░░██║  ███████╗  ░░╚██╔╝░╚██╔╝░██║██║░╚███║██████╔╝
                    ╚═╝░░░░░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝  ╚══════╝  ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░""")
            else:
                print("""
                    ██████╗░██╗░░░░░░█████╗░██╗░░░██╗███████╗██████╗░  ██████╗░  ░██╗░░░░░░░██╗██╗███╗░░██╗░██████╗
                    ██╔══██╗██║░░░░░██╔══██╗╚██╗░██╔╝██╔════╝██╔══██╗  ╚════██╗  ░██║░░██╗░░██║██║████╗░██║██╔════╝
                    ██████╔╝██║░░░░░███████║░╚████╔╝░█████╗░░██████╔╝  ░░███╔═╝  ░╚██╗████╗██╔╝██║██╔██╗██║╚█████╗░
                    ██╔═══╝░██║░░░░░██╔══██║░░╚██╔╝░░██╔══╝░░██╔══██╗  ██╔══╝░░  ░░████╔═████║░██║██║╚████║░╚═══██╗
                    ██║░░░░░███████╗██║░░██║░░░██║░░░███████╗██║░░██║  ███████╗  ░░╚██╔╝░╚██╔╝░██║██║░╚███║██████╔╝
                    ╚═╝░░░░░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝  ╚══════╝  ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░""")
            return True

        return False

    def promotion_types(self, position):
        print("""
                1. Rook
                2. Knight
                3. Bishop
                4. Queen""")
        choice = input("Choose upgrade: ")
        while choice not in ("1", "2", "3", "4"):
            choice = input("Choose upgrade: ")
        
        if choice == "1":
            return Rook(position, self.name, 'RX', self.piece_sym[2])
        if choice == "2":
            return Knight(position, self.name, 'KnX', self.piece_sym[1])
        if choice == "3":
            return Bishop(position, self.name, 'BX', self.piece_sym[3])
        if choice == "4":
            return Queen(position, self.name, 'QX', self.piece_sym[4])
    def check_pawn_promotion(self, piece):
        row, _ = piece.position
        if self.name == "1":
            if row == 7: 
                setattr(self, piece.name, self.promotion_types(piece.position))
        else:
            if row == 0:
                setattr(self, piece.name, self.promotion_types(piece.position))

        return self.get_piece(piece.name)
        
        #Is pawn on the other side of board on its oppposite row
        #Change object to either
        # - Rook
        # - Knight
        # - Bishop
        # - Queen

    def checkmated(self, king_valid_moves, enemy):
        #King is in peril danger and has no way out, thus he will be destoryed the next turn
        
        
        for position in king_valid_moves:                  
            enemy.checkmate = True

            if self.possibile_attacks[position] == "0":
                enemy.checkmate = False
                break
        


    def draw(self):
        #1 stalemate - 
        #2 insufficient material 
        #3 offer draw
        #4 thee fold repitition 
        pass



class Board:
    
    def __init__(self, p1, p2):
        self.board = []
        self.p1 = p1
        self.p2 = p2
    def __str__(self):
        clear = lambda: os.system('clear')
        clear()
        
        for row in self.board:
            print()
            for item in row:
                if item == 0:
                    print(f"  {item}  ", end = '')
                else:
                    print(f" {item} ", end = '')
        return ""

    def create(self):

        self.board = np.array([[self.p1.R1,   self.p1.KN1,   self.p1.B1,   self.p1.Q,   self.p1.K,   self.p1.B2,   self.p1.KN2,   self.p1.R2],
                              [self.p1.P1, self.p1.P2, self.p1.P3, self.p1.P4, self.p1.P5, self.p1.P6, self.p1.P7, self.p1.P8],
                              [' _ ',  ' _ ',  ' _ ',  ' _ ',  ' _ ',  ' _ ',   ' _ ',   ' _ '],
                              [' _ ',  ' _ ',  ' _ ',  ' _ ',  ' _ ',  ' _ ',   ' _ ',   ' _ '],

                              [' _ ',  ' _ ',  ' _ ',  ' _ ',  ' _ ',  ' _ ',   ' _ ',   ' _ '],
                              [' _ ',  ' _ ',  ' _ ',  ' _ ',  ' _ ',  ' _ ',   ' _ ',   ' _ '],
                              [self.p2.P1, self.p2.P2, self.p2.P3, self.p2.P4, self.p2.P5, self.p2.P6, self.p2.P7, self.p2.P8],
                              [self.p2.R1,   self.p2.KN1,   self.p2.B1,   self.p2.Q,   self.p2.K,   self.p2.B2,   self.p2.KN2,   self.p2.R2]])
        

                              #
    def get_pos(self, position):
        x, y = position
        if self.check_bounds(position):
            return self.board[x][y]
        return False
    def set_pos(self, piece, new_pos, player, old_pos):

        taken_from = []

        a, b = old_pos
        self.board[a][b] = " _ "
        
        # if the new position is an enemy piece
        # return the enemy name, Else False
        new_item = self.get_pos(new_pos)
        
    
        i,j = new_pos
        if isinstance(new_item, Piece) and new_item.player != player:
            taken_from = ["2", new_pos]  if player == "1" else ["1", new_pos]

        #Castling
        elif isinstance(new_item, Rook) and isinstance(piece, King) and new_item.player == player:
            if new_pos > old_pos:
                self.board[a][b+2] = piece
                self.board[i][j-2] = new_item # rook
                piece.position = (a, b+2)
                new_item.position = (i, j-2)
            else:
                self.board[a][b-2] = piece
                self.board[i][j+3] = new_item 
                piece.position = (a, b-2)
                new_item.position = (i, j+3)
            
            self.board[i][j] = " _ "
            return None

        #en_passant
        elif isinstance(piece, Pawn) and piece.en_passant == True:
            taken_from = ["2", (i-1, j)]  if player == "1" else ["1", (i+1, j)]
            a, b = taken_from[1]
            self.board[a][b] = " _ "
            piece.en_passant = False


        x, y = new_pos
        self.board[x][y] = piece

        return taken_from

    def update_valid(self, valid_pos, remove): 
        if remove:
            for choice, (x, y) in enumerate(valid_pos, start=1):
                item = self.board[x][y]

                if isinstance(item, Piece):
                    item.green = False
                elif item[10:][:len(str(choice))] == str(choice):
                        self.board[x][y] = " _ "

        else:
            for choice, (x, y) in enumerate(valid_pos, start=1):
                item = self.board[x][y] 
                
                if item == ' _ ':
                    self.board[x][y] =  colored(f' {choice} ', 'green', attrs=['blink'])
                else:
                    item.green = True
                 
    def check_valid(self, valid_pos, piece, player_name):
        valid = []

        for key, value in valid_pos.items(): 
            for idx, position in enumerate(value):

                item = self.get_pos(position)
                if item:

                    if item == ' _ ' and key not in ('pawn_attack', 'en-passant', 'KS_castling', 'QS_castling') :
                        valid.append(position)

                    elif key[-8:] == "castling":

                            rook = self.get_pos(valid_pos[key][-1])
                            if isinstance(rook, Rook):
                                if rook.movements != 0:
                                    break
                            if item == ' _ ':
                                valid.append(position)
                            else:
                                break

                    elif isinstance(item, Piece) and  item.player != player_name:
                        
                        if isinstance(piece, Pawn):
                            if key in ("en-passant", "pawn_attack"):
                                valid.append(valid_pos['pawn_attack'][idx])
                                if key == "en-passant":
                                    piece.en_passant = True
                            else:
                                break
                        
                        elif key in ("L, square, pawn_attack"):
                            valid.append(position)
                        
                        else:
                            valid.append(position)
                            break
                                         
                    elif key in ("square", "L"):
                        pass

                    else:
                        break

        if isinstance(piece, Queen):
            return list(set(valid))
    
        return valid    
    
    def check_bounds(self, position):

        for i in position:
            if i > 7 or i < 0:
                return False
        return True



class Piece():
    def __init__(self, position, player, piece_name, piece_sym, alive=None):
        self.position = position
        self.player = player
        self.name = piece_name
        self.sym = piece_sym
        self.alive = True
        self.green = False
        self.movements = 0
    def __str__(self):
        item = self.player + '_' + self.sym
        if self.green:
            return colored(item, 'green', attrs=['blink'])
        return item

    def get_pos(self):
        return self.position

    def vertical_horizontal(self):
        coord = np.moveaxis(np.mgrid[:8,:8], 0, -1)
        i, j = self.position
   
        row = list(map(tuple, coord[i , :]))
        column = list(map(tuple, coord[: , j]))

        return  {"left": row[:j][::-1],    
                    "right": row[j+1:],
                    "up": column[:i][::-1], 
                    "down": column[i+1:]}
    
    def diagonal_sub(self, name, iter, i, j):
        if name == "TL":
            return (i - (1*iter), j - (1*iter))
        elif name == "TR":
            return (i - (1*iter), j + (1*iter))
        elif name == "BL":
            return (i + (1*iter), j - (1*iter))
        else:
            return (i + (1*iter), j + (1*iter))
    def diagonal(self):
        dict_ = {
            "TL" : [],
            "TR" : [],
            "BL" : [],
            "BR" : [],
        }

        for key, _ in dict_.items():
            iter = 1
            temp = []
            x, y = i, j = self.position 
 
            diag_val = (self.diagonal_sub(key, iter, i, j))

            while min(diag_val) >= 0 and max(diag_val) <= 7:
                temp.append(diag_val)
                diag_val = self.diagonal_sub(key, iter, i, j)
                x, y = temp[iter-1]
                iter += 1
            dict_[key] = temp[1:]
        return  dict_
             
    def square(self):  
        i, j = self.position
        return {"square" :  [(i-1, j-1),(i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]}
            
class Pawn(Piece):
    def __init__(self, position, player, piece_name, piece_sym, alive=None):
        self.position = position
        self.player = player
        self.name = piece_name
        self.sym = piece_sym
        self.alive = True
        self.green = False
        self.movements = 0
        self.en_passant = False

    #returns valid moves
    def valid_moves(self):
        i, j = self.position
        p = -1 if self.player == "2" else 1

        return  { "pawn_horizontal" : [(i + (p*1), j), (i + (p*2), j)] if self.movements == 0 else [(i + (p*1), j)],
                  "pawn_attack" : [(i-1, j-1), (i-1, j+1)] if self.player == "2" else [(i+1, j-1),(i+1, j+1)],
                  "en-passant" : [(i, j-1), (i, j+1)]}

class Knight(Piece):
   
    def valid_moves(self):
        i,j = self.position
        return { "L" : [(i-2, j-1), (i-2, j+1), (i-1, j-2), (i-1, j+2), (i+2, j-1), (i+2, j+1), (i+1, j-2), (i+1, j+2)]}

class Rook(Piece):

    def valid_moves(self):
        return self.vertical_horizontal()
        
class Bishop(Piece):

    def valid_moves(self):
        return self.diagonal()

class Queen(Piece):
     
    def valid_moves(self):
       return self.vertical_horizontal() | self.diagonal() |  self.square()

class King(Piece):
    
    def valid_moves(self):
        return self.square() | self.castling()
    
    def castling(self):
        if self.movements == 0:
            i,j = self.position
            return {"KS_castling" : [(i,j+2), (i,j+3)],
                     "QS_castling" : [(i,j-2), (i,j-3), (i, j-4)]}            
        return {}
        
        #method for king piece
        #
        #Rules: 
        #1 king and rook to be castled must never have moved in game
        #2 If the path is clear from king to rook then can castle  
        #3 King cannot escape check from castling
        #4 can never castle king into a check
        #5 May never cross a square that is in attack
        



def get_valid_piece(player):

    piece_name = input("\nPlease enter piece from following: ").upper()

    while not player.valid_piece(piece_name) or (player.checked == True and piece_name != "K"):
        piece_name = input("\nPlease enter a valid piece: ").upper()
    return player.get_piece(piece_name) #obj ref

def print_player(player):
    if player.name == "1":
        print("""
███████████████████████████████████████████
█▄─▄▄─█▄─▄████▀▄─██▄─█─▄█▄─▄▄─█▄─▄▄▀███▀░██
██─▄▄▄██─██▀██─▀─███▄─▄███─▄█▀██─▄─▄████░██
▀▄▄▄▀▀▀▄▄▄▄▄▀▄▄▀▄▄▀▀▄▄▄▀▀▄▄▄▄▄▀▄▄▀▄▄▀▀▀▄▄▄▀""")
    else:
        print("""
████████████████████████████████████████████
█▄─▄▄─█▄─▄████▀▄─██▄─█─▄█▄─▄▄─█▄─▄▄▀███▀▄▄▀█
██─▄▄▄██─██▀██─▀─███▄─▄███─▄█▀██─▄─▄████▀▄██
▀▄▄▄▀▀▀▄▄▄▄▄▀▄▄▀▄▄▀▀▄▄▄▀▀▄▄▄▄▄▀▄▄▀▄▄▀▀▀▄▄▄▄▀""")       
def print_main_menu():
    clear = lambda: os.system('clear')
    clear()

    print("""
            ░█████╗░██╗░░██╗███████╗░██████╗░██████╗
            ██╔══██╗██║░░██║██╔════╝██╔════╝██╔════╝
            ██║░░╚═╝███████║█████╗░░╚█████╗░╚█████╗░
            ██║░░██╗██╔══██║██╔══╝░░░╚═══██╗░╚═══██╗
            ╚█████╔╝██║░░██║███████╗██████╔╝██████╔╝
            ░╚════╝░╚═╝░░╚═╝╚══════╝╚═════╝░╚═════╝░

            █████╗█████╗█████╗█████╗█████╗█████╗█████╗
            ╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝""")


def clear():
    clear = lambda: os.system('clear')
    time.sleep(3)
    clear()

if __name__ == "__main__":
    #player one create
    p1_sym = ['♟︎', '♘', '♖', '♗', '♕', '♔']
    p1_pawn_pos = [(1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7)]
    p1_knight_pos = [(0,1), (0,6)]
    p1_rook_pos = [(0,0), (0,7)]
    p1_bishop = [(0,2), (0,5)]
    p1_queen = (0,3)
    p1_king = (0,4)
    p1 = Player(p1_pawn_pos, p1_knight_pos, p1_rook_pos, p1_bishop, p1_queen, p1_king,  "1", p1_sym)

    #player two create
    p2_sym = ['♙', '♞', '♜', '♝', '♛', '♚']
    p2_pawn_pos = [(6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7)]
    p2_knight_pos = [(7,1), (7,6)]
    p2_rook_pos = [(7,0), (7,7)]
    p2_bishop = [(7,2), (7,5)]
    p2_queen = (7,3)
    p2_king = (7,4)
    p2 = Player(p2_pawn_pos,  p2_knight_pos, p2_rook_pos, p2_bishop, p2_queen, p2_king,  "2", p2_sym)

    #create the board with both players and their pieces
    board = Board(p1, p2)
    board.create()

    win = False

    print_main_menu()
    inp = input("\n\t\t     Press a key to continue")

    while not win: #Whilst no one has won
        for idx, player in enumerate((p1, p2)):

            enemy = p2 if player == p1 else p1
            
            print(board)           

            #Player's turn and show pieces
            print_player(player)
            player.print_pieces()
            player.print_taken()
            
            while True: #Whilst a valid piece is picked
                piece = get_valid_piece(player)
                
                #Gets valid movements and shows new board
                valid_moves = player.get_valid_moves(piece) #Gets the valid moves for the given piece
                valid_moves = board.check_valid(valid_moves, piece, player.name) #Are there any conflics on the board for these valid moves
                
                if piece.name == "K":
                   valid_moves = [i for i in valid_moves if enemy.possibile_attacks[i] != "1"]

    
                if valid_moves: 
                    break #if there are possible moves
                print(f"No valid moves for piece : {piece.name}")
                clear()

            #Update board with the valid positions and print
            board.update_valid(valid_moves, False) #Remove=False
            print(board)

            #shows valids movements and gets new position
            newline = "\n"
            print("\n  ", player)
            print(f"Choice  |  Position  |  Value")
            print(f'{newline.join(f"   {idx}    |  {positions}    |   {board.get_pos(positions)}" for idx, positions in enumerate(valid_moves, start=1))}')
            while True:
                try:
                    new_pos = valid_moves[int(input("\nChoice:  ")) - 1]
                    break
                except:
                    pass

            #create temp as old position and update player's piece with new position
            old_pos = piece.position
            player.update_piece(piece, new_pos)

            board.update_valid(valid_moves, True) #Remove the green valid movements
 
            # is the piece a pawn, can we promote the pawn?
            if isinstance(piece, Pawn):
                piece = player.check_pawn_promotion(piece)

            #General update of board with new position of piece AND
            #if a piece is taken from enemy, will return player name and pos of taken
            taken_from = board.set_pos(piece, new_pos, player.name, old_pos)
            
            if taken_from:
                piece_taken = enemy.remove_piece(taken_from[1])
                player.update_taken(piece_taken)
           
            """if taken_from:
                if taken_from[0] == "1":
                    #piece name taken and updated scoreboard (taken pieces) for that player
                    piece_taken = p1.remove_piece(taken_from[1])
                    p2.update_taken(piece_taken)
                else:
                    piece_taken = p2.remove_piece(taken_from[1])
                    p1.update_taken(piece_taken)"""
   

            #All the possible attacks that can be made for that player
            player.possibile_attacks = np.zeros((8,8), str)
            for _, piece in np.ndenumerate(player.pieces):
            
                if isinstance(piece, Piece):
                
                    valid_moves = player.get_valid_moves(piece) #Get valid 
                    valid_moves = board.check_valid(valid_moves, piece, player.name)

                    player.possibile_attacks[piece.position] = piece.sym

                    for (i,j) in valid_moves:
                        player.possibile_attacks[i,j] = "1"



            #Is the enemy king in the line of sight for all my possible attacks?
            
            enemy_king = enemy.get_piece("K")

            if player.possibile_attacks[enemy_king.position] == "1": 
                enemy.checked = True
                valid_moves = board.check_valid(enemy_king.valid_moves(), enemy_king, enemy.name)
                player.checkmated(valid_moves, enemy)

            if enemy.checkmate:
                print("Checkmate")
                break
            
            elif enemy.checked:
                print("check")