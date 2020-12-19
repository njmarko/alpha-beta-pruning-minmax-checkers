def input_choose_piece(position, available_pieces=None):
    while True:
        if available_pieces:
            print(
                "Forced captures are enabled! You can only choose the highlighted figures.")
        coord = input(
            "Enter the figure coordinates(row+column without space ex. 70 for down left)<x to exit>:")
        try:
            if coord.lower() == "x":
                return None
            coordinate = (int(coord) // 10), (int(coord) % 10)
            field = position.get_table()[coordinate[0]][coordinate[1]]
            if available_pieces:
                if coordinate in available_pieces:
                    if position.get_white_to_move() and field.lower() == "b":
                        next_moves = position.find_valid_moves_for_piece(
                            coordinate)
                        if len(next_moves) != 0:
                            return coordinate
                        else:
                            print("Chosen figure has no available moves!")
                            continue
                    elif not position.get_white_to_move() and field.lower() == "c":
                        return coordinate
                    else:
                        print("Selection is not valid! Try again.")
            else:
                if position.get_white_to_move() and field.lower() == "b":
                    next_moves = position.find_valid_moves_for_piece(
                        coordinate)
                    if len(next_moves) != 0:
                        return coordinate
                    else:
                        print("Chosen figure has no available moves!")
                        continue
                elif not position.get_white_to_move() and field.lower() == "c":
                    return coordinate
                else:
                    print("Selection is not valid! Try again.")
        except:
            print("Invalid coordinate! Try again.")


def input_choose_field(valid_moves):
    while True:
        coord = input(
            "Enter the field coordinates(row+column without space ex. 70 for down left)<x to exit>:")
        try:
            if coord.lower() == "x":
                return None
            coordinate = (int(coord) // 10), (int(coord) % 10)
            if coordinate not in valid_moves:
                print("Selection is not valid! Try again.")
            else:
                return coordinate
        except:
            print("Invalid coordinate! Try again.")


def input_forced_moves():
    while True:
        forced = input(
            "Do you want to enable forced captures? <yes|no>:")
        try:
            if forced.lower() == "yes":
                return True
            if forced.lower() == "no":
                return False
            print("Invalid choice! Try again.")

        except:
            print("Invalid input! Try again!")
