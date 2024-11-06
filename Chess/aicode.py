import random
CHECKMATE = 1000
STALEMATE = 0
MAX_DEPTH = 2

def randomMove(gs,validMoves):
    move = random.randint(validMoves)
    return move

def bestMove(gs, validMoves): #this gets the best move from the minimax aglorithm and returns it
    global bestMove
    bestMove = None
    minimax(gs, MAX_DEPTH, gs.whiteToMove, validMoves)
    return bestMove


def minimax(gs, depth, max_player, validMoves):
    global bestMove
    if depth == 0 or gs.game == False:
        return evaluate(gs)

    if max_player == True: 
        maxEval = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.validMoves()
            evaluation = minimax(gs, depth-1, False, nextMoves)
            if evaluation > maxEval:
                maxEval = evaluation
                if depth == MAX_DEPTH:
                    bestMove = move    
            gs.undoMove()
        return maxEval

    else:
        minEval = CHECKMATE   
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.validMoves()
            evaluation = minimax(gs, depth-1, True, nextMoves)
            if evaluation < minEval:
                minEval = evaluation
                if depth == MAX_DEPTH:
                    bestMove = move
            gs.undoMove()
        return minEval
        

def evaluate(gs):
    score = 0
    # Positive scores are good for white but bad for black and vice versa. 
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else: 
            return CHECKMATE
    if gs.stalemate:
            return STALEMATE

    for row in range(8):
        for col in range(8):
            team = gs.board[row][col][:5]
            piece = gs.board[row][col][6:]
            if piece == "pawn":
                if team == "black":
                    score = score +1
                else:
                    score = score -1
            if piece == "bishop":
                if team == "black":
                    score = score +1
                else:
                    score = score -1
            if piece == "knight":
                if team == "black":
                    score = score +3
                else:
                    score = score -3
            if piece == "rook":
                if team == "black":
                    score = score +5
                else:
                    score = score -5
            if piece == "queen":
                if team == "black":
                    score = score +9
                else:
                    score = score -9
    return score