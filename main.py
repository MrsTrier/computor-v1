import sys
import re
import math
from itertools import groupby


def calculate_descriminant(coeffs):
    if 0 not in coeffs:
        coeffs[0] = 0
    if 1 not in coeffs:
        coeffs[1] = 0
    d = coeffs[1] * coeffs[1] - 4 * coeffs[0] * coeffs[2]
    if d == 0:
        result = f'{-coeffs[1] / (2 * coeffs[2]) : g}'
        result = "0" if result == "-0" else result
        result = f"Discriminant is equals zero, the only solution is:\n{result}"
    elif d > 0:
        result = "Discriminant is strictly positive, the two solutions are:\n{0:.6f}"\
                .format((- coeffs[1] - math.sqrt(d)) / (2 * coeffs[2])).rstrip('0').rstrip('.')
        result += "\n{0:.6f}".format((- coeffs[1] + math.sqrt(d)) / (2 * coeffs[2])).rstrip('0').rstrip('.')
    else:
        result = "Discriminant not positive"
    print(result)


def get_polynomial_degree(powers):
    if len(powers) == 0:
        print("Polynomial degree: {}".format(0))
        print("The solution is: each real number")
        exit(0)
    max_pow = max(powers)
    print("Polynomial degree: {}".format(f'{max_pow:g}'))
    if max_pow not in [0, 1, 2]:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        exit(0)
    return max_pow


def reduced_form(coeffs):
    res = ""
    for i in sorted(coeffs):
        num = coeffs[i]
        if num == 0:
            coeffs.pop(i)
            if len(coeffs.keys()) == 0:
                print("0 = 0")
                return
            continue
        if num > 0:
            num = "+ " + "{}".format(coeffs[i])
        elif num < 0:
            num = "- " + "{}".format(coeffs[i] * -1)
        res += "{} * X^{} ".format(num, f'{i:g}')
    if res[0] == '+':
        res = res[2:]
    res += "= 0"
    res = "Reduced form: " + res
    print(res)


def get_tuple(equation_part):
    res = re.findall(r'(-*\d+|-*\d+\.\d+)\*[Xx]\^(\d+\.*\d*)', equation_part)
    for indx, t in enumerate(res):
        res[indx] = tuple(float(x) for x in t)
    return res


def dict_from_tuple(tupl, left):
    for key, group in groupby(tupl, lambda x: x[0]):
        for thing in group:
            if thing[1] in dictionary:
                if left:
                    dictionary[thing[1]] += key
                else:
                    dictionary[thing[1]] -= key
            else:
                dictionary[thing[1]] = key if left else -key


def calculate_first_polinom(coeffs):
    print("The solution is:\n{}".format(-coeffs[0]/coeffs[1]))
    return -coeffs[0]/coeffs[1]


if __name__ == '__main__':
    equation = sys.argv[1]
    equation = equation.replace(" ", "")
    lhs = equation.split("=")[0]
    rhs = equation.split("=")[1]

    if len(equation.split("=")) != 2:
        print("Error: entry mistake")
        exit(0)

    res = get_tuple(lhs)
    res_rhs = get_tuple(rhs)

    dictionary = {}
    dict_from_tuple(res, 1)
    dict_from_tuple(res_rhs, 0)

    reduced_form(dictionary)
    polynomial_degree = get_polynomial_degree(dictionary.keys())


    if polynomial_degree == 1:
        calculate_first_polinom(dictionary)
    elif polynomial_degree == 0:
        print("Error")
    else:
        calculate_descriminant(dictionary)


