# Implementation of Monte Carlo method to approximate pi value
import argparse
import math
import random


def f(x):
    return math.sqrt(1 - math.pow(x, 2))


def main(n):
    below_counter = 0
    for i in range(0, n):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)

        if y < f(x):
            below_counter = below_counter + 1

    pi = 4.0 * float(below_counter) / float(n)
    print("The approximate value of pi with " + str(n) + " random points is " + str(pi))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--number', default=100000, help="number of random points to be generated")
    args = parser.parse_args()

    main(args.number)
