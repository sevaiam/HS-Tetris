# Write your code here
import copy


def clean_board(dim):
    return [['-'] * dim[0] for _ in range(dim[1])]


def print_board(board):
    for it in range(len(board)):
        print(*(x for x in board[it]), sep=' ')
    print()


def check_borders(board, piece_pos, piece_corr):
    width = len(board[0])
    height = len(board)
    for r, c in piece_pos:
        next_c = c + piece_corr
        if r + 1 >= height:  # hit the floor
            return False
        if not 0 <= next_c < width:  # hit walls
            return False
        if board[r + 1][next_c] == 0:  # hit other piece
            return False
    return True


def abs_position(piece):
    abs_coords = []
    for i in piece:
        abs_coords.append([i // 10, i % 10])
    return abs_coords


def play_piece(f_board, piece, moves):
    # p_dic = {'O': (4, 14, 15, 5),
    #          'I': (4, 14, 24, 34),
    #          'S': (5, 4, 14, 13),
    #          'Z': (4, 5, 15, 16),
    #          'L': (4, 14, 24, 25),
    #          'J': (5, 15, 25, 24),
    #          'T': (4, 14, 24, 15)}

    p_dic = {'O': [[4, 14, 15, 5]],
             'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
             'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
             'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
             'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
             'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
             'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]}
    rot_dic = {'O': ((0, 0), (0, 0), (0, 0), (0, 0)),
               'I': (((0, 1), (1, 0), (2, -1), (3, -2)), ((0, -1), (-1, 0), (-2, 1), (-3, 2))),
               'S': (((0, 1), (-1, 0), (0, -1), (-1, -2)), ((0, -1), (1, 0), (0, 1), (1, 2))),
               'Z': (((0, -1), (-1, 0), (0, 1), (-1, 2)), ((0, 1), (1, 0), (0, -1), (1, -2))),
               'L': (((0, 0), (0, 0), (0, 0), (0, 0)), ((0, 1), (0, 1), (-1, 0), (-1, -2)),
                     ((0, 0), (0, 0), (0, 0), (0, 0)), ((0, 0), (0, 0), (0, 0), (0, 0))),
               'J': (((0, 0), (0, 0), (0, 0), (0, 0)), ((0, 0), (0, 0), (0, 0), (0, 0)),
                     ((0, 0), (0, 0), (0, 0), (0, 0)), ((0, 0), (0, 0), (0, 0), (0, 0))),
               'T': (((0, 0), (0, 0), (0, 0), (0, 0)), ((0, 0), (0, 0), (0, 0), (0, 0)),
                     ((0, 0), (0, 0), (0, 0), (0, 0)), ((0, 0), (0, 0), (0, 0), (0, 0)))}

    # new_board = copy.deepcopy(f_board)
    work_piece = p_dic[piece]

    rotation = 0
    piece_correction = 0

    piece_position = abs_position(work_piece[0])


    for no in range(len(moves)):
        curr_move = moves[no]
        if curr_move == 'left':
            if check_borders(f_board, piece_position, -1):
                piece_correction += -1
                piece_position = [[x + 1, y - 1] for x, y in piece_position]
            elif check_borders(f_board, piece_position, 0):
                piece_position = [[x + 1, y] for x, y in piece_position]
            pass
        elif curr_move == 'right':
            if check_borders(f_board, piece_position, 1):
                piece_correction += 1
                piece_position = [[x + 1, y + 1] for x, y in piece_position]
            elif check_borders(f_board, piece_position, 0):
                piece_position = [[x + 1, y] for x, y in piece_position]
            pass
        elif curr_move == 'rotate':
            # find out the rotation correction
            cur_rotate = work_piece[rotation % len(work_piece)]
            next_rotate = work_piece[(rotation + 1) % len(work_piece)]
            abs_rotate = []
            for o, n in zip(cur_rotate, next_rotate):
                abs_rotate.append([(n // 10) - (o // 10), (n % 10) - (o % 10)])

            rotated_piece = []
            for a, b in zip(piece_position, abs_rotate):
                rotated_piece.append([a[0] + b[0], a[1] + b[1]])
            # for r, c in abs_position(p_dic[piece][(rotation + 1) % len(p_dic[piece])]):
            #     row = r + len(moves)
            #     column = c + piece_correction
            #     rotated_piece.append([row, column])
            if check_borders(f_board, rotated_piece, 0):
                rotation += 1
                piece_position = [[x + 1, y] for x, y in rotated_piece]
            elif check_borders(f_board, piece_position, 0):
                piece_position = [[x + 1, y] for x, y in piece_position]
            pass
        elif curr_move == 'down':
            if check_borders(f_board, piece_position, 0):
                piece_position = [[x + 1, y] for x, y in piece_position]
            else:
                for r, c in piece_position:
                    f_board[r][c] = 0
                global piece_in_game
                piece_in_game = False
            pass

    new_board = copy.deepcopy(f_board)
    for r, c in piece_position:
        new_board[r][c] = 0

    return new_board


def break_lines(board):
    for line in range(len(board)):
        if '-' not in board[line]:
            del board[line]
            board.insert(0, ['-'] * len(board[0]))


board_dim = [int(x) for x in input().split()]
play_board = clean_board(board_dim)
print_board(play_board)
moves_que = []
piece_in_game = False
current_piece = None

next_move = input()

while next_move != 'exit':
    if next_move == 'piece':
        if piece_in_game:
            print('Another piece is in game. Pick a move.')
        else:
            current_piece = input()
            moves_que.clear()
            piece_in_game = True
            print_board(play_piece(play_board, current_piece, moves_que))
    elif next_move == 'break':
        break_lines(play_board)
        print_board(play_board)
    elif next_move in ['rotate', 'left', 'right', 'down']:
        if piece_in_game:
            moves_que.append(next_move)
            print_board(play_piece(play_board, current_piece, moves_que))
        else:
            print('No piece in game. Use "piece" to enter new piece')
    else:
        print('Invalid move!')
    if not piece_in_game and 0 in play_board[0]:
        print('Game Over!')
        break
    next_move = input()
