global error
error = ""
class Pawn:
    def __init__(self, owner, curRow, curCol, hasMoved):
        self.owner = owner
        self.row = curRow
        self.col = curCol
        self.hasMoved = hasMoved
    def __str__(self):
        return "P"
    def promote(self, board):
        if self.owner == "White" and self.row == 7 or self.owner == "Black" and self.row == 0:
            board[self.curRow][self.curCol] = Queen(self.owner, self.curRow, self.curCol)
            return board
    def move(self, newrow, newcol, owner, board):

class Rook:
    def __init__(self, owner, curRow, curCol, hasMoved):
        self.owner = owner
        self.row = curRow
        self.col = curCol
        self.hasMoved = hasMoved
    def __str__(self):
        return "R"
    def move(self, newrow, newcol, owner, board):
        global error
        if self.curRow == newrow:
            if self.curCol < newcol:
                for i in range(self.curCol + 1, newcol):
                    if board[self.curRow][i] != " ":
                        error = "There is a piece in the way"
                        return board
            elif self.curCol > newcol:
                for i in range(self.curCol - 1, newcol, -1):
                    if board[self.curRow][i] != None:
                        error = "There is a piece in the way"
                        return board
        elif self.curCol == newcol:
            if self.curCol < newcol:
                for i in range(self.curRow + 1, newrow):
                    if board[i][self.curCol] != None:
                        error = "There is a piece in the way"
                        return board
            elif self.curCol > newcol:
                for i in range(self.curRow - 1, newrow, -1):
                    if board[i][self.curCol] != None:
                        error = "There is a piece in the way"
                        return board
        else:
            error = "Invalid move"
            return board
        if board[newrow][newcol] != " " and board[newrow][newcol].owner != owner:
            error = "You cannot capture your own piece"
            return board
        else:
            c = check(board, owner, newrow, newcol, self)
            if c == None:
                error = "would put you in check or does not deal with current check"
                return board
            else:
                self.hasMoved = True
                return c
            
class Bishop:
    def __init__(self, curRow, curCol, owner):
        self.curRow = curRow
        self.curCol = curCol
        self.owner = owner
    def __str__(self):
        return "B"
    def move(self, newrow, newcol, owner, board):
        global error
        if abs(self.curRow - newrow) == abs(self.curCol - newcol):
            if self.curRow < newrow and self.curCol < newcol:
                for i in range(1, abs(self.curRow - newrow)):
                    if board[self.curRow + i][self.curCol + i] != None:
                        error = "There is a piece in the way"
                        return board
            elif self.curRow < newrow and self.curCol > newcol:
                for i in range(1, abs(self.curRow - newrow)):
                    if board[self.curRow + i][self.curCol - i] != None:
                        error = "There is a piece in the way"
                        return board
            elif self.curRow > newrow and self.curCol < newcol:
                for i in range(1, abs(self.curRow - newrow)):
                    if board[self.curRow - i][self.curCol + i] != None:
                        error = "There is a piece in the way"
                        return board
            elif self.curRow > newrow and self.curCol > newcol:
                for i in range(1, abs(self.curRow - newrow)):
                    if board[self.curRow - i][self.curCol - i] != None:
                        error = "There is a piece in the way"
                        return board
        else:
            error = "Invalid move"
            return board
        if board[newrow][newcol] != " " and board[newrow][newcol].owner != owner:
            error = "You cannot capture your own piece"
            return board
        else:
            c = check(board, owner, newrow, newcol, self)
            if c == None:
                error = "would put you in check or does not deal with current check"
                return board
            else:
                return c
            
class Knight:
    def __init__(self, curRow, curCol, owner):
        self.curRow = curRow
        self.curCol = curCol
        self.owner = owner
    def __str__(self):
        return "N"
    def move(self, newrow, newcol, owner, board):
        global error
        if (abs(self.curRow - newrow) == 2 and abs(self.curCol - newcol) == 1) or (abs(self.curRow - newrow) == 1 and abs(self.curCol - newcol) == 2):
            if board[newrow][newcol] != " " and board[newrow][newcol].owner != owner:
                error = "You cannot capture your own piece"
                return board
            else:
                c = check(board, owner, newrow, newcol, self)
                if c == None:
                    error = "would put you in check or does not deal with current check"
                    return board
                else:
                    return c
        else:
            error = "Invalid move"
            return board
            
class Queen:
    def __init__(self, curRow, curCol, owner):
        self.curRow = curRow
        self.curCol = curCol
        self.owner = owner
    def __str__(self):
        return "Q"
    def move(self, newrow, newcol, owner, board):
        global error
        if abs(self.curRow - newrow) == abs(self.curCol - newcol):
            if self.curRow < newrow and self.curCol < newcol:
                for i in range(1, abs(self.curRow - newrow)):
                    if board[self.curRow + i][self.curCol + i] != None:
                        error = "There is a piece in the way"
                        return board
            elif self.curRow < newrow and self.curCol > newcol:
                for i in range(1, abs(self.curRow - newrow)):
                    if board[self.curRow + i][self.curCol - i] != None:
                        error = "There is a piece in the way"
                        return board
            elif self.curRow > newrow and self.curCol < newcol:
                for i in range(1, abs(self.curRow - newrow)):
                    if board[self.curRow - i][self.curCol + i] != None:
                        error = "There is a piece in the way"
                        return board
            elif self.curRow > newrow and self.curCol > newcol:
                for i in range(1, abs(self.curRow - newrow)):
                    if board[self.curRow - i][self.curCol - i] != None:
                        error = "There is a piece in the way"
                        return board
            elif self.curRow == newrow:
                if self.curCol < newcol:
                    for i in range(self.curCol + 1, newcol):
                        if board[self.curRow][i] != None:
                            error = "There is a piece in the way"
                            return board
                elif self.curCol > newcol:
                    for i in range(self.curCol - 1, newcol, -1):
                        if board[self.curRow][i] != None:
                            error = "There is a piece in the way"
                            return board
            elif self.curCol == newcol:
                if self.curCol < newcol:
                    for i in range(self.curRow + 1, newrow):
                        if board[i][self.curCol] != None:
                            error = "There is a piece in the way"
                            return board
                elif self.curCol > newcol:
                    for i in range(self.curRow - 1, newrow, -1):
                        if board[i][self.curCol] != None:
                            error = "There is a piece in the way"
                            return board
            else:
                error = "Invalid move"
                return board
            if board[newrow][newcol] != " " and board[newrow][newcol].owner != owner:
                error = "You cannot capture your own piece"
                return board
            else:
                c = check(board, owner, newrow, newcol, self)
                if c == None:
                    error = "would put you in check or does not deal with current check"
                    return board
                else:
                    return c

class King:
    def __init__(self, curRow, curCol, owner, hasMoved, hasBeenChecked):
        self.curRow = curRow
        self.curCol = curCol
        self.owner = owner
        self.hasMoved = hasMoved
        self.hasBeenChecked = hasBeenChecked
    def __str__(self):
        return "K"
    def castle(self, newrow, newcol, owner, board):
        global error
        if self.hasMoved == False and self.hasBeenChecked == False:
            if self.curRow == newrow:
                if self.curCol < newcol:
                    if board[self.curRow][self.curCol + 1] == " " and board[self.curRow][self.curCol + 2] == " " and board[self.curRow][self.curCol + 3] != None and board[self.curRow][self.curCol + 3].hasMoved == False:
                        for i in range(self.curCol + 1, newcol):
                            if board[self.curRow][i] != None:
                                error = "There is a piece in the way"
                                return board
                        c = check(board, owner, newrow, newcol, self)
                        if c == None:
                            error = "would put you in check or does not deal with current check"
                            return board
                        else:
                            board[self.curRow][self.curCol + 3].move(self.curRow, self.curCol + 1, owner, board)
                            return c
                    else:
                        error = "Invalid move"
                        return board
                elif self.curCol > newcol:
                    if board[self.curRow][self.curCol - 1] == " " and board[self.curRow][self.curCol - 2] == " " and board[self.curRow][self.curCol - 3] == " " and board[self.curRow][self.curCol - 4] != None and board[self.curRow][self.curCol - 4].hasMoved == False:
                        for i in range(self.curCol - 1, newcol, -1):
                            if board[self.curRow][i] != None:
                                error = "There is a piece in the way"
                                return board
                        c = check(board, owner, newrow, newcol, self)
                        if c == None:
                            error = "would put you in check or does not deal with current check"
                            return board
                        else:
                            board[self.curRow][self.curCol - 4].move(self.curRow, self.curCol - 1, owner, board)
                            return c
            else:
                error = "Invalid move"
                return board
        else:
            error = "Invalid move"
            return board
    def move(self, newrow, newcol, owner, board):
        global error
        if abs(self.curRow - newrow) <= 1 and abs(self.curCol - newcol) <= 1:
            if board[newrow][newcol] != " " and board[newrow][newcol].owner != owner:
                error = "You cannot capture your own piece"
                return board
            else:
                c = check(board, owner, newrow, newcol, self)
                if c == None:
                    error = "would put you in check or does not deal with current check"
                    return board
                else:
                    self.hasMoved = True
                    return c
        else:
            error = "Invalid move"
            return board


