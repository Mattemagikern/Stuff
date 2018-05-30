# -*- coding: utf-8 -*-
#from termcolor import colored #Needed for print colors
import random as r
import cPickle
import time as t
import math
#from tqdm import tqdm
human = 0
computer = 0
board = 0
peaces = {1: {'P': "♙", 'R': "♖", 'N': "♘", 'B': "♗", 'Q': "♔",'K': "♕" },
          2: {'P': "♟", 'R': "♜", 'N': "♞", 'B': "♝", 'Q': "♚", 'K': "♛" }
         }
killed = [[],[]]
iterations = []

#{{{ init
def init():
    global board, killed
    board = [[("x",0) for i in range(8)] for j in range(8)]
    board[7] = [(i,1) for i in ["R","N","B", "K","Q","B","N","R"]]
    board[6] = [("P",1)] * 8
    board[1] = [("P",2)] * 8
    board[0] = [(i,2) for i in ["R","N","B", "K","Q","B","N","R"]]
    killed = [[],[]]
#}}}

#{{{ find_moves
def find_moves(player, board = None):
    if board == None: board = globals()["board"]
    moves = []
    for i in range(8):
        for j in range(8):
            sq = board[i][j]
            dirs = []
            if sq[1] == player:
                dist = 8
                #Rook
                if sq[0] == "R":
                    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
                #Knight, speciall case
                elif sq[0] == "N": 
                    dist = 2
                    dirs = [(1,2), (2,1), (-1,2), (-2, 1),
                            (-2,-1), (-1, -2), (1, -2), (2, -1)]
                #Bishop
                elif sq[0] == "B": 
                    dirs = [(1,1),(-1,-1),(-1,1),(1,-1)]
                #King!
                elif sq[0] == "K": 
                    dirs = [(1,0),(1,1),(-1,-1),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]
                    dist = 2
                #Queen
                elif sq[0] == "Q": 
                    dirs = [(1,0),(1,1),(-1,-1),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]
                #Pawn
                elif sq[0] == "P":
                    dist = 2

                    if i == 7 or i == 0:
                        #find what pieces are aviable
                        #move: ((piece, -1 , -1), (i,j))
                        for piece in [ a for a in killed[player%2] if a != "P"]:
                            moves.append((((piece, sq[1]),(-1,-1)),(i,j)))
                            continue

                    if player == 1:
                        if i == 6 and board[i-2][j] == ("x", 0):
                            dist = 3
                        if i-1 > -1:
                            if board[i-1][j][0] == "x": 
                                dirs = [(-1,0)]
                            if j+1 < 8:
                                if board[i-1][j+1][1] == player % 2 + 1:
                                    dirs.append((-1,1))
                            if j-1 > -1:
                                if board[i-1][j-1][1] == player % 2 + 1:
                                    dirs.append((-1,-1))
                    else:
                        if i == 1 and board[i+2][j] == ("x", 0):
                            dist = 3
                        if i+1 < 8:
                            if board[i+1][j][0] == "x":
                                dirs = [(1,0)]
                            if j+1 < 8:
                                if board[i+1][j+1][1] == player % 2 + 1:
                                    dirs.append((1,1))
                            if j-1 > -1:
                                if board[i+1][j-1][1] == player % 2 + 1:
                                    dirs.append((1,-1))
                #actually adding the possible moves!
                for dir in dirs:
                    for r in range(1,dist):
                        x = i + dir[0] * r
                        y = j + dir[1] * r
                        if (x < 0 or y < 0 or x > 7 or y > 7 or
                                board[x][y][1] == player):
                            break
                        elif (board[x][y][1] == player % 2 + 1):
                            moves.append(((sq,(i,j)),(x,y)))
                            break

                        moves.append(((sq,(i,j)),(x,y)))
    return moves

#}}}

#{{{ make_moves
#move: ((piece, (old_x, old_y)), (newx,newy))
def make_move(move, board = None, killed = None):
    if board == None: board = globals()["board"]
    if killed == None: killed = globals()["killed"]
    #normal
    old = move[0]
    new = move[1]
    #killing
    if board[new[0]][new[1]][0] != "x":
        piece = board[new[0]][new[1]]
        killed[piece[1]%2].append(piece[0])
    if old[1] != (-1,-1):
        board[old[1][0]][old[1][1]] = ("x", 0)
    board[new[0]][new[1]] = old[0]

#}}}

#{{{ find_piece
def find_piece(piece, board = None):
    if board == None: board = globals()["board"]
    for i in range(8):
        for j in range(8):
            if board[i][j] == piece:
                return i,j
    return None
#}}}

#{{{ check
def check(moves, opponent, board = None):
    if board == None: board = globals()["board"]
    x,y = find_piece(("K",opponent), board = board)
    if (x,y) in [i[1] for i in moves]:
        return True
    return False        
#}}}

#{{{ show
def show(board = None):
    if board == None: board = globals()["board"]
    print "   ",
    for i in range(8):
        print i,
    print "x"
    print "_"
    for y in range(8):
        print y, " ",
        for x in range(8):
            if board[x][y][1] != 0:
                print peaces[board[x][y][1]][board[x][y][0]],
            else:
                #print colored(board[x][y][0],"white"),
                print board[x][y][0],
        print
    print "y"
#}}}

def deepcopy(matrix):
    return cPickle.loads(cPickle.dumps(matrix,-1))

#{{{ alpha-beta and heuristics
def heuristics(killed_list, player,board = None):
    if board == None: board = globals()["board"]
    values = {"K": 1000, "Q": 700, "R": 500, "B": 300, "N": 300, "P": 50}
    points = 0
    #This should be reversed?
    for i in killed_list[(player + 1) % 2]:
        points += values[i]
    for i in killed_list[(player) % 2]:
        points -= values[i]
    return [points, "null"];

def alpha_beta(player, alpha, beta, depth, time, board, killed):
    moves = find_moves(player, board=board)
    #if depth == 0 or "K" in killed[0] + killed[1]:
    if depth == 0 or "K" in killed[0] + killed[1] or time < t.time():
        return heuristics(killed, computer, board = board)
    if player == human:#Minimum player
        v = [float('inf'), "null"]
        for m in moves:
            temp_board = deepcopy(board)
            tem_killed = deepcopy(killed)
            make_move(m, board = temp_board, killed =
                    tem_killed)
            res = alpha_beta(((player) % 2) + 1,  alpha, beta,
                    depth-1, time, temp_board, tem_killed)
            if v[0] > res[0]:
                v = res
                v[1] = m
                beta = min(beta, v[0])
            if beta <= alpha:
                break 
    else:#Maximum player
        v = [-float('inf'), "null"]
        for m in moves:
            temp_board = deepcopy(board)
            tem_killed = deepcopy(killed)
            make_move(m, board = temp_board, killed =
                    tem_killed)
            res = alpha_beta(((player) % 2 )+1,  alpha, beta,
                    depth-1, time, temp_board, tem_killed)
            if v[0] < res[0]:
                v = res
                v[1] = m
                alpha = max(alpha, v[0])
            if beta <= alpha:
                 break
    return v

# }}}

def monte_carlo(player, moves, real_board, real_killed,time):
    points = [0 for i in range(len(moves))]
    ittr = 0
    enemy_king = find_piece(("K",player % 2 + 1), board = real_board)
    king_slaying_moves = [i for i in moves if i[1] == enemy_king]
    if len(king_slaying_moves) > 0:
        return king_slaying_moves[0]
    while time > t.time():
        ittr += 1
        index = r.randint(0, len(moves) - 1)
        killed = deepcopy(real_killed)
        save = deepcopy(real_board)
        make_move(moves[index], board = save, killed = killed) 
        player = player % 2 + 1 
        i = 0 
        while i < 5: 
            if "K" in [j for j in killed[0]+killed[1]]:
                break
            mov = find_moves(player, board = save)
            enemy_king = find_piece(("K",player % 2 + 1), board = save)
            make_move(r.choice(mov), board = save, killed = killed)
            player = player % 2 + 1
            i += 1
    #This should be reversed?
        monte_ =  heuristics(killed, human, board = save)[0]
        points[index] += monte_
    iterations.append(ittr)
    if points == [0]* len(points):
        return r.choice(moves)
    return moves[points.index(max(points))]


def main():
    print "Welcome, choose a player 1 or 2!" 
    print "player 2 starts"
    try:
        global human
        global computer
        human = int(raw_input("Choose a player:"))
        computer = human % 2 + 1
        if human != 1 and human != 2:
            raise ValueError
    except ValueError:
        print("Invalid number")
        sys.exit(1)
    computer_win = 0
    human_win = 0
    player = 2
    init()
    print peaces[human]["K"]
    print 
    while "K" not in [j for j in killed[0] + killed[1]]:
        moves = find_moves(player)
        if player == human:
            move = monte_carlo(player, moves, board, killed)
            make_move(move)
            #moves = find_moves(player)
            #make_move(r.choice(moves))
            """
            show() 
            print "------------------"
            while(True):
                print "Possible moves: ",
                for i in range(len(moves)):
                    print str(i) + ":" + str(moves[i]) + ", ",
                print " "
                try:
                    move = int(raw_input("Choose a move: "))
                    if 0 > move or move > (len(moves)-1):
                        print "in error"
                        raise ValueError
                    make_move(moves[move])
                    break
                except ValueError:
                    print("Invalid move")
            """
        elif player == computer:   
            temp_board = deepcopy(board)
            tem_killed = deepcopy(killed)
            move = alpha_beta(player, -10000, 10000, 5,
                    board = temp_board, killed =
                    tem_killed)[1]
            make_move(move)
            #make_move(r.choice(moves))
        show()
        print "-----------------"
        player = (player % 2) + 1
    if "K" in killed[(computer+1)%2 ]:
        computer_win += 1
        #print "player 2 won!"
    else:
        human_win+=1
        #print "player 1 won!"
    #print "killed: player 2: ", killed[0]
    #print "killed: player 1: ", killed[1]
    print peaces[human]["K"]
    print "computer_win:", computer_win
    print "human_win:", human_win

if __name__ == '__main__':
    alpha_beta_win= 0
    monte_carlo_win = 0
    draw = 0
    human = 2
    computer = 1
    alpha_beta_time = 0
    for z in range(1):
        player = 2
        move_nbr = 0;
        init()
        while "K" not in [j for j in killed[0]+killed[1]] and move_nbr < 55:
            moves = find_moves(player)
            if player == human:
                move = monte_carlo(player, moves, board, killed,
                        t.time() + 2)
                make_move(move)
            elif player == computer:   
                temp_board = deepcopy(board)
                tem_killed = deepcopy(killed)
                time_t = t.time()
                move = alpha_beta(player, -float('inf'), float('inf'),
                        5,t.time() + 2,
                        board = temp_board, killed =
                        tem_killed)
                time_l = t.time()
                alpha_beta_time += time_l - time_t
                make_move(move[1])
            show()
            move_nbr += 1
            player = (player % 2) + 1
        if "K" in killed[human % 2]:
            alpha_beta_win += 1
        elif "K" in killed[computer % 2]:
            monte_carlo_win += 1
        else:
            draw += 1
    alpha_beta_avrage = alpha_beta_time / float(move_nbr)
    print "avrage itterations:", sum(iterations) / float(move_nbr)
    print "alpha_beta_tot_time", alpha_beta_time
    print "alpha_beta:",  alpha_beta_win
    print "Alpha-Beta_time:", alpha_beta_avrage
    print "monte_carlo_win:", monte_carlo_win
    print "draw:",  draw
