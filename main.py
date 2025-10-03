import random
import time
import pseudoprimes
from functools import reduce
from math import sqrt
import sys

BASE_POWER = 50
BASE_LAST_NUMBER = int(2 ** BASE_POWER + 1)
INDEX_CAP = 100


def generate_true_prime():
    last_number = BASE_LAST_NUMBER
    loop_limit = random.randint(0, INDEX_CAP)

    for index in range(0, loop_limit):
        last_number = pseudoprimes.next_prime(last_number)
        sys.stdout.write("\rProcessing prime no. " + str(index) + " / " + str(loop_limit - 1))

    sys.stdout.write("\r \n")
    return last_number


def generate_mislead():
    mislead = random.getrandbits(BASE_POWER)
    if not mislead % 2:
        mislead += 1
    count = 1
    while pseudoprimes.is_prime(mislead):
        mislead += 2
        count += 1

        if not count % 100:
            print("Processing mislead no. " + str(count))

        if prime_check_5(mislead):
            continue

    return mislead


def prime_check_5(number):
    if [0, 5].__contains__(int(repr(number)[-1])):
        return True

    return False


def main():
    random.seed(time.time())

    print("Generating mislead...")
    mislead = generate_mislead()
    print("Processesing mislead factors (This takes the most time!)...")
    list_of_factors = factors(mislead)
    print("Generating true prime...")
    true_prime = generate_true_prime()

    if random.randint(0, 1):
        evaluate = true_prime
        list_of_factors = [1, true_prime]
    else:
        print()
        evaluate = mislead

    print("n chosen for combo is:")
    print(evaluate)
    answer = prompt_user(evaluate)

    print("List of factors: " + str(list_of_factors))
    print("Did it factor? \t" + str(answer in list_of_factors))
    print("Psuedoprime? \t" + str(evaluate == mislead))


def prompt_user(evaluate):
    # input cannot be 0, 1, <1, or n
    # if they choose 2 warn them this is a bad idea
    answer = 0

    while True:
        response = input("Enter the defending player's chosen factor.\n")

        try:
            response = int(response)
        except ValueError:
            print("Invalid formatting. Please input a number.")
            continue

        if response in [0, 1, evaluate]:
            print("These are invalid answers, try again.")
            continue
        elif response == 2:
            print("Please warn the player this is a horrendous idea.")

        print("The chosen factor is " + str(response) + ". Is this correct? Y/n")

        reset = False
        while True:
            validate = input()

            if validate == "":
                return answer
            elif "no".__contains__(validate.lower()):
                reset = True
                break
            elif "yes".__contains__(validate.lower()):
                return answer

        if reset:
            reset = False
            continue

    return answer


def factors(n):
    list = [n]
    factor_range = range(2, int(sqrt(n)) + 1)
    length = len(factor_range)
    count = 1
    pct = 0
    small_list = [1]

    for i in factor_range:
        if n % i == 0:
            list.append(n // i)
            small_list.append(i)
        count += 1

        if not count % int(length / 100.0):
            pct = pct + 1
            sys.stdout.write("\r" + str(pct) + "%")

    sys.stdout.write("\r \n")

    for i in reversed(small_list):
        list.append(i)

    return list


main()
