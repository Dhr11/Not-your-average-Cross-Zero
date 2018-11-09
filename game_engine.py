#!/usr/bin/env python3
import copy
import sys
import time

max_player = ''
min_player = ''
n = ''
counter_max = 0
blockcol = []

def printable_board(board):
    print("\n".join([ " ".join([ str(board[row][col]) for col in range(0,len(board)-3)]) for row in range(0,len(board))]))

def boardstring(board):
    print(''.join(a for i in board for a in i))

def da_move_calculator(board, player):
    N = len(board)
    expanded = board+board
    width = N-3 
    #c = [[]]
    c = []
    for i in range(0, N):
        board2 = []
        for j in range(0, N-3):
            board2.append('.')
        c.append(board2)
    #c = [['.'] for i in range(N) for j in range(N-3)]
    
    player2 = 'x' if player == 'o' else 'o'
    first_player2 = ['.' for x in range(0,width)]
    last_player2 = ['.' for x in range(0,width)]
    
    first_empty = ['.' for x in range(0,width)]
    count_other = 0     
    
    for y in range(0,width):
        for x in range(2*N-1,N-1,-1):
            #print(x)
            
            if first_empty[y] == '.' and expanded[x][y] == '.' :   first_empty[y]=x-N
            if last_player2[y] == '.' and expanded[x][y] == player2 : last_player2[y] = x-N              
            if expanded[x][y] == player2 : 
                first_player2[y] = x-N                
                count_other +=1               
            if expanded[x][y] == '.': 
                c[x-N][y] ='.'
                continue
            
            past = x+1
            if past<2*N and c[past-N][y]!='.' and c[past-N][y]!= player2 and c[past-N][y]>1:
                c[x-N][y] = c[past-N][y]-1
                continue
            
            if expanded[x][y] == player: 
                c[x-N][y] =0
                continue
            count = 0
            for i in range(x-1,0,-1):
                
                if expanded[i][y] == player:
                    c[x-N][y] = x-i-count 
                    break
                if expanded[i][y] == '.':   count +=1
            #print(expanded[x][y],player2)    
            
            # when after all this we still dont have value it means there is no 
            # element of player, but if other is there, then handle
            if c[x-N][y]=='.' and expanded[x][y] == player2:
                #print("sxsx")
                c[x-N][y]=player2
    #print(first_player2)
    #print(last_player2)
    row_moves = []        
    for r in range(N-1,-1,-1):
        row_sum= 0
        for col in range(0,width):
            if c[r][col]=='.':
                row_sum += first_empty[col]-r+1
            elif c[r][col]==player2:
                row_sum += r-first_empty[col]+1 if first_empty[col] !='.' else 100000
            else:
                row_sum +=c[r][col]
        row_moves.append(row_sum)
    maindiagonal = [0,0]    
    for r in range(N-4,-1,-1):
        col =[N-r-4,r]
        for i in [0,1]:
            if c[r][col[i]]=='.':   maindiagonal[i] += abs(first_empty[col[i]]-r)+1
            elif c[r][col[i]] == player2:    
                maindiagonal[i] += r-first_empty[col[i]]+1 if first_empty[col[i]]!='.' else 100000
            else:   
                #print(c)
                maindiagonal[i] += c[r][col[i]]
    colmoves=[]
    for y in range(0,width):
        if(last_player2[y]=='.') :
            #print("sd\n",board)
            if first_empty[y] != '.': colmoves.append(first_empty[y] + 1)
            else : colmoves.append(0)
            continue
        if last_player2[y]-first_player2[y] >2:
            colmoves.append(100000) 
            continue
        if last_player2[y]-first_player2[y]<3 :
            #print(first_empty[y])
            #print(c)
            val = 0
            if first_empty[y] != '.' : val += first_empty[y] + 1
            if first_player2[y]< N-3 : val+= abs(first_player2[y]-(N-3))                 
            colmoves.append(val) 
            continue
    p_block = []
    for y in range(0,width):
        if colmoves[y]>10000:
            p_block.append(y)
    
    #print(colmoves)
    #print(maindiagonal)
    #print(row_moves)
    #printable_board(c)
    return (min(min(colmoves),min(maindiagonal), min(row_moves[3:])), count_other)
    
    #print(c)           
def da_heuristic2(move1,move2,count1,count2):
    val=move2-move1-initval
    #return 10*val
    return 6*move2-4*move1

def da_heuristic3(move1,move2,count1,count2):
    fullval = n*(n+3)/2
    rem1 = fullval- count1
    rem2 = fullval- count2
    #if count1==0 or count2==0 or count1==count2:
    #    return (move2)-(move1)
    if rem2!=0: 
        ratio = rem1/rem2
        if ratio>1 and rem2!=0: return (8*move2)-(move1*4)
    return (6*move2)-(move1*4)

def da_heuristic4(move1,move2,count1,count2):
    fullval = n*(n+3)/2
    rem1 = fullval- count1
    rem2 = fullval- count2
    if count1==0 or count2==0 or count1==count2:
        return (move2)-(move1)
    if rem2!=0: 
        ratio = rem1/rem2
        if ratio>2 and rem2!=0: return (move1*1)
    return (1*move2)-(move1*1)    


def drop(col, current_player, board1):
    global counter_max
    counter_max+=1
    current_board = copy.deepcopy(board1)
    select = -1
    for i in range(len(current_board)):
        if i == 0 and current_board[i][col] != '.':
            break  # cannot add a pebble here
        if current_board[i][col] == '.':
            select = i
    if select != -1:
        current_board[select][col] = current_player
    return current_board


def rotate(col, board1):
    board = copy.deepcopy(board1)
    no_of_row = len(board1)
    temp = board[no_of_row - 1][col]
    for i in range(no_of_row - 1, 0, -1):
        board[i][col] = board[i - 1][col]

    board[0][col] = '.'
    board = drop(col, temp, board)
    return board


def successors(board, current_player):
    global n
    global counter_max
    total = (n + (n+3))/2
    list1 = []
    for i in range(n):
        #if i not in blockcol:   list1.append(rotate(i, board))
        if board[0][i]=='.' :#and counter_max < total:
            list1.append(drop(i, current_player, board))
        if board[n+2][i]!='.':   list1.append(rotate(i, board))
        
        #list1.append(rotate(i, board))
    return list1


def terminal(s, depth):
    if depth == 0:
        return 1
    return 0


def min_value(s, alpha, beta, depth):
    global min_player
    depth -= 1
    mv1,count2 = da_move_calculator(s,player1) 
    player2 = 'x' if player1 == 'o' else 'o'
    mv2,count1 = da_move_calculator(s,player2)
    if(mv1==0): return 10000
    if(mv2==0): return -10000  
    if terminal(s, depth):
        #print("terminal depth min fn")
        return da_heuristic2(mv1,mv2,count1,count2)
    for s2 in successors(s, min_player):
        val = max_value(s2, alpha, beta, depth)
        #print("beta: ",beta," max val: ", val)
        beta = min(beta, val)
        if alpha >= beta:
            return beta
    return beta


def max_value(s, alpha, beta, depth):
    global max_player
    depth -= 1
    mv1,count2 = da_move_calculator(s,player1) 
    player2 = 'x' if player1 == 'o' else 'o'
    mv2,count1 = da_move_calculator(s,player2)
    if(mv1==0): return 10000
    if(mv2==0): return -10000
    if terminal(s, depth):
        #print("terminal depth max fn depth")
        #printable_board(s)
        #print(da_heuristic2(s))
        
    #    return da_heuristic2(s)
        return da_heuristic2(mv1,mv2,count1,count2)
    for s2 in successors(s, max_player):
        val = min_value(s2, alpha, beta, depth)
        #print("alpha: ",alpha," min val: ", val)
        alpha = max(alpha, val)
        
        if alpha >= beta:
            return alpha
    return alpha


def successors2(main_succ, board):
    global n
    global max_player
    for i in range(n):
        temp = rotate(i, board)
        if temp == main_succ:
            decision = i+1
            return -decision
        temp = drop(i, max_player, board)
        if temp == main_succ:
            decision = i+1
            return decision


def alpha_beta_decision(initial_board, depth):
    global max_player
    alpha = -1000000
    for s in successors(initial_board, max_player):
            a = min_value(s, alpha, 1000000, depth)
            if alpha < a:
                alpha = a
                main_suc = s
    decision = successors2(main_suc, initial_board)
    return main_suc, decision


def main():
    global n
    global max_player
    global min_player
    global player1
    global initval
    start = time.time()
    n = int(sys.argv[1])
    max_player = sys.argv[2]
    player1 = sys.argv[2]
    if max_player == 'x':
        min_player = 'o'
    else:
        min_player = 'x'
    state_of_board = sys.argv[3]
    time_limit = int(sys.argv[4])
    initval = 0    
    initial_board = []
    for i in range(0, len(state_of_board), n):
        board = []
        for j in range(0, n):
            board.append(state_of_board[i + j])
        initial_board.append(board)
        
    #printable_board(initial_board)
    a,b = da_move_calculator(initial_board, player1)
    c,d = da_move_calculator(initial_board, min_player)

    initval = c-a 
    #da_heuristic2(initial_board)
    #print(da_move_calculator(initial_board,max_player))
    #print(da_move_calculator(initial_board,min_player))
    depth = 1
    
    while True:
        mainsuc, decision = alpha_beta_decision(initial_board, depth)
        
        str = ''
    
        for i in mainsuc:
            for j in i:
                str += j
        print(decision, " ", str)
        depth += 2
        if time.time() > start + time_limit:
            break
    """
    if decision < 0:
        print("I'd recommend rotating column ", abs(decision))
    else:
        print("I'd recommend dropping a pebble in column ", decision)
    """
    
    
    return


if __name__ == '__main__':
    main()