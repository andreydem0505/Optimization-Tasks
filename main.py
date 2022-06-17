from api import Solver


def take_coefficients(s):
    parameters = ['x' + str(i) for i in range(1, 10)]
    coef = []
    last_found = -2
    for parameter in parameters:
        index = s.find(parameter)
        if index > -1:
            try:
                coef.append(float(s[last_found + 2:index]))
            except ValueError:
                coef.append(float(('' if s[last_found + 2] != '-' else '-') + '1'))
            last_found = index
        else:
            break
    return coef


if __name__ == '__main__':
    print('Решение оптимизационных задач')
    f = input('Введите функцию: ')
    coefficients = take_coefficients(f)
    print('Стремимся к 1) максимуму или 2) минимуму?')
    digit = -1
    while digit not in range(1, 3):
        try:
            digit = int(input())
        except ValueError:
            continue
    is_max = True if digit == 1 else False
    n = int(input('Введите количество ограничений: '))
    restrictions = []
    for i in range(n):
        print(f'Введите левую часть ограничения №{i + 1}:')
        left_side = take_coefficients(input())
        print(f'Введите правую часть ограничения №{i + 1}:')
        right_side = float(input())
        left_side.append(right_side)
        if right_side < 0:
            for j in range(len(left_side)):
                left_side[j] *= -1
        restrictions.append(left_side)
    solver = Solver(coefficients, is_max, restrictions)
    solver.solve()
    input()
