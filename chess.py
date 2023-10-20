# TO DO
# Add en passant
# Add capture noti to last move display / update error messages to be more elegant + not output them at the top of the screen too
# GUI (probably not)
# Make second game mode with special abilities?
# Implement Player vs AI
# Tune and test eval function
# Possibly AI vs AI training for practice
# Doubled pawn penalty
# Queen and bishop on same diagonal buff
# pawn diagonal buff
# higher buff for moving bishop and knight eary
import copy
# board creation
global board
board = [[]]
global lastMove
lastMove = ""
global whiteKingPos, blackKingPos
whiteKingPos = [7, 4]
blackKingPos = [0, 4]
global inCheckBy
inCheckBy = ""
global turn_counter
turn_counter = 0
global tookpiece
tookpiece = "             "
global setTookPieceFlag
setTookPieceFlag = False
# pieces
class Rook:
    # constructor
    def __init__(self, owner):
        self.owner = owner
        self.hasMoved = False
    # to string
    def __str__(self):
        return "  " + self.owner + " Rook  "
    def ezString(self):
        return " Rook "
    # move
    def move(self, startRow, startCol, endRow, endCol, flag):
        # verify that the move stated is a legal rook move
        if verifyRook(startRow, startCol, endRow, endCol):
            return "That is not a valid move. Try again."
        global board
        global tookpiece
        # horizontal movement
        if startRow == endRow:
            if startCol > endCol:
                counter = startCol - 1
                while counter > endCol:
                    if board[startRow][counter] != "              ":
                        return "That move is blocked, try again"
                    counter = counter - 1
            else:
                if endCol > startCol:
                    counter = endCol - 1
                    while counter > startCol:
                        if board[startRow][counter] != "              ":
                            return "That move is blocked, try again"
                        counter = counter - 1
        # vertical movement
        else:
            if startCol == endCol:
                if startRow > endRow:
                    counter = startRow - 1
                    while counter > endRow:
                        if board[counter][startCol] != "              ":
                            return "That move is blocked, try again"
                        counter = counter - 1
                else:
                    if endRow > startRow:
                        counter = endRow - 1
                        while counter > startRow:
                            if board[counter][startCol] != "              ":
                                return "That move is blocked, try again"
                            counter = counter - 1
        # once we verify that the pathway is open
        if board[endRow][endCol] == "              " or (self.owner == "White" and board[endRow][endCol].owner == "Black") or (self.owner == "Black" and board[endRow][endCol].owner == "White"):
                hold = board[endRow][endCol]
                board[endRow][endCol] = self
                board[startRow][startCol] = "              "
                if isCheck(self.owner, flag):
                    board[endRow][endCol] = hold
                    board[startRow][startCol] = self
                    return "You are in check or this move would put you in check and is illegal. Try again."
                tookpiece = detTP2(hold)
                self.hasMoved = True
                return "Success"
        else:
                return "you cannot take your own piece"
            

class Knight:
    # constructor
    def __init__(self, owner):
        self.owner = owner
    # to string
    def __str__(self):
        return " " + self.owner + " Knight "
    def ezString(self):
        return " Knight "
    # move
    def move(self, startRow, startCol, endRow, endCol, flag):
        global board
        global tookpiece
        # ensure that move is a legal knight move
        if (startRow - endRow == 2 and startCol - endCol == 1) or (startRow - endRow == 2 and endCol - startCol == 1) or (endRow - startRow == 2 and endCol - startCol == 1) or (endRow - startRow == 2 and startCol - endCol == 1) or (startRow - endRow == 1 and startCol - endCol == 2) or (startRow - endRow == 1 and endCol - startCol == 2) or (endRow - startRow == 1 and endCol - startCol == 2) or (endRow - startRow == 1 and startCol - endCol == 2):
            # ensure spot is empty or not your own piece in case of a capture
            if board[endRow][endCol] == "              " or (self.owner == "White" and board[endRow][endCol].owner == "Black") or (self.owner == "Black" and board[endRow][endCol].owner == "White"):
                hold = board[endRow][endCol]
                board[endRow][endCol] = self
                board[startRow][startCol] = "              "
                if isCheck(self.owner, flag):
                    board[endRow][endCol] = hold
                    board[startRow][startCol] = self
                    return "would put you in check or does not deal with current check, try again"
                tookpiece = detTP2(hold)
                return "Success"
            else:
                return "space isn't empty and is occupied by one of your pieces"
        else:
            return "invalid knight move"

class Bishop:
    def __init__(self, owner):
        self.owner = owner
    def __str__(self):
        return " " + self.owner + " Bishop "
    def ezString(self):
        return " Bishop "
    def move(self, startRow, startCol, endRow, endCol, flag):
        if verifyBishop(startRow, startCol, endRow, endCol):
            return "illegal move"
        global board
        global tookpiece
        if startRow > endRow and startCol > endCol:
            counter1 = startRow - 1
            counter2 = startCol - 1
            while counter1 > endRow:
                if board[counter1][counter2] != "              ":
                    return "move blocked"
                counter1 = counter1 - 1
                counter2 = counter2 - 1
        else:
            if startRow < endRow and startCol > endCol:
                counter1 = startRow + 1
                counter2 = startCol - 1
                while counter1 < endRow:
                    if board[counter1][counter2] != "              ":
                        return "move blocked"
                    counter1 = counter1 + 1
                    counter2 = counter2 - 1
            else:
                if startRow < endRow and startCol < endCol:
                    counter1 = endRow - 1
                    counter2 = endCol - 1
                    while counter1 > startRow:
                        if board[counter1][counter2] != "              ":
                            return "move blocked"
                        counter1 = counter1 - 1
                        counter2 = counter2 - 1
                else:
                    if startRow > endRow and startCol < endCol:
                        counter1 = startRow - 1
                        counter2 = startCol + 1
                        while counter1 > endRow:
                            if board[counter1][counter2] != "              ":
                                return "move blocked"
                            counter1 = counter1 - 1
                            counter2 = counter2 + 1
        
        if board[endRow][endCol] == "              " or (self.owner == "White" and board[endRow][endCol].owner == "Black") or (self.owner == "Black" and board[endRow][endCol].owner == "White"):
                hold = board[endRow][endCol]
                board[endRow][endCol] = self
                board[startRow][startCol] = "              "
                if isCheck(self.owner, flag):
                    board[endRow][endCol] = hold
                    board[startRow][startCol] = self
                    return "you are in check / this move would put you in check and is illegal"
                tookpiece = detTP2(hold)
                return "Success"
        else:
                return "you cannot take your own piece"

class Pawn:
    def __init__(self, owner):
        self.owner = owner   
        self.hasMoved = False
    def __str__(self):
        return "  " + self.owner + " Pawn  "
    def ezString(self):
        return " Pawn "
    def promote(self, row, col):
        if (self.owner == "White" and row == 0) or (self.owner == "Black" and row == 7):
            if self.owner == "White":
                toProm = "Queen"
            else:
                toProm = input("type selection for promotion, capitalise first letter, i.e. Rook: ")
            if toProm == "Queen":
                q = Queen(self.owner)
                board[row][col] = q
            else:
                if toProm == "Rook":
                    q = Rook(self.owner)
                    board[row][col] = q
                else:
                    if toProm == "Knight":
                        q = Knight(self.owner)
                        board[row][col] = q
                    else:
                        if toProm == "Bishop":
                            q = Bishop(self.owner)
                            board[row][col] = q
                        else:
                            return "illegal promotion, can only promote to Queen, Rook, Knight, or Bishop"
    def move(self, x, y, m, n, flag):
        global board
        global tookpiece
        if self.owner == "White":
            
                if y == n:
                    if x - m == 2 and self.hasMoved == False:
                        if board[x - 1][y] == "              " and board[x - 2][y] == "              ":
                            hold = board[m][n]
                            board[m][n] = self
                            board[x][y] = "              "
                            
                            if isCheck(self.owner, flag):
                                board[m][n] = hold
                                board[x][y] = self
                                return "would put you in check, illegal OR does not prevent you from being in check"
                            tookpiece = detTP2(hold)
                            self.hasMoved = True
                            return "Success"
                        else:
                            return "Piece blocked"
                    else:
                        if x - m == 1:
                            if board[x - 1][y] == "              ":
                                hold = board[m][n]
                                board[m][n] = self
                                board[x][y] = "              "
                                if isCheck(self.owner, flag):
                                    board[m][n] = hold
                                    board[x][y] = self
                                    return "would put you in check, illegal OR does not prevent you from being in check"
                                tookpiece = detTP2(hold)
                                self.promote(m, n)
                                self.hasMoved = True
                                return "Success"
                            else:
                                return "Piece blocked"
                        else:
                            return "invalid move, too far forwards or backwards with a pawn"
                else:
                    if abs(y - n) == 1:
                        if m == x - 1:
                            if board[m][n] != "              ":
                                if board[m][n].owner == "Black":
                                    hold = board[m][n]
                                    board[m][n] = self
                                    board[x][y] = "              "
                                    if isCheck(self.owner, flag):
                                        board[m][n] = hold
                                        board[x][y] = self
                                        return "would put you in check, illegal OR does not prevent you from being in check"
                                    self.promote(m, n)
                                    tookpiece = detTP2(hold)
                                    self.hasMoved = True
                                    return "Success"
                                else:
                                    return "cannot capture your own piece"
                            else:
                                return "no piece to capture there"
                        else:
                            return "too far away"
                    else:
                        return "too far away"
        else:
                        
                if y == n:
                    if m - x == 2 and self.hasMoved == False:
                        if board[x + 1][y] == "              " and board[x + 2][y] == "              ":
                            hold = board[m][n]
                            board[m][n] = self
                            board[x][y] = "              "
                            if isCheck(self.owner, flag):
                                board[m][n] = hold
                                board[x][y] = self
                                return "would put you in check, illegal OR does not prevent you from being in check"
                            tookpiece = detTP2(hold)
                            self.hasMoved = True
                            return "Success"
                        else:
                            return "Piece blocked"
                    else:
                        if m - x == 1:
                            if board[x + 1][y] == "              ":
                                hold = board[m][n]
                                board[m][n] = self
                                board[x][y] = "              "
                                if isCheck(self.owner, flag):
                                    board[m][n] = hold
                                    board[x][y] = self
                                    return "would put you in check, illegal OR does not prevent you from being in check"
                                tookpiece = detTP2(hold)
                                self.promote(m, n)
                                self.hasMoved = True
                                return "Success"
                            else:
                                return "Piece blocked"
                        else:
                            return "invalid move, too far forwards or backwards with a pawn"
                else:
                    if abs(y - n) == 1:
                        if m == x + 1:
                            if board[m][n] != "              ":
                                if board[m][n].owner == "White":
                                    hold = board[m][n]
                                    board[m][n] = self
                                    board[x][y] = "              "
                                    if isCheck(self.owner, flag):
                                        board[m][n] = hold
                                        board[x][y] = self
                                        return "would put you in check, illegal OR does not prevent you from being in check"
                                    tookpiece = detTP2(hold)
                                    self.promote(m, n)
                                    self.hasMoved = True
                                    return "Success"
                                else:
                                    return "cannot capture your own piece"
                            else:
                                return "no piece to capture there"
                        else:
                            return "too far away"
                    else:
                        return "too far away"

class Queen:
    def __init__(self, owner):
        self.owner = owner
    def __str__(self):
        return " " + self.owner + " Queen  "
    def ezString(self):
        return " Queen "
    def move(self, startRow, startCol, endRow, endCol, flag):
        if verifyRook(startRow, startCol, endRow, endCol) and verifyBishop(startRow, startCol, endRow, endCol):
            return "Illegal queen move."
        if not verifyRook(startRow, startCol, endRow, endCol):
            r = Rook(self.owner)
        if not verifyBishop(startRow, startCol, endRow, endCol):
            r = Bishop(self.owner)
        status = r.move(startRow, startCol, endRow, endCol, flag)
        if status == "Success":
            hold = board[endRow][endCol]
            board[endRow][endCol] = self
            board[startRow][startCol] = "              "
            if isCheck(self.owner, flag):
                board[endRow][endCol] = hold
                board[startRow][startCol] = self
                return "would put you in check or does not prevent you from being in check"
            return "Success"
        else:
            board[startRow][startCol] = self
            return status

class King:
    def __init__(self, owner):
        self.owner = owner
        self.hasMoved = False
        self.hasBeenChecked = False
    def __str__(self):
        return "  " + self.owner + " King  "
    def ezString(self):
        return " King "
    # if move is more than 1 spot in horizontal fashion, check if trying to castle
    # check if king has moved or been checked. if so, failure
    # check if direction of move still has rook unmoved in original position
    # check if there is anything blocking, or if there is something checking in the way
    def castle(self, startRow, startCol, direction, flag):
        global board
        global whiteKingPos
        global blackKingPos
        if self.hasMoved == False and self.hasBeenChecked == False and not isCheck(self.owner, flag):
            if direction == "Queenside":
                if isinstance(board[startRow][0], Rook):
                    if board[startRow][0].hasMoved == False:
                        if board[startRow][1] == "              " and board[startRow][2] == "              " and board[startRow][3] == "              ":
                            board[startRow][3] = self
                            if self.owner == "White":
                                whiteKingPos = [startRow, 3]
                            else:
                                blackKingPos = [startRow, 3]
                            board[startRow][4] = "              "
                            if isCheck(self.owner, flag):
                                board[startRow][startCol] = self
                                if self.owner == "White":
                                    whiteKingPos = [startRow, startCol]
                                else:
                                    blackKingPos = [startRow, startCol]
                                board[startRow][3] = "              "
                                return "checking piece is blocking castle"
                            board[startRow][2] = self
                            if self.owner == "White":
                                whiteKingPos = [startRow, 2]
                            else:
                                blackKingPos = [startRow, 2]
                            board[startRow][3] = "              "
                            if isCheck(self.owner, flag):
                                board[startRow][startCol] = self
                                if self.owner == "White":
                                    whiteKingPos = [startRow, startCol]
                                else:
                                    blackKingPos = [startRow, startCol]
                                board[startRow][2] = "              "
                                return "checking piece is blocking castle"
                            board[startRow][3] = board[startRow][0]
                            board[startRow][0] = "              "
                            self.hasMoved = True
                            board[startRow][3].hasMoved = True
                            return "Success"
                        else:
                            return "pieces blocking castle"
                    else:
                        return "That rook has moved and you cannot castle that side"
                else:
                    return "There is not a rook on that side to castle with"
            else:
                if isinstance(board[startRow][7], Rook):
                    if board[startRow][7].hasMoved == False:
                        if board[startRow][6] == "              " and board[startRow][5] == "              ":
                            board[startRow][5] = self
                            if self.owner == "White":
                                whiteKingPos = [startRow, 5]
                            else:
                                blackKingPos = [startRow, 5]
                            board[startRow][4] = "              "
                            if isCheck(self.owner, flag):
                                board[startRow][startCol] = self
                                if self.owner == "White":
                                    whiteKingPos = [startRow, startCol]
                                else:
                                    blackKingPos = [startRow, startCol]
                                board[startRow][5] = "              "
                                return "checking piece is blocking castle"
                            board[startRow][6] = self
                            if self.owner == "White":
                                whiteKingPos = [startRow, 6]
                            else:
                                blackKingPos = [startRow, 6]
                            board[startRow][5] = "              "
                            if isCheck(self.owner, flag):
                                board[startRow][startCol] = self
                                if self.owner == "White":
                                    whiteKingPos = [startRow, startCol]
                                else:
                                    blackKingPos = [startRow, startCol]
                                board[startRow][6] = "              "
                                return "checking piece is blocking castle"
                            board[startRow][5] = board[startRow][7]
                            board[startRow][7] = "              "
                            self.hasMoved = True
                            board[startRow][5].hasMoved = True
                            return "Success"
                        else:
                            return "pieces blocking castle"
                    else:
                        return "That rook has moved and you cannot castle that side"
                else:
                    return "There is not a rook on that side to castle with"
        else:
            return "either you are trying to illegally castle (your king has been moved already, or has been in check) or this is an illegal king move otherwise."

    def move(self, startRow, startCol, endRow, endCol, flag):
        global board
        global whiteKingPos
        global blackKingPos
        global tookpiece
        if startCol - endCol > 1:
            return self.castle(startRow, startCol, "Queenside", flag)
        if endCol - startCol > 1:
            return self.castle(startRow, startCol, "Kingside" , flag)
        if abs(startRow - endRow) > 1:
            return "Illegal king move, too far"
        if board[endRow][endCol] == "              " or (self.owner == "White" and board[endRow][endCol].owner == "Black") or (self.owner == "Black" and board[endRow][endCol].owner == "White"):
                hold = board[endRow][endCol]
                board[endRow][endCol] = self
                if self.owner == "White":
                    whiteKingPos = [endRow, endCol]
                else:
                    blackKingPos = [endRow, endCol]
                board[startRow][startCol] = "              "
                if isCheck(self.owner, flag):
                    board[endRow][endCol] = hold
                    if self.owner == "White":
                        whiteKingPos = [startRow, startCol]
                    else:
                        blackKingPos = [startRow, startCol]
                    board[startRow][startCol] = self
                    return "you are in check / this move would put you in check and is illegal"
                tookpiece = detTP2(hold)
                self.hasMoved = True
                return "Success"
        else:
            return "you cannot take your own piece"
        
        
# checks if the referenced player is in check
# check if first piece on kings column and row is a foe and is a rook or queen
# check if first piece on each diagonal is a queen or bishop, and if the immediate diagonal spots are enemy pawns
def isCheck(player, flag):
    global board
    global whiteKingPos
    global blackKingPos
    loop = 0
    kingR = 0
    kingC = 0
    if player == "White":
        kingR = whiteKingPos[0]
        kingC = whiteKingPos[1]
    else:
        kingR = blackKingPos[0]
        kingC = blackKingPos[1]
    #check row to the left
    loop = kingC - 1
    while loop >= 0:
        if board[kingR][loop] == "              ":
            loop = loop - 1
        else:
            if board[kingR][loop].owner != player and (isinstance(board[kingR][loop], Queen) or isinstance(board[kingR][loop], Rook)):
                if flag == 1:
                    board[kingR][kingC].hasBeenChecked = True
                return True
            break
    # check row to right
    loop = kingC + 1
    while loop <= 7:
        if board[kingR][loop] == "              ":
            loop = loop + 1
        else:
            if board[kingR][loop].owner != player and (isinstance(board[kingR][loop], Queen) or isinstance(board[kingR][loop], Rook)):
                if flag == 1:
                    board[kingR][kingC].hasBeenChecked = True
                return True
            break
    # check column up
    loop = kingR - 1
    while loop >= 0:
        if board[loop][kingC] == "              ":
            loop = loop - 1
        else:
            if board[loop][kingC].owner != player and (isinstance(board[loop][kingC], Queen) or isinstance(board[loop][kingC], Rook)):
                if flag == 1:
                    board[kingR][kingC].hasBeenChecked = True
                return True
            break
    # check column down
    loop = kingR + 1
    while loop <= 7:
        if board[loop][kingC] == "              ":
            loop = loop + 1
        else:
            if board[loop][kingC].owner != player and (isinstance(board[loop][kingC], Queen) or isinstance(board[loop][kingC], Rook)):
                if flag == 1:
                    board[kingR][kingC].hasBeenChecked = True
                return True
            break
    # check if immediate diags are enemy pawns
    if player == "White" and kingR != 0 and ((kingR - 1 >= 0 and kingC + 1 < 8 and isinstance(board[kingR - 1][kingC + 1], Pawn) and board[kingR - 1][kingC + 1].owner != player) or (kingR - 1 >= 0 and kingC - 1 >= 0 and isinstance(board[kingR - 1][kingC - 1], Pawn) and board[kingR - 1][kingC - 1].owner != player)):
        if flag == 1:
                    board[kingR][kingC].hasBeenChecked = True
        return True
    if player == "Black" and kingR != 7 and ((kingR + 1 < 8 and kingC + 1 < 8 and isinstance(board[kingR + 1][kingC + 1], Pawn) and board[kingR + 1][kingC + 1].owner != player) or (kingR + 1 < 8 and kingC - 1 >= 0 and isinstance(board[kingR + 1][kingC - 1], Pawn) and board[kingR + 1][kingC - 1].owner != player)):
        if flag == 1:
                    board[kingR][kingC].hasBeenChecked = True
        return True
    # check up left diagonal
    loop = kingR - 1
    loop2 = kingC - 1
    while loop >= 0 and loop2 >= 0:
        if board[loop][loop2] == "              ":
            loop = loop - 1
            loop2 = loop2 - 1
        else:
            if board[loop][loop2].owner != player and (isinstance(board[loop][loop2], Queen) or isinstance(board[loop][loop2], Bishop)):
                # print("is getting here some how " + str(loop) + " " + str(loop2))
                if flag == 1:
                    board[kingR][kingC].hasBeenChecked = True
                return True
            break
    # check up right diagonal
    loop = kingR - 1
    loop2 = kingC + 1
    while loop >= 0 and loop2 <= 7:
        if board[loop][loop2] == "              ":
            loop = loop - 1
            loop2 = loop2 + 1
        else:
            if board[loop][loop2].owner != player and (isinstance(board[loop][loop2], Queen) or isinstance(board[loop][loop2], Bishop)):
                if flag == 1:
                    board[kingR][kingC].hasBeenChecked = True
                return True
            break
    # check down left diagonal
    loop = kingR + 1
    loop2 = kingC - 1
    while loop <= 7 and loop2 >= 0:
        if board[loop][loop2] == "              ":
            loop = loop + 1
            loop2 = loop2 - 1
        else:
            if board[loop][loop2].owner != player and (isinstance(board[loop][loop2], Queen) or isinstance(board[loop][loop2], Bishop)):
                if flag == 1:
                    board[kingR][kingC].hasBeenChecked = True
                return True
            break
    # check down right diagonal
    loop = kingR + 1
    loop2 = kingC + 1
    while loop <= 7 and loop2 <= 7:
        if board[loop][loop2] == "              ":
            loop = loop + 1
            loop2 = loop2 + 1
        else:
            if board[loop][loop2].owner != player and (isinstance(board[loop][loop2], Queen) or isinstance(board[loop][loop2], Bishop)):
                if flag == 1:
                    board[kingR][kingC].hasBeenChecked = True
                return True
            break
    if kingR + 1 <= 7 and kingC + 2 <= 7 and isinstance(board[kingR + 1][kingC + 2], Knight) and board[kingR + 1][kingC + 2].owner != player:
        if flag == 1:
            board[kingR][kingC].hasBeenChecked = True
        return True
    if kingR + 1 <= 7 and kingC - 2 >= 0 and isinstance(board[kingR + 1][kingC - 2], Knight) and board[kingR + 1][kingC - 2].owner != player:
        if flag == 1:
            board[kingR][kingC].hasBeenChecked = True
        return True
    if kingR - 1 >= 0 and kingC + 2 <= 7 and isinstance(board[kingR - 1][kingC + 2], Knight) and board[kingR - 1][kingC + 2].owner != player:
        if flag == 1:
            board[kingR][kingC].hasBeenChecked = True
        return True
    if kingR - 1 >= 0 and kingC - 2 >= 0 and isinstance(board[kingR - 1][kingC - 2], Knight) and board[kingR - 1][kingC - 2].owner != player:
        if flag == 1:
            board[kingR][kingC].hasBeenChecked = True
        return True
    if kingR + 2 <= 7 and kingC + 1 <= 7 and isinstance(board[kingR + 2][kingC + 1], Knight) and board[kingR + 2][kingC + 1].owner != player:
        if flag == 1:
            board[kingR][kingC].hasBeenChecked = True
        return True
    if kingR + 2 <= 7 and kingC - 1 >= 0 and isinstance(board[kingR + 2][kingC - 1], Knight) and board[kingR + 2][kingC - 1].owner != player:
        if flag == 1:
            board[kingR][kingC].hasBeenChecked = True
        return True
    if kingR - 2 >= 0 and kingC + 1 <= 7 and isinstance(board[kingR - 2][kingC + 1], Knight) and board[kingR - 2][kingC + 1].owner != player:
        if flag == 1:
            board[kingR][kingC].hasBeenChecked = True
        return True
    if kingR - 2 >= 0 and kingC - 1 >= 0 and isinstance(board[kingR - 2][kingC - 1], Knight) and board[kingR - 2][kingC - 1].owner != player:
        if flag == 1:
            board[kingR][kingC].hasBeenChecked = True
        return True
    return False

def verifyRook(startRow, startCol, endRow, endCol):
    return (startRow != endRow) and (startCol != endCol)

def verifyBishop(startRow, startCol, endRow, endCol):
    return (abs(startRow - endRow) != abs(startCol - endCol))
# loop through each place on the board. If there is a piece there and it belongs to the player calling the function, generate its legal moves
# we do this by if pawn: checking if it has moved, 1 to 2 spaces forward based on that. Check if can capture on diagonals, or can enpassant
def generateMoves(player):
    moves = []
    key = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    key2 = {0 : 8, 1 : 7, 2 : 6, 3 : 5, 4 : 4, 5 : 3, 6 : 2, 7 : 1, 8 : 0}
    global board
    x = 0
    y = 0            # could just copy piece thats moving and piece that is being taken, move, check for success, replace and recopy. Add check flag that won't trigger check function when moving pieces back
    while x < 8: # instead of copying maybe just save flag states and change them back after moving back
        y = 0
        while y < 8:
            piece = board[x][y]
            if piece == "              ":
                next
            elif piece.owner == player:
                if isinstance(piece, Pawn):
                    save_moved = piece.hasMoved
                    if player == "White":
                        if x - 1 >= 0:
                            hold = board[x-1][y]
                        if x - 1 >= 0 and (board[x-1][y] == "              " or board[x-1][y].owner != player) and piece.move(x, y, x - 1, y, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[y] + str(key2[x - 1]))
                            board[x][y] = piece
                            board[x-1][y] = hold
                            piece.hasMoved = save_moved
                        if x - 2 >= 0:
                            hold = board[x-2][y]
                        if x - 2 >= 0 and (board[x-2][y] == "              " or board[x-2][y].owner != player) and piece.move(x, y, x - 2, y, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[y] + str(key2[x - 2]))
                            board[x][y] = piece
                            board[x-2][y] = hold
                            piece.hasMoved = save_moved
                        if x -1>= 0 and y - 1 >= 0:
                             hold = board[x-1][y-1]
                        if x - 1 >= 0 and y - 1 >= 0 and (board[x-1][y-1] == "              " or board[x-1][y-1].owner != player) and  piece.move(x, y, x - 1, y - 1, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[y - 1] + str(key2[x - 1]))
                            board[x][y] = piece
                            board[x-1][y-1] = hold
                            piece.hasMoved = save_moved
                        if x -1>= 0 and y + 1 <= 7:
                            hold = board[x-1][y+1]
                        if x - 1 >= 0 and y + 1 <= 7 and (board[x-1][y+1] == "              " or board[x-1][y+1].owner != player ) and  piece.move(x, y, x - 1, y + 1, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[y + 1] + str(key2[x - 1]))
                            board[x][y] = piece
                            board[x-1][y+1] = hold
                            piece.hasMoved = save_moved
                    else:
                        if x + 1 <= 7:
                            hold = board[x+1][y]
                        if x + 1 <= 7 and (board[x+1][y] == "              " or board[x+1][y].owner != player) and piece.move(x, y, x + 1, y, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[y] + str(key2[x + 1]))
                            board[x][y] = piece
                            board[x+1][y] = hold
                            piece.hasMoved = save_moved
                        if x + 2 <= 7:
                            hold = board[x+2][y]
                        if x + 2 <= 7 and (board[x+2][y] == "              " or board[x+2][y].owner != player) and piece.move(x, y, x + 2, y, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[y] + str(key2[x + 2]))
                            board[x][y] = piece
                            board[x+2][y] = hold
                            piece.hasMoved = save_moved
                        if x + 1 <= 7  and  y - 1 >= 0:
                            hold = board[x+1][y-1]
                        if x + 1 <= 7  and  y - 1 >= 0 and (board[x+1][y-1] == "              " or board[x+1][y-1].owner != player) and piece.move(x, y, x + 1, y - 1, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[y - 1] + str(key2[x + 1]))
                            board[x][y] = piece
                            board[x+1][y-1] = hold
                            piece.hasMoved = save_moved
                        if x + 1 <= 7  and  y + 1 <= 7:
                            hold = board[x+1][y+1]
                        if x + 1 <= 7  and  y + 1 <= 7 and (board[x+1][y+1] == "              " or board[x+1][y+1].owner != player) and piece.move(x, y, x + 1, y + 1, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[y + 1] + str(key2[x + 1]))
                            board[x][y] = piece
                            board[x+1][y+1] = hold
                            piece.hasMoved = save_moved

                elif isinstance(piece, Rook):
                    save_moved = piece.hasMoved
                    vert = x + 1
                    hor = y - 1
                    while vert < 8:
                        hold = board[vert][y]
                        if (board[vert][y] == "              " or board[vert][y].owner != player) and piece.move(x, y, vert, y, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[y] + str(key2[vert]))
                            board[x][y] = piece
                            board[vert][y] = hold
                            piece.hasMoved = save_moved
                        else:
                            break
                        vert = vert + 1
                    vert = x - 1
                    while vert >= 0:
                        hold = board[vert][y]
                        if (board[vert][y] == "              " or board[vert][y].owner != player) and piece.move(x, y, vert, y, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[y] + str(key2[vert]))
                            board[x][y] = piece
                            board[vert][y] = hold
                            piece.hasMoved = save_moved
                        else:
                            break
                        vert = vert - 1
                    while hor >= 0:
                        hold = board[x][hor]
                        if (board[x][hor] == "              " or board[x][hor].owner != player) and piece.move(x, y, x, hor, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[hor] + str(key2[x]))
                            board[x][y] = piece
                            board[x][hor] = hold
                            piece.hasMoved = save_moved
                        else:
                            break
                        hor = hor - 1
                    hor = y + 1
                    while hor < 8:
                        hold = board[x][hor]
                        if (board[x][hor] == "              " or board[x][hor].owner != player) and piece.move(x, y, x, hor, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[hor] + str(key2[x]))
                            board[x][y] = piece
                            board[x][hor] = hold
                            piece.hasMoved = save_moved
                        else:
                            break
                        hor = hor + 1
                    
                elif isinstance(piece, Knight):
                    if x + 2 < 8 and y + 1 < 8:
                        hold = board[x+2][y+1]
                    if x + 2 < 8 and y + 1 < 8 and (board[x+2][y+1] == "              " or board[x+2][y+1].owner != player) and piece.move(x, y, x + 2, y + 1, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y + 1] + str(key2[x + 2]))
                        board[x][y] = piece
                        board[x+2][y+1] = hold
                    if x + 2 < 8 and y - 1 >= 0:
                        hold = board[x+2][y-1]
                    if x + 2 < 8 and y - 1 >= 0 and (board[x+2][y-1] == "              " or board[x+2][y-1].owner != player) and piece.move(x, y, x + 2, y - 1, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y - 1] + str(key2[x + 2]))
                        board[x][y] = piece
                        board[x+2][y-1] = hold
                    if x - 2 >= 0 and y + 1 < 8:
                        hold = board[x-2][y+1]
                    if x - 2 >= 0 and y + 1 < 8 and (board[x-2][y+1] == "              " or board[x-2][y+1].owner != player) and piece.move(x, y, x - 2, y + 1, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y + 1] + str(key2[x - 2]))
                        board[x][y] = piece
                        board[x-2][y+1] = hold
                    if x - 2 >= 0 and y - 1 >= 0:
                        hold = board[x-2][y-1]
                    if x - 2 >= 0 and y - 1 >= 0 and (board[x-2][y-1] == "              " or board[x-2][y-1].owner != player) and piece.move(x, y, x - 2, y - 1, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y - 1] + str(key2[x - 2]))
                        board[x][y] = piece
                        board[x-2][y-1] = hold
                    if y + 2 < 8 and x + 1 < 8:
                        hold = board[x+1][y+2]
                    if y + 2 < 8 and x + 1 < 8 and (board[x+1][y+2] == "              " or board[x+1][y+2].owner != player) and piece.move(x, y, x + 1, y + 2, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y + 2] + str(key2[x + 1]))
                        board[x][y] = piece
                        board[x+1][y+2] = hold
                    if y + 2 < 8 and x - 1 >= 0:
                        hold = board[x-1][y+2]
                    if y + 2 < 8 and x - 1 >= 0 and (board[x-1][y+2] == "              " or board[x-1][y+2].owner != player) and piece.move(x, y, x - 1, y + 2, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y + 2] + str(key2[x - 1]))
                        board[x][y] = piece
                        board[x-1][y+2] = hold
                    if y - 2 >= 0 and x + 1 < 8:
                        hold = board[x+1][y-2]
                    if y - 2 >= 0 and x + 1 < 8 and (board[x+1][y-2] == "              " or board[x+1][y-2].owner != player ) and piece.move(x, y, x + 1, y - 2, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y - 2] + str(key2[x + 1]))
                        board[x][y] = piece
                        board[x+1][y-2] = hold
                    if y - 2 >= 0 and x - 1 >= 0:
                        hold = board[x-1][y-2]
                    if y - 2 >= 0 and x - 1 >= 0 and (board[x-1][y-2] == "              " or board[x-1][y-2].owner != player) and piece.move(x, y, x - 1, y - 2, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y - 2] + str(key2[x - 1]))
                        board[x][y] = piece
                        board[x-1][y-2] = hold

                elif isinstance(piece, Bishop):
                    vert = x - 1
                    hor = y - 1
                    # top left diag
                    while vert >= 0 and hor >= 0:
                        hold = board[vert][hor]
                        if (board[vert][hor] == "              " or board[vert][hor].owner != player) and piece.move(x, y, vert, hor, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[hor] + str(key2[vert]))
                            board[x][y] = piece
                            board[vert][hor] = hold
                        else:
                            break
                        vert = vert - 1
                        hor = hor - 1
                    vert = x - 1
                    hor = y + 1
                    # top right diag
                    while vert >= 0 and hor < 8:
                        hold = board[vert][hor]
                        if (board[vert][hor] == "              " or board[vert][hor].owner != player) and piece.move(x, y, vert, hor, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[hor] + str(key2[vert]))
                            board[x][y] = piece
                            board[vert][hor] = hold
                        else:
                            break
                        vert = vert - 1
                        hor = hor + 1
                    vert = x + 1
                    hor = y - 1
                    # bottom left diag
                    while vert < 8 and hor >= 0:
                        hold = board[vert][hor]
                        if (board[vert][hor] == "              " or board[vert][hor].owner != player) and piece.move(x, y, vert, hor, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[hor] + str(key2[vert]))
                            board[x][y] = piece
                            board[vert][hor] = hold
                        else:
                            break
                        vert = vert + 1
                        hor = hor - 1
                    vert = x + 1
                    hor = y + 1
                    # bottom right diag
                    while vert < 8 and hor < 8:
                        hold = board[vert][hor]
                        if (board[vert][hor] == "              " or board[vert][hor].owner != player) and piece.move(x, y, vert, hor, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[hor] + str(key2[vert]))
                            board[x][y] = piece
                            board[vert][hor] = hold
                        else:
                            break
                        vert = vert + 1
                        hor = hor + 1
                      
                elif isinstance(piece, Queen):
                    vert = x - 1
                    hor = y - 1
                    # top left diag
                    while vert >= 0 and hor >= 0:
                        hold = board[vert][hor]
                        if piece.move(x, y, vert, hor, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[hor] + str(key2[vert]))
                            board[x][y] = piece
                            board[vert][hor] = hold
                        else:
                            break
                        vert = vert - 1
                        hor = hor - 1
                    vert = x - 1
                    hor = y + 1
                    # top right diag
                    while vert >= 0 and hor < 8:
                        hold = board[vert][hor]
                        if piece.move(x, y, vert, hor, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[hor] + str(key2[vert]))
                            board[x][y] = piece
                            board[vert][hor] = hold
                        else:
                            break
                        vert = vert - 1
                        hor = hor + 1
                    vert = x + 1
                    hor = y - 1
                    # bottom left diag
                    while vert < 8 and hor >= 0:
                        hold = board[vert][hor]
                        if piece.move(x, y, vert, hor, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[hor] + str(key2[vert]))
                            board[x][y] = piece
                            board[vert][hor] = hold
                        else:
                            break
                        vert = vert + 1
                        hor = hor - 1
                    vert = x + 1
                    hor = y + 1
                    # bottom right diag
                    while vert < 8 and hor < 8:
                        hold = board[vert][hor]
                        if piece.move(x, y, vert, hor, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[hor] + str(key2[vert]))
                            board[x][y] = piece
                            board[vert][hor] = hold
                        else:
                            break
                        vert = vert + 1
                        hor = hor + 1
                    vert = x + 1
                    hor = y - 1
                    while vert < 8:
                        hold = board[vert][y]
                        if piece.move(x, y, vert, y, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[y] + str(key2[vert]))
                            board[x][y] = piece
                            board[vert][y] = hold
                        else:
                            break
                        vert = vert + 1
                    vert = x - 1
                    while vert >= 0:
                        hold = board[vert][y]
                        if piece.move(x, y, vert, y, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[y] + str(key2[vert]))
                            board[x][y] = piece
                            board[vert][y] = hold
                        else:
                            break
                        vert = vert - 1
                    while hor >= 0:
                        hold = board[x][hor]
                        if piece.move(x, y, x, hor, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[hor] + str(key2[x]))
                            board[x][y] = piece
                            board[x][hor] = hold
                        else:
                            break
                        hor = hor - 1
                    hor = y + 1
                    while hor < 8:
                        hold = board[x][hor]
                        if piece.move(x, y, x, hor, 0) == "Success":
                            moves.append(key[y] + str(key2[x]) + " to " + key[hor] + str(key2[x]))
                            board[x][y] = piece
                            board[x][hor] = hold
                        else:
                            break
                        hor = hor + 1
                else:
                    global whiteKingPos
                    global blackKingPos
                    if player == "White":
                        index = whiteKingPos
                    else:
                        index = blackKingPos
                    holder = index[0]
                    holder2 = index[1]
                    flag_moved = piece.hasMoved
                    flag_checked = piece.hasBeenChecked
                    rookflag = None
                    if y - 2 >= 0:
                        hold = board[x][0]
                        if isinstance(hold, Rook):
                            rookflag = hold.hasMoved
                    if y - 2 >= 0 and piece.move(x, y, x, y - 2, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y - 2] + str(key2[x]))
                        board[x][y] = piece
                        board[x][0] = hold
                        board[x][1] = "              "
                        board[x][2] = "              "
                        board[x][3] = "              "
                        hold.hasMoved = rookflag
                        piece.hasMoved = flag_moved
                        piece.hasBeenChecked = flag_checked
                        index[0] = holder
                        index[1] = holder2
                    if y + 2 < 8:
                        hold = board[x][7]
                        if isinstance(hold, Rook):
                            rookflag = hold.hasMoved
                    if y + 2 < 8 and piece.move(x, y, x, y + 2, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y + 2] + str(key2[x]))
                        board[x][y] = piece
                        board[x][7] = hold
                        board[x][6] = "              "
                        board[x][5] = "              "
                        hold.hasMoved = rookflag
                        piece.hasMoved = flag_moved
                        piece.hasBeenChecked = flag_checked
                        index[0] = holder
                        index[1] = holder2
                    if y + 1 < 8 and x + 1 < 8:
                        hold = board[x+1][y+1]
                    if y + 1 < 8 and x + 1 < 8 and piece.move(x, y, x + 1, y + 1, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y + 1] + str(key2[x + 1]))
                        board[x][y] = piece
                        board[x+1][y+1] = hold
                        piece.hasMoved = flag_moved
                        piece.hasBeenChecked = flag_checked
                        index[0] = holder
                        index[1] = holder2
                    if y - 1 >= 0 and x - 1 >= 0:
                        hold = board[x-1][y-1]
                    if y - 1 >= 0 and x - 1 >= 0 and piece.move(x, y, x - 1, y - 1, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y - 1] + str(key2[x - 1]))
                        board[x][y] = piece
                        board[x-1][y-1] = hold
                        piece.hasMoved = flag_moved
                        piece.hasBeenChecked = flag_checked
                        index[0] = holder
                        index[1] = holder2
                    if y + 1 < 8 and x - 1 >= 0:
                        hold = board[x-1][y+1]
                    if y + 1 < 8 and x - 1 >= 0 and piece.move(x, y, x - 1, y + 1, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y + 1] + str(key2[x - 1]))
                        board[x][y] = piece
                        board[x-1][y+1] = hold
                        piece.hasMoved = flag_moved
                        piece.hasBeenChecked = flag_checked
                        index[0] = holder
                        index[1] = holder2
                    if y - 1 >= 0 and x + 1 < 8:
                        hold = board[x+1][y-1]
                    if y - 1 >= 0 and x + 1 < 8 and piece.move(x, y, x + 1, y - 1, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y - 1] + str(key2[x + 1]))
                        board[x][y] = piece
                        board[x+1][y-1] = hold
                        piece.hasMoved = flag_moved
                        piece.hasBeenChecked = flag_checked
                        index[0] = holder
                        index[1] = holder2
                    if y + 1 < 8:
                        hold = board[x][y+1]
                    if y + 1 < 8 and piece.move(x, y, x, y + 1, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y + 1] + str(key2[x]))
                        board[x][y] = piece
                        board[x][y+1] = hold
                        piece.hasMoved = flag_moved
                        piece.hasBeenChecked = flag_checked
                        index[0] = holder
                        index[1] = holder2
                    if y - 1 >= 0:
                        hold = board[x][y-1]
                    if y - 1 >= 0 and piece.move(x, y, x, y - 1, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y - 1] + str(key2[x]))
                        board[x][y] = piece
                        board[x][y-1] = hold
                        piece.hasMoved = flag_moved
                        piece.hasBeenChecked = flag_checked
                        index[0] = holder
                        index[1] = holder2
                    if x + 1 < 8:
                        hold = board[x+1][y]
                    if x + 1 < 8 and piece.move(x, y, x + 1, y, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y] + str(key2[x + 1]))
                        board[x][y] = piece
                        board[x+1][y] = hold
                        piece.hasMoved = flag_moved
                        piece.hasBeenChecked = flag_checked
                        index[0] = holder
                        index[1] = holder2
                    if x - 1 >= 0:
                        hold = board[x-1][y]
                    if x - 1 >= 0 and piece.move(x, y, x - 1, y, 0) == "Success":
                        moves.append(key[y] + str(key2[x]) + " to " + key[y] + str(key2[x - 1]))
                        board[x][y] = piece
                        board[x-1][y] = hold
                        piece.hasMoved = flag_moved
                        piece.hasBeenChecked = flag_checked
                        index[0] = holder
                        index[1] = holder2
                    if player == "White":
                        whiteKingPos = index
                    else:
                        blackKingPos = index
            y = y + 1
        x = x + 1
    #print(player)
    #print(str(whiteKingPos) + " " + str(blackKingPos))
    return moves

def eval():
    global turn_counter
    global board
    score = 0
    piece_value = {" Pawn " : 1, " Knight " : 3, " Bishop " : 3, " Rook " : 5, " Queen " : 9}
    legal_moves1 = len(generateMoves("Black"))
    score -= 0.05 * legal_moves1
    # Check the number of legal moves for white pieces
    legal_moves = len(generateMoves("White"))
    score += 0.05 * legal_moves 
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == "              ":
                continue
            if piece.owner == "White":  # White piece
                if isinstance(piece, King):  # White king
                # Evaluate castling rights
                    if row == 7 and (col == 2 or col == 6):
                        score += 0.3  # Favor castling rights
                    open_files = sum(1 for i in range(8) if board[i][col] == ' ') # Assess the number of open files around the king
                    score -= 0.05 * open_files  # Penalize for open files
                if isinstance(piece, Rook):  # White pawn
                    if all(board[i][col] == ' ' for i in range(8)):
                        score += 0.8  # Favor rooks on open files
                if col == 0 or col == 7 or row == 0 or row == 7:
                    score -= 0.1
                score += piece_value.get(piece.ezString(), 0)
                if isinstance(piece, Pawn):
                    if (col == 0 or not isinstance(board[row][col - 1], Pawn)) and (col == 7 or not isinstance(board[row][col + 1], Pawn)):
                        score -= 0.2  # Penalize isolated pawns
                    if all(board[i][col] == ' ' for i in range(8)): # Check for passed pawns
                        score += 0.4
                    if 3 <= col <= 4 and 3 <= row <= 4: # Favor pawns controlling central squares
                        score += 0.3
                else:  
                    if 3 <= col <= 4 and 3 <= row <= 4: # Favor central control by other pieces
                        score += 0.5
                if isinstance(piece, Queen) and turn_counter < 10 and (col != 3 and row != 7) :
                    score -= .5
                if isinstance(piece, Knight) and turn_counter < 10 and ((col != 1 and row != 7) or (col != 6 and row != 7)) :
                    score += .3
            else:  # Black piece
                if isinstance(piece, King):  # Black king
                    if row == 0 and (col == 2 or col == 6):
                        score -= 0.3  # Favor castling rights
                    open_files = sum(1 for i in range(8) if board[i][col] == ' ')
                    score += 0.05 * open_files  # Penalize for open files
                if isinstance(piece, Rook):  # Black pawn
                    if all(board[i][col] == ' ' for i in range(8)):
                        score -= 0.8  # Favor rooks on open files
                if col == 0 or col == 7 or row == 0 or row == 7:
                    score += 0.1
                score -= piece_value.get(piece.ezString(), 0)
                if isinstance(piece, Pawn):
                    if (col == 0 or not isinstance(board[row][col - 1], Pawn)) and (col == 7 or not isinstance(board[row][col + 1], Pawn)):
                        score += 0.2  # Penalize isolated pawns
                # Check for passed pawns
                    if all(board[i][col] == ' ' for i in range(8)):
                        score -= 0.4  # Favor passed pawns
                    if 3 <= col <= 4 and 3 <= row <= 4:
                        score -= 0.3
                else:
                    if 3 <= col <= 4 and 3 <= row <= 4:
                        score -= 0.5
                if isinstance(piece, Queen) and turn_counter < 10 and (col != 3 and row != 0) :
                    score += .5
                if isinstance(piece, Knight) and turn_counter < 10 and ((col != 1 and row != 0) or (col != 6 and row != 0)) :
                    score -= .3
    return score

def pick_move():
    global board
    max_eval = 1000
    local_max = -1000
    max_eval4 = None
    move_picked = ""
    first_b = ""
    second_b = ""
    third_b = ""
    global whiteKingPos
    global blackKingPos
    moves = generateMoves("White")
    took1 = None
    took2 = None
    took3 = None 
    took4 = None
    took5 = None
    took6 = None
    took7 = None
    took8 = None
    took9 = None
    global tookpiece
    holder = whiteKingPos[0]
    holder2 = whiteKingPos[1]
    for move1 in moves:
        error = move(move1, "White", 0)
        took1 = detTP()
        
        moves2 = generateMoves("Black")
        holder3 = blackKingPos[0]
        holder4 = blackKingPos[1]
        for move2 in moves2:
                error2 = move(move2, "Black", 0)
                took9 = detTP()
                e = eval()
                if e < max_eval:
                    max_eval = e
                    first_b = move2
                tookpiece = detTP2(took9)
                undo(move2)
                blackKingPos[0] = holder3
                blackKingPos[1] = holder4
        error3 = move(first_b, "Black", 0)
        took4 = detTP()
        holder5 = whiteKingPos[0]
        holder6 = whiteKingPos[1]
        moves3 = generateMoves("White")
        for move3 in moves3:
            error4 = move(move3, "White", 0)
            took2 = detTP()
            moves4 = generateMoves("Black")
            holder7 = blackKingPos[0]
            holder8 = blackKingPos[1]
            max_eval = 1000
            for move4 in moves4:
                error5 = move(move4, "Black", 0) # move the eval functions to reduce overhead outside of loop
                took7 = detTP()
                e = eval()
                if e < max_eval:
                    max_eval = e
                    second_b = move4
                tookpiece = detTP2(took7)
                undo(move4)
                blackKingPos[0] = holder7
                blackKingPos[1] = holder8
            error6 = move(second_b, "Black", 0)
            took5 = detTP()
            holder9 = whiteKingPos[0]
            holder10 = whiteKingPos[1]
            moves5 = generateMoves("White")
            for move5 in moves5:
                error7 = move(move5, "White", 0)
                took3 = detTP()
                moves6 = generateMoves("Black")
                holder11 = blackKingPos[0]
                holder12 = blackKingPos[1]
                max_eval = 1000
                for move6 in moves6:
                    error8 = move(move6, "Black", 0)
                    took8 = detTP()
                    e = eval()
                    if e < max_eval:
                        max_eval = e
                        third_b = move6
                    tookpiece = detTP2(took8)
                    undo(move6)
                    blackKingPos[0] = holder11
                    blackKingPos[1] = holder12
                error9 = move(third_b, "Black", 0)
                took6 = detTP()
                e = eval()
                if e > local_max:
                    local_max = e
                    move_picked = move1
                tookpiece = detTP2(took6)
                undo(third_b)
                whiteKingPos[0] = holder9
                whiteKingPos[1] = holder10
                tookpiece = detTP2(took3)
                undo(move5)
            tookpiece = detTP2(took5)
            undo(second_b)
            tookpiece = detTP2(took2)
            undo(move3)
            whiteKingPos[0] = holder5
            whiteKingPos[1] = holder6
        tookpiece = detTP2(took4)
        undo(first_b)
        tookpiece = detTP2(took1)
        undo(move1)

        whiteKingPos[0] = holder
        whiteKingPos[1] = holder2
    return move_picked

def detTP():
    global tookpiece
    if tookpiece == "              ":
        return "              "
    else:
        return copy.deepcopy(tookpiece)
    
def detTP2(e):
    if e == "              ":
        return "              "
    else:
        return copy.deepcopy(e)

def undo(play):
    global board
    global tookpiece
    key = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f':5, 'g': 6, 'h': 7}
    key2 = {1 : 7, 2 : 6, 3 : 5, 4 : 4, 5 : 3, 6 : 2, 7 : 1, 8 : 0}
    initialCol = play[0]
    if initialCol in key:
        initialCol = key[initialCol]
    else:
        return "invalid, out of play"
    initialRow = int(play[1])
    if initialRow in key2:
        initialRow = key2[initialRow]
    else:
        return "invalid, out of play"
    endCol = play[6]
    if endCol in key:
        endCol = key[endCol]
    else:
        return "invalid, out of play"
    endRow = int(play[7])
    if endRow in key2:
        endRow = key2[endRow]
    else: 
        return "invalid, out of play"
    if endCol == 2 and endRow == 0 and isinstance(board[endRow][endCol], King) and initialCol == 4:
            board[initialRow][initialCol] = board[endRow][endCol]
            board[initialRow][initialCol].hasMoved = False
            board[0][0] = board[0][3]
            board[0][0].hasMoved = False
            board[0][3] = "              "
            board[0][2] = "              "
    elif endCol == 6 and endRow == 0 and isinstance(board[endRow][endCol], King) and initialCol == 4:
            board[initialRow][initialCol] = board[endRow][endCol]
            board[initialRow][initialCol].hasMoved = False
            board[0][7] = board[0][5]
            board[0][7].hasMoved = False
            board[0][5] = "              "
            board[0][6] = "              "
    elif endCol == 6 and endRow == 7 and isinstance(board[endRow][endCol], King) and initialCol == 4:
            board[initialRow][initialCol] = board[endRow][endCol]
            board[initialRow][initialCol].hasMoved = False
            board[7][7] = board[7][5]
            board[7][7].hasMoved = False
            board[7][5] = "              "
            board[7][6] = "              "
    elif endCol == 2 and endRow == 7 and isinstance(board[endRow][endCol], King) and initialCol == 4:
            board[initialRow][initialCol] = board[endRow][endCol]
            board[initialRow][initialCol].hasMoved = False
            board[7][0] = board[7][3]
            board[7][0].hasMoved = False
            board[7][3] = "              "
            board[7][2] = "              "
    else:
        if isinstance(board[endRow][endCol], Pawn) and (initialRow == 6 or initialRow == 1):
            board[endRow][endCol].hasMoved = False
        
        #print("putting " + str(board[endRow][endCol]) + " back at " + str(initialRow) + " " + str(initialCol) + " from " + str(endRow) + " " + str(endCol) + "")
        #print("tookpiece is " + str(tookpiece))
        #if board[endRow][endCol] == "              ":
            #printBoard("")
            #quit()
        board[initialRow][initialCol] = board[endRow][endCol]
        board[endRow][endCol] = copy.deepcopy(tookpiece)


def move(play, player, flag):
    global lastMove
    key = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f':5, 'g': 6, 'h': 7}
    key2 = {1 : 7, 2 : 6, 3 : 5, 4 : 4, 5 : 3, 6 : 2, 7 : 1, 8 : 0}
    initialCol = play[0]
    if initialCol in key:
        initialCol = key[initialCol]
    else:
        return "invalid, out of play"
    initialRow = int(play[1])
    if initialRow in key2:
        initialRow = key2[initialRow]
    else:
        return "invalid, out of play"
    endCol = play[6]
    if endCol in key:
        endCol = key[endCol]
    else:
        return "invalid, out of play"
    endRow = int(play[7])
    if endRow in key2:
        endRow = key2[endRow]
    else: 
        return "invalid, out of play"
    global board
    piece = board[initialRow][initialCol]
    lastMove = "" + player + " moves their" + piece.ezString() + "from " + play + ""
    if piece == "              ":
        return "no piece there"
    if piece.owner == player:
        error = piece.move(initialRow, initialCol, endRow, endCol, flag)
        return error
    else:
        return "not your piece dummy"

def isCheckmate(player):
    if isCheck(player, 1):
        if len(generateMoves(player)) == 0:
            return True
    return False

def printBoard(e):
    global lastMove
    if e == "Success":
        e = lastMove
    s = eval()
    m = 8
    print("          A                 B                C                D                E                F                G                 H       ")
    for y in board:
        
        print("  -----------------------------------------------------------------------------------------------------------------------------------------")
        print("  |                |                |                |                |                |                |                |                |")
        print("  |                |                |                |                |                |                |                |                |")
        print(m, end=" ")
        for x in y:
            print("| ", end="")
            print(x, end=" ")
        print("|", end = " ")
        if m == 5:
            print(e + " " + f"{s:.2f}")
        else:
            print("")
        print("  |                |                |                |                |                |                |                |                |")
        print("  |                |                |                |                |                |                |                |                |")
        m = m - 1
    print("  -----------------------------------------------------------------------------------------------------------------------------------------")
    print("          A                 B                C                D                E                F                G                 H       ")

def createBoard():
    rook1 = Rook("Black")
    rook2 = Rook("Black")
    knight1 = Knight("Black")
    knight2 = Knight("Black")
    bishop1 = Bishop("Black")
    bishop2 = Bishop("Black")
    queen1 = Queen("Black")
    king1 = King("Black")
    pawn1 = Pawn("Black")
    pawn2 = Pawn("Black")
    pawn3 = Pawn("Black")
    pawn4 = Pawn("Black")
    pawn5 = Pawn("Black")
    pawn6 = Pawn("Black")
    pawn7 = Pawn("Black")
    pawn8 = Pawn("Black")
    rook3 = Rook("White")
    rook4 = Rook("White")
    knight3 = Knight("White")
    knight4 = Knight("White")
    bishop3 = Bishop("White")
    bishop4 = Bishop("White")
    queen2 = Queen("White")
    king2 = King("White")
    pawn9 = Pawn("White")
    pawn10 = Pawn("White")
    pawn11 = Pawn("White")
    pawn12 = Pawn("White")
    pawn13 = Pawn("White")
    pawn14 = Pawn("White")
    pawn15 = Pawn("White")
    pawn16 = Pawn("White")
    global board
    board = [[rook1, knight1, bishop1, queen1, king1, bishop2, knight2, rook2], [pawn1, pawn2, pawn3, pawn4, pawn5, pawn6, pawn7, pawn8], ["              ", "              ", "              ", "              ", "              ", "              ", "              ", "              "], ["              ", "              ", "              ", "              ", "              ", "              ", "              ", "              "],
             ["              ", "              ", "              ", "              ", "              ", "              ", "              ", "              "], ["              ", "              ", "              ", "              ", "              ", "              ", "              ", "              "], [pawn9, pawn10, pawn11, pawn12, pawn13, pawn14, pawn15, pawn16], [rook3, knight3, bishop3, queen2, king2, bishop4, knight4, rook4]]

def play():
    global turn_counter
    print("White player starts first.")
    turn2move = ["White", "Black"]
    counter = 0
    while (1):
        turn = turn2move[counter % 2]
        if isCheckmate(turn):
           print("" + turn2move[(counter + 1) % 2] + " wins by checkmate.")
           break
        if turn == "White":
            mOve = pick_move()
        else:
            mOve = input(turn + " enter move: ")
        if mOve == "quit":
            print("" + turn2move[(counter + 1) % 2] + " wins by concession.")
            quit()
        e = move(mOve, turn, 1)
        if e != "Success":
            print("invalid move reason: " + e)
        else:
            counter += 1
            turn_counter += 1
        printBoard(e)


def main():
    createBoard()
    e = ""
    printBoard(e)
    play()

if __name__ == "__main__":
    main()

# use pysimplegui to make GUI
# use divider methods to make rows
# create buttons with piece pictures as their image
# on button press, select that piece. Then select the square to move to. The first button press gives you the "A4", second the part after the "to"
# after two buttons are pressed, process the move. Then, using the new board state, create a new GUI layout and refresh the GUI.
