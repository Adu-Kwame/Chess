from typing import ParamSpec

class GameState():
    def __init__(self):
        self.board = [
        ["black_rook","black_knight","black_bishop","black_queen","black_king","black_bishop","black_knight","black_rook"],
        ["black_pawn","black_pawn","black_pawn","black_pawn","black_pawn","black_pawn","black_pawn","black_pawn"],
        ["e","e","e","e","e","e","e","e"],
        ["e","e","e","e","e","e","e","e"],
        ["e","e","e","e","e","e","e","e"],
        ["e","e","e","e","e","e","e","e"],
        ["white_pawn","white_pawn","white_pawn","white_pawn","white_pawn","white_pawn","white_pawn","white_pawn"],
        ["white_rook","white_knight","white_bishop","white_queen","white_king","white_bishop","white_knight","white_rook"],
        ]
        self.board1 =  [
        ["e","e","e","e","black_king","e","e","e"],
        ["e","e","e","e","e","e","e","e"],
        ["e","e","e","e","e","e","e","e"],
        ["e","e","e","e","white_rook","e","e","e"],
        ["e","e","e","e","e","e","e","e"],
        ["e","e","e","e","e","e","e","e"],
        ["e","e","e","e","e","e","e","e"],
        ["e","e","e","e","white_king","e","e","e"],
        ]

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLoc = (7,4)
        self.blackKingLoc = (0,4)
        self.whiteQueenCastle = True
        self.whiteKingCastle = True
        self.blackQueenCastle = True
        self.blackKingCastle = True
        self.kingMoveCount = 0
        self.checkmate = False
        self.stalemate = False
        self.game = True
    
 
    def makeMove(self, move):
        if move.pieceMoved != "e": 
            self.board[move.startRow][move.startCol] = "e"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)
            self.whiteToMove = not self.whiteToMove 
        if move.castleMove == True: #moves the rook for castling
            if move.endCol - move.startCol == 2: #kingside
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "e"
            else: #queenside
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "e"    
        if move.pieceMoved == "white_king":#checks if the king or rook moves 
            self.whiteKingLoc = (move.endRow,move.endCol)
            self.whiteKingCastle = False
            self.whiteQueenCastle = False
        elif move.pieceMoved == "black_king":
            self.blackKingLoc = (move.endRow,move.endCol)
            self.blackKingCastle = False
            self.blackQueenCastle = False
        elif move.pieceMoved == "white_rook" and move.startCol == 0:
            self.whiteQueenCastle = False
        elif move.pieceMoved == "white_rook" and move.startCol == 7:
            self.whiteKingCastle = False
        elif move.pieceMoved == "black_rook" and move.startCol == 0:
            self.blackQueenCastle = False
        elif move.pieceMoved == "black_rook" and move.startCol == 7:
            self.blackKingCastle = False
        elif move.pieceMoved == "white_pawn" and move.endRow == 0: self.board[move.endRow][move.endCol] = "white_queen"
        elif move.pieceMoved == "black_pawn" and move.endRow == 7: self.board[move.endRow][move.endCol] = "black_queen"
                        
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured 
            self.whiteToMove = not self.whiteToMove 
        if move.castleMove:
            if move.endCol - move.startCol == 2: #kingside
                if self.whiteToMove:
                    self.board[move.endRow][move.endCol+1] = "white_rook"
                    self.whiteKingCastle = True
                else:
                    self.board[move.endRow][move.endCol+1] = "black_rook"
                    self.blackKingCastle = True
            else: #queenside
                if self.whiteToMove:
                    self.board[move.endRow][move.endCol-2] = "white_rook"
                    self.board[move.endRow][move.endCol+1] = "e"
                    self.whiteQueenCastle = True
                else:
                    self.board[move.endRow][move.endCol-2] = "black_rook"
                    self.blackQueenCastle = True
        if move.pieceMoved[6:] == "king":
            if move.pieceMoved[:5] == "white":
                self.whiteKingLoc = (move.startRow,move.startCol)
                self.whiteKingCastle = True
                self.whiteQueenCastle = True
            else:
                self.blackKingLoc == (move.startRow,move.startCol)
                self.blackKingCastle = True 
                self.blackQueenCastle = True
        if move.pieceMoved[6:] == "rook":
            if move.startCol == 0:
                if move.pieceMoved[:5] == "white": 
                    self.whiteQueenCastle = True
                else:
                    self.blackQueenCastle = True
            elif move.startCol == 7:
                if move.pieceMoved[:5] == "white": 
                    self.whiteKingCastle = True
                else:
                    self.blackKingCastle = True


    def validMoves(self):
        moves = self.possibleMoves()
        for m in range(len(moves)-1, -1, -1):#removes any moves that will lead to put themselves in check
            self.makeMove(moves[m]) 
            self.whiteToMove = not self.whiteToMove
            if self.inCheck() == True:
                moves.remove(moves[m])
            self.whiteToMove = not self.whiteToMove        
            self.undoMove()
        if len(moves) == 0 and self.inCheck():
            self.checkmate = True
        elif len(moves) == 0 and self.inCheck() == False:
            self.stalemate = True
        elif self.kingMoveCount == 0 and self.inCheck():
            self.checkmate = True
        else:
            self.stalemate = False
            self.checkmate = False
        if self.game == False:
            print("Game has ended")
        return moves
        

    def inCheck(self):#checks if the king is being attacked
        if self.whiteToMove:
            return self.attackedArea(self.whiteKingLoc[0], self.whiteKingLoc[1],"white_king")
        else:
            return self.attackedArea(self.blackKingLoc[0], self.blackKingLoc[1],"black_king")

    def attackedArea(self,row,col,piece):
        self.whiteToMove = not self.whiteToMove
        enemyMoves = self.possibleMoves()
        self.whiteToMove = not self.whiteToMove
        for m in enemyMoves:#checks if any move from the enemy team attacks a specific piece
            if (m.endRow == row and m.endCol == col) or m.pieceCaptured == piece:
                return True
        return False

    def possibleMoves(self):
        #calculates all possible moves for every piece
        self.moves = []
        for row in range(8):
            for col in range(8):
                team = self.board[row][col][:5]
                piece = self.board[row][col][6:]
                if (team == "white" and self.whiteToMove == True) or (team == "black" and self.whiteToMove == False):
                    if piece == "pawn":
                        self.pawnMoves(row,col,self.moves,team)
                    if piece == "knight":
                        self.knightMoves(row,col,self.moves,team)
                    if piece == "bishop":
                        self.bishopMoves(row,col,self.moves,team)
                    if piece == "rook":
                        self.rookMoves(row,col,self.moves,team)
                    if piece == "queen":
                        self.queenMoves(row,col,self.moves,team)
                    if piece == "king":
                        self.kingMoves(row,col,self.moves,team)
        return self.moves
 
    def pawnMoves(self,row,col,moves,team):
        if team == 'white':
            if self.board[row-1][col] == "e":
                self.moves.append(Move((row,col),(row-1,col), self.board))
                if row == 6 and self.board[row-2][col] == "e":
                    self.moves.append(Move((row,col),(row-2,col), self.board))
            if col != 7:
                if self.board[row-1][col+1][:5] != team and self.board[row-1][col+1] != "e":
                    self.moves.append(Move((row,col),(row-1,col+1), self.board))
            if col != 0:
                if self.board[row-1][col-1][:5] != team and self.board[row-1][col-1] != "e":
                    self.moves.append(Move((row,col),(row-1,col-1), self.board))
        else:
            if self.board[row+1][col] == "e":
                self.moves.append(Move((row,col),(row+1,col), self.board))
                if row == 1 and self.board[row+2][col] == "e":
                    self.moves.append(Move((row,col),(row+2,col), self.board))
            if col != 7:
                if self.board[row+1][col+1][:5] != team and self.board[row+1][col+1] != "e":
                    self.moves.append(Move((row,col),(row+1,col+1), self.board))
            if col != 0:
                if self.board[row+1][col-1][:5] != team and self.board[row+1][col-1] != "e":
                    self.moves.append(Move((row,col),(row+1,col-1), self.board))
    def knightMoves(self,row,col,moves,team):
        if not(row-2 < 0 or col-1 < 0):
            if self.board[row-2][col-1] == "e" or self.board[row-2][col-1][:5] != team:
                self.moves.append(Move((row,col),(row-2,col-1), self.board))
        if not(row-2 < 0 or col+1 >= 8):
            if self.board[row-2][col+1] == "e" or self.board[row-2][col+1][:5] != team:
                self.moves.append(Move((row,col),(row-2,col+1), self.board))
        if not(row-1 < 0 or col+2 >= 8):
            if self.board[row-1][col+2] == "e" or self.board[row-1][col+2][:5] != team:
                self.moves.append(Move((row,col),(row-1,col+2), self.board))
        if not(row+1 >= 8 or col+2 >= 8):
            if self.board[row+1][col+2] == "e" or self.board[row+1][col+2][:5] != team:
                self.moves.append(Move((row,col),(row+1,col+2), self.board))
        if not(row-1 < 0 or col-2 < 0):
            if self.board[row-1][col-2] == "e" or self.board[row-1][col-2][:5] != team:
                self.moves.append(Move((row,col),(row-1,col-2), self.board))
        if not(row+1 >= 8 or col-2 < 0):
            if self.board[row+1][col-2] == "e" or self.board[row+1][col-2][:5] != team:
                self.moves.append(Move((row,col),(row+1,col-2), self.board))
        if not(row+2 >= 8 or col+1 >= 8):
            if self.board[row+2][col+1] == "e" or self.board[row+2][col+1][:5] != team:
                self.moves.append(Move((row,col),(row+2,col+1), self.board))
        if not(row+2 >= 8 or col-1 < 0):
            if self.board[row+2][col-1] == "e" or self.board[row+2][col-1][:5] != team:
                self.moves.append(Move((row,col),(row+2,col-1), self.board))
        pass
    def bishopMoves(self,row,col,moves,team):
        for x in range(1,8):#checks for all valid moves going top-left
            if not(row-x < 0) and not(col-x < 0):
                if self.board[row-x][col-x] == "e":
                    self.moves.append(Move((row,col),(row-x,col-x), self.board))
                elif self.board[row-x][col-x][:5] != team:
                    self.moves.append(Move((row,col),(row-x,col-x), self.board))
                    break
                else: break
            else: break
        for x in range(1,8):#checks for all valid moves going botton-right
            if not(row+x >= 8) and not(col+x >= 8):
                if self.board[row+x][col+x] == "e":
                    self.moves.append(Move((row,col),(row+x,col+x), self.board))
                elif self.board[row+x][col+x][:5] != team:
                    self.moves.append(Move((row,col),(row+x,col+x), self.board))
                    break
                else: break
            else: break


        for x in range(1,8):
            if not(row-x < 0) and not(col+x >= 8) :#checks for all valid moves going top-right
                if self.board[row-x][col+x] == "e":
                    self.moves.append(Move((row,col),(row-x,col+x), self.board))
                elif self.board[row-x][col+x][:5] != team:
                    self.moves.append(Move((row,col),(row-x,col+x), self.board))
                    break
                else: break
            else: break
        
        for x in range(1,8):
            if not(row+x >= 8) and not(col-x < 0):#checks for all valid moves going bottom-left
                if self.board[row+x][col-x] == "e":
                    self.moves.append(Move((row,col),(row+x,col-x), self.board))
                elif self.board[row+x][col-x][:5] != team:
                    self.moves.append(Move((row,col),(row+x,col-x), self.board))
                    break
                else: break
            else: break     
    def rookMoves(self,row,col,moves,team):
        for x in range(1,row+1):#checks for all valid moves going up
            if self.board[row-x][col] == "e":
                self.moves.append(Move((row,col),(row-x,col), self.board))
            elif  self.board[row-x][col][:5] != team:
                self.moves.append(Move((row,col),(row-x,col), self.board))
                break
            else: break

        for x in range(1,8):#checks for all valid moves going down
            if not(row+x >= 8):
                if self.board[row+x][col] == "e":
                    self.moves.append(Move((row,col),(row+x,col), self.board))
                elif self.board[row+x][col][:5] != team:
                    self.moves.append(Move((row,col),(row+x,col), self.board))
                    break
                else: break
            else: break
        for x in range(1,col+1):#checks for all valid moves going left
            if self.board[row][col-x] == "e":
                self.moves.append(Move((row,col),(row,col-x), self.board))
            elif self.board[row][col-x][:5] != team:
                self.moves.append(Move((row,col),(row,col-x), self.board))
                break 
            else: break 
       
        for x in range(1,8):#checks for all valid moves going right
            if not(col+x >= 8):
                if self.board[row][col+x] == "e":
                    self.moves.append(Move((row,col),(row,col+x), self.board))
                elif self.board[row][col+x][:5] != team:
                    self.moves.append(Move((row,col),(row,col+x), self.board))
                    break
                else: break
            else: break        
    def queenMoves(self,row,col,moves,team):
        self.rookMoves(row,col,moves,team)
        self.bishopMoves(row,col,moves,team)
        pass
    def kingMoves(self,row,col,moves,team):
        kingMoves = ((-1,-1),(-1,0),(0,-1),(1,0),(0,1),(1,1),(1,-1),(-1,1))
        self.kingMoveCount == 0
        for x in range(8):
            endRow = row + kingMoves[x][0]
            endCol = col + kingMoves[x][1]
            if (0 <= endRow < 8) and (0 <= endCol < 8): 
                endPos = self.board[endRow][endCol]
                if endPos[:5] != team:
                    self.moves.append(Move((row,col),(endRow,endCol), self.board))
                    self.kingMoveCount = self.kingMoveCount+1
        if self.whiteKingLoc == (7,4) and team == "white":
            if self.whiteKingCastle == True:
                if self.board[row][col+1] == "e" and self.board[row][col+2] == "e":
                    self.moves.append(Move((row,col),(row,col+2), self.board, True))
            if self.whiteQueenCastle == True:
                if self.board[row][col-1] == "e" and self.board[row][col-2] and self.board[row][col-3] == "e":
                    self.moves.append(Move((row,col),(row,col-2), self.board, True))
        if self.blackKingLoc == (0,4) and team == "black":
            if self.blackKingCastle == True:
                if self.board[row][col+1] == "e" and self.board[row][col+2] == "e":
                    self.moves.append(Move((row,col),(row,col+2), self.board, True))
            if self.blackQueenCastle == True:
                if self.board[row][col-1] == "e" and self.board[row][col-2] == "e" and self.board[row][col-3] == "e":
                    self.moves.append(Move((row,col),(row,col-2), self.board, True))

class Move():
    #creates a class of move that has the details of the move 
    def __init__(self, startSq, endSq, board, castleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1] 
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow + self.startCol*10 + self.endRow*100 +self.endCol*1000
        self.castleMove = castleMove

    def __eq__(self,other):
        #allows move classes to be compared by their moveID 
        if isinstance(other,Move):
            return self.moveID == other.moveID
        else:
            return False
