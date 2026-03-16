import math


def winner(board):
    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    for a, b, c in lines:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return all(c != " " for c in board)


def minimax(board, is_max):
    w = winner(board)
    if w == "X":
        return 1
    if w == "O":
        return -1
    if is_full(board):
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                best = max(best, minimax(board, False))
                board[i] = " "
        return best

    best = math.inf
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            best = min(best, minimax(board, True))
            board[i] = " "
    return best


def best_move(board):
    best_score, move = -math.inf, -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score, move = score, i
    return move


def main():
    board = ["X", "O", "X", " ", "O", " ", " ", " ", " "]
    print("\nSeason 4 / Ep 02 - Minimax Tic-Tac-Toe")
    print("Best move for X:", best_move(board))


if __name__ == "__main__":
    main()
