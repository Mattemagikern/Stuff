import sys
from copy import copy, deepcopy
import time

#{{{  Setup for the Othello board
playground = [[0 for i in range(8)] for j in range(8)]
playground[4][4] = 1
playground[4][3] = 2
playground[3][4] = 2
playground[3][3] = 1
#}}}
human = 0
computer = 0

#white == 1 black == 2
#{{{
def main():
    print "Welcome, choose a player 1 or 2!" 
    print "player 2 starts"
    try:
        global human
        global computer
        human = int(raw_input("Choose a player: "))
        computer = human % 2 +1
        if human != 1 and human != 2:
            raise ValueError
    except ValueError:
        print("Invalid number")
        sys.exit(1)
    player = 2 

    while(True):
        moves = find_legal_moves(playground, player)
        if len(moves) == 0:
            moves2 = find_legal_moves(playground, player % 2 + 1)
            if len(moves2) == 0:
                print " " 
                check_result(moves, final=True)
                sys.exit(0)
            elif len(moves2) != 0:
                print "you have no possible moves to make"
                print "your turn has been forfited to the computer"
                player = (player % 2) + 1 
                continue

        if player == human:
            print_othello()
            print "------------------"
            while(True):
                print "Possible moves: ",
                for i in range(len(moves)):
                    print str(i) + ":" + str(moves[i][0]) + ", ",
                print " "
                try:
                    move = int(raw_input("Choose a move: "))
                    if 0 > move or move > (len(moves)-1):
                        print "in error"
                        raise ValueError
                    make_move(player, moves[move], playground)
                    break
                except ValueError:
                    print("Invalid move")
        else:
            if len(moves) != 0:
                move = alpha_beta(player, playground, -1000, 1000, 5)[1]
                make_move(player, move, playground)
        player = (player % 2) + 1

#}}}
#{{{ stuff
""" WIP - not to be implemented.
simulates a game depending on the moves aviable and returns the move that
provided the most wins
"""
def simulate_game(moves, player):
    global playground
    what_move = {}

    for m in moves: what_move[m] = 0

    for move in moves:
        board = deepcopy(playground)
        white = 0;
        black = 0;
        make_move(move,board=board)
        #runs a random game. 
        for i in range(10):
            for i in range(64):
                player = i%2+1
                #print "---------------Player " + str(i%2+1) + "-----------------"
                moves = find_legal_moves(board, player)
                if len(moves) == 0:
                    moves2 = find_legal_moves(board, player%2+1)
                    if len(moves2) == 0:
                        print " " 
                        res = check_result(moves)
                        if(res == player):
                            what_move[move] +=1;
                        break;
                else:
                    move = r.choice(moves) # create better choice algorithm.
                    make_move(i%2+1,move)

    return max(what_move, key=what_move.get)
#}}}
#{{{
def alpha_beta(player, board, alpha, beta, depth):
    moves = find_legal_moves(board, player) 
    if depth == 0 or len(moves) == 0:#omg we found a leaf
        if points(board,human) == 0:
            return [float(points(board, computer)), "temp"]
        return [float(points(board, computer)) / points(board, human),"temp"]

    if player == human:#Minimum player
        v = [100, "null"]
        for m in moves:
            temp_board = deepcopy(board)
            make_move(player, m, temp_board)
            res = alpha_beta(player % 2 + 1, temp_board, alpha, beta,
                    depth-1)
            if v[0] > res[0]:
                v = res
                v[1] = m
                beta = min(beta, v[0])
            if beta <= alpha:
                break 
    else:#Maximum player
        v = [-100, "null"]
        for m in moves:
            temp_board = deepcopy(board) 
            make_move(player, m, temp_board)
            res = alpha_beta(player % 2 + 1, temp_board, alpha, beta,
                    depth-1)
            if v[0] < res[0]:
                v = res
                v[1] = m
                alpha = max(alpha, v[0])
            if beta <= alpha:
                break
    return v
#}}}
#{{{ Finding legal moves

#returns a list of legual moves positioned as ((x,y),[dirs])
def find_legal_moves(board, player):
    legal_moves = []
    #check find legal moves
    for i in range(8):
        for j in range(8):
            legal_dir = out_flank(board, i, j, player)
            if len(legal_dir) != 0:
                legal_moves.append(((i, j),legal_dir))
    return legal_moves

def out_flank(board, x, y, player):
    dirs = [(-1,-1),(-1,0),(0,-1),(0,1),(1,0),(1,1)]
    legal = []
    if board[x][y] == 0:
        for dir in dirs:
            if(8 > x + dir[0] > -1) and (8 > y + dir[1] > -1):
                if (board[x + dir[0]][y + dir[1]] != player and board[x +
                    dir[0]][y + dir[1]] != 0):
                    for i in range(1,8):
                        if ( 8 > x + i * dir[0] > -1) and (8 > y + i* dir[1] > -1):
                            if board[x + i * dir[0]][y + i * dir[1]] == player:
                                legal.append(dir)
                                break
    return legal

#if there is no legal moves, exit and tell the results
def check_result(legal_moves, final = False):
    if len(legal_moves) == 0:
        black = points(playground, 2)
        white = points(playground, 1)
        if(final):
            if(black == white):
                print ("its a draw! White: " + str(white) + " " + "Black: " +
                        str(black))
            elif black < white:
                print ("1 Won! Congratulation! " + str(white) + " vs " +
                        str(black))
            else:
                print ("2 Won! Congratulation! " + str(black) + " vs " +
                        str(white))
                print_othello() 
        return 1 if white > black else 2
    return 0
#}}}

#{{{ utiity
def print_othello():
    print "   0  1  2  3  4  5  6  7 "
    for i in range(8):
        print str(i) + " " + str(playground[i])

def print_board(board):
    print "   0  1  2  3  4  5  6  7 "
    for i in range(8):
        print str(i) + " " + str(board[i])

def reset():
    global playground
    playground = [[0 for i in range(8)] for j in range(8)]
    playground[4][4] = 1
    playground[4][3] = 2
    playground[3][4] = 2
    playground[3][3] = 1




##Flips the tiles given a move((x,y), (dx,dy)).
def make_move(player, move, board): 
    x = move[0][0]
    y = move[0][1]
    dx = move[1][0][0]
    dy = move[1][0][1]
    for i in range(8):
        if(board[x + i * dx][y + i * dy] != player):
            board[x + i * dx][y + i * dy] = player
        else:
            break;

def points(board, player):
    result = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                result += 1
    return result
# }}}


if __name__ == '__main__':
    main()
