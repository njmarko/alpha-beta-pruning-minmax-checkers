from input import *
from output import print_table
from position import Position
from math import inf
from time import time
from copy import deepcopy

# MIN MAX simple implementation


def min_max(position, depth, max_player):
    if depth == 0 or position.get_game_end():
        return position.evaluate_state()
    if max_player:
        max_evaluation = -inf
        for child in position.get_next_moves():
            eval = min_max(child, depth - 1, False)
            max_evaluation = max(max_evaluation, eval)
        position.set_evaluation(max_evaluation)
        return max_evaluation
    else:
        min_evaluation = inf
        for child in position.get_next_moves():
            eval = min_max(child, depth - 1, True)
            min_evaluation = min(min_evaluation, eval)
        position.set_evaluation(min_evaluation)
        return min_evaluation

# MIN MAX with ALPHA-BETA pruning


def alpha_beta(position, depth, alpha, beta, max_player, forced_caputure):
    if depth == 0 or position.get_game_end():
        return position.evaluate_state()
    if max_player:
        max_evaluation = -inf
        for child in position.get_next_moves(forced_caputure):
            eval = alpha_beta(child, depth - 1, alpha,
                              beta, False, forced_caputure)
            max_evaluation = max(max_evaluation, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                # print("pruning max")
                break
        position.set_evaluation(max_evaluation)
        return max_evaluation
    else:
        min_evaluation = inf
        for child in position.get_next_moves(forced_caputure):
            eval = alpha_beta(child, depth - 1, alpha,
                              beta, True, forced_caputure)
            min_evaluation = min(min_evaluation, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                # print("pruning min")
                break
        position.set_evaluation(min_evaluation)
        return min_evaluation

# Alpha beta pruning minmax that calls a different function. It can be changed to take the function as a parameter


def alpha_beta_ending(position, depth, alpha, beta, max_player, forced_caputure):
    if depth == 0 or position.get_game_end():
        return position.evaluate_state_ending()
    if max_player:
        max_evaluation = -inf
        for child in position.get_next_moves(forced_caputure):
            eval = alpha_beta_ending(
                child, depth - 1, alpha, beta, False, forced_caputure)
            max_evaluation = max(max_evaluation, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                # print("pruning max")
                break
        position.set_evaluation(max_evaluation)
        return max_evaluation
    else:
        min_evaluation = inf
        for child in position.get_next_moves(forced_caputure):
            eval = alpha_beta_ending(
                child, depth - 1, alpha, beta, True, forced_caputure)
            min_evaluation = min(min_evaluation, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                # print("pruning min")
                break
        position.set_evaluation(min_evaluation)
        return min_evaluation


def determine_dynamic_depth(time_previous_move, depth, forced_caputure, num_moves):
    if forced_caputure:
        if time_previous_move < 0.5 and num_moves <= 6:
            return depth + 1
        if depth > 6 and (time_previous_move > 4 or num_moves > 6):
            return depth - 1
        return depth
    else:
        if time_previous_move < 0.5:
            return depth + 1
        if time_previous_move > 4.5:
            return depth - 1
        return depth


def ending_conditions(position, figure_counter, forced_caputure):
    moves = position.get_next_moves(forced_caputure)

    num_figures = position.count_pieces()
    if num_figures[0] == 0:
        print("Black won!")
        return True
    if num_figures[1] == 0:
        print("White won!")
        return True
    if num_figures[0] + num_figures[1] == figure_counter[0]:
        figure_counter[1] += 1
        if figure_counter[1] == 50:
            print("Tie!")
            return True
    else:
        figure_counter[0] = num_figures[0] + num_figures[1]
        figure_counter[1] = 0
    if not moves:
        print("There are no possible moves left! Game is finished!")
        return True
    return False


def main():
    # table = [['B', '.', 'B', '.', 'B', '.', '.', '.'],
    #          ['.', '.', '.', '.', '.', '.', '.', '.'],
    #          ['.', '.', '.', '.', '.', '.', 'B', '.'],
    #          ['.', '.', '.', '.', '.', 'B', '.', '.'],
    #          ['c', '.', '.', '.', '.', '.', '.', '.'],
    #          ['.', '.', '.', 'C', '.', '.', '.', '.'],
    #          ['.', '.', 'c', '.', '.', '.', 'c', '.'],
    #          ['.', '.', '.', '.', '.', '.', '.', '.']]

    table = [['.', 'c', '.', 'c', '.', 'c', '.', 'c'],
             ['c', '.', 'c', '.', 'c', '.', 'c', '.'],
             ['.', 'c', '.', 'c', '.', 'c', '.', 'c'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
             ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
             ['b', '.', 'b', '.', 'b', '.', 'b', '.']]
    forced_caputure = input_forced_moves()

    position = Position(table, True)
    time_previous_move = 4.5
    depth = 6
    # broj figura, i counter koliko poteza je proslo bez jedenja
    without_capture = [0, 0]

    while True:
        if ending_conditions(position, without_capture, forced_caputure):
            break

        print("New depth is {} ".format(depth))
        available_pieces = position.find_capturing_moves()
        if forced_caputure:
            print_table(position.get_table(), available_pieces)
            piece = input_choose_piece(position, available_pieces)
        else:
            print_table(position.get_table())
            piece = input_choose_piece(position)

        if not piece:
            print("Goodbye!")
            break
        valid_moves = position.find_valid_moves_for_piece(
            piece, forced_caputure)
        print_table(position.get_table(), piece, valid_moves)
        new_position = input_choose_field(valid_moves)
        if not new_position:
            print("Taknuto maknuto! Doviđenja!")
            break
        previous_table = deepcopy(position.get_table())
        position = position.play_move(piece, new_position)
        differences = position.find_move_played(previous_table)
        print_table(position.get_table(), differences)
        print("User played the move displayed on the table above.\n\n\n")
        if ending_conditions(position, without_capture, forced_caputure):
            break
        num_moves = len(position.get_next_moves())
        depth = determine_dynamic_depth(
            time_previous_move, depth, forced_caputure, num_moves)
        previous_table = deepcopy(position.get_table())
        print("THINKING.....................................")
        t1 = time()
        num_figures = position.count_pieces()
        if num_figures[0] + num_figures[1] > 6:
            alpha_beta(position, depth, -inf, inf, True, forced_caputure)
            # for child in position.get_next_moves():
            #     print_table(child.get_table())
            #     print(str(child.get_evaluation()) + " Tabla iznad")
            position = max(position.get_next_moves())
        else:
            alpha_beta_ending(position, 20, -inf, inf, True, forced_caputure)
            # for child in position.get_next_moves():
            #     print_table(child.get_table())
            #     print(str(child.get_evaluation()) + " Tabla iznad")
            position = max(position.get_next_moves())
        t2 = time()
        time_previous_move = t2 - t1
        differences = position.find_move_played(previous_table)
        print(time_previous_move)
        # print("Dubina je {} ".format(depth))
        print_table(position.get_table(), differences)
        print("Computer played a move displayed on the table above.\n\n")


if __name__ == '__main__':
    main()
