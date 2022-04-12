import argparse
import socket
import random
import string


def main(host, port):
    server_addr = (host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # The board is a 10x10 matrix of integers
    # 0 means water
    # 1 means a ship section
    board = "0 0 0 1 0 0 0 0 0 0; 0 0 0 1 0 0 0 0 0 1; 0 0 0 0 0 1 0 0 0 1; 0 1 0 1 0 1 0 1 0 1; 0 1 0 0 0 0 0 0 0 1; " \
            "0 1 0 0 0 0 0 0 0 0; 0 0 0 0 1 1 1 0 0 0; 0 0 0 0 0 0 0 0 0 0; 0 1 0 0 1 1 0 0 0 1; 0 0 0 0 0 0 0 0 0 0"

    # We are going to generate an array with all the possible movements (A1, A2, A3, A4 ..., A10, B1, B2 ..., B10 ...,
    # J10)
    # The letter represents the columns, the number the row of the (10x10) board
    movements = []
    # Uppercase letters from 'A' to 'J'
    letters = string.ascii_uppercase[:10]
    for letter in letters:
        # Numbers from 1 to 10
        for number in range(1,11):
            # We concatenate the letter with the number to generate the movement code
            movements.append(letter+str(number))

    # We shuffle the movements array for a random game strategy in each execution
    random.shuffle(movements)

    # We send our player name to the server
    s.sendto("Korvo".encode("utf-8"), server_addr)
    # We send our board to the server
    s.sendto(board.encode("utf-8"), server_addr)

    again = False
    next_turn = -1
    # Game loop
    finished = False
    while not finished:
        # We wait for Server instruction
        buffer, addr = s.recvfrom(512)
        message = buffer.decode("utf-8")
        # It is our turn
        if "Turn" in message:
            # We get the turn ID
            aux = message.split()
            turn = int(aux[1])
            # We check if the turn ID is correct
            if next_turn != -1 and again:
                if next_turn != turn:
                    raise AssertionError("Turn ID " + str(turn) + " is incorrect, it should have been " + str(next_turn))
            # We send our movement
            movement = movements.pop()
            print("It is my turn (Turn " + str(turn) + "). My movement it is " + movement + ".")
            s.sendto(movement.encode("utf-8"), server_addr)
            # We wait for the server response with the effect of our movement
            buffer, addr = s.recvfrom(512)
            message = buffer.decode("utf-8")
            if message == "You win":
                print("Yesss! I won. I am the best.")
                finished = True
            elif message == "Hit":
                print("I got it right. It will be my turn again.")
                next_turn = turn + 1
                again = True
            elif message == "Fail":
                print("I failed.")
                again = False
            else:
                raise AssertionError("Received message '" + message + "' unknown or out of flow")
        elif message == "You lost":
            print("Damn it! I lost. Let's go again!")
            finished = True
        else:
            raise AssertionError("Received message '" + message + "' unknown or out of flow")

    s.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="remote port")
    parser.add_argument('--host', default='localhost', help="remote host")
    args = parser.parse_args()

    main(args.host, args.port)
