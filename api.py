import sys


def get_table_cell(value):
    if isinstance(value, float):
        s = str(round(value, 3))
    else:
        s = value
    return s + (12-len(s)) * ' '


class Solver:
    def __init__(self, coefficients, is_max, restrictions):
        self.table = []
        self.basis = []
        self.is_max = is_max
        self.basis_indexes = []
        self.resolution_column = -1
        self.coefficients = coefficients
        self.restrictions_number = len(restrictions)
        max_length = 0
        for i in restrictions:
            max_length = max(max_length, len(i)) - 1
        self.width = max_length + self.restrictions_number
        self.height = self.restrictions_number+1
        for i in range(self.restrictions_number):
            row = []
            for j in range(self.width):
                if j < len(restrictions[i])-1:
                    row.append(restrictions[i][j])
                else:
                    if i == j - max_length:
                        row.append(1.0)
                    else:
                        row.append(0.0)
            row.append(restrictions[i][len(restrictions[i])-1])
            self.table.append(row)
        row = []
        for coefficient in coefficients:
            row.append(-coefficient)
        for i in range(self.height):
            row.append(0.0)
        self.table.append(row)
        self.select_basis()

    def select_basis(self):
        self.basis = ['' for _ in range(self.height-1)]
        self.basis_indexes = [0 for _ in range(self.height-1)]
        for i in range(self.width):
            counter = 0
            index = -1
            for j in range(self.height):
                if self.table[j][i] != 0:
                    counter += 1
                    index = j
            if counter == 1:
                if i < self.width - self.restrictions_number:
                    self.basis[index] = 'x' + str(i+1)
                else:
                    self.basis[index] = 'y' + str(i - self.width + self.restrictions_number + 1)
                self.basis_indexes[index] = i

    def solve(self):
        while not self.is_over():
            self.count_bi()
            self.print(False)
            self.append()
            self.select_basis()
        self.print(True)
        print()
        variables = [None for _ in range(len(self.coefficients))]
        for i in range(self.height-1):
            var = self.table[i][self.width] / self.table[i][self.basis_indexes[i]]
            print(f'{self.basis[i]}={round(var, 3)}')
            if self.basis[i][0] == 'x':
                variables[int(self.basis[i][1:])-1] = var
        success = variables.count(None) == 0
        if success:
            print('f(', end='')
            print('; '.join(list(map(str, variables))), end='')
            res = 0
            for i in range(len(variables)):
                res += variables[i] * self.coefficients[i]
            print(') =', res)

    def count_bi(self):
        self.resolution_column = self.get_resolution_column_index()
        for i in range(self.height-1):
            self.table[i].append(self.table[i][self.width] / self.table[i][self.resolution_column])

    def is_over(self):
        f = (lambda x: x < 0) if self.is_max else (lambda x: x > 0)
        for i in range(self.width+1):
            if f(self.table[self.height-1][i]):
                return False
        return True

    def append(self):
        best = float('inf')
        h_index = -1
        for i in range(self.height-1):
            if 0 < self.table[i][self.width + 1] < best:
                best = self.table[i][self.width+1]
                h_index = i
        new_table = [[] for _ in range(self.height)]
        for i in range(self.width+1):
            new_table[h_index].append(self.table[h_index][i])
        for i in range(self.height):
            if i != h_index:
                coef = -(self.table[i][self.resolution_column] / self.table[h_index][self.resolution_column])
                for j in range(self.width+1):
                    new_table[i].append(self.table[i][j] + self.table[h_index][j] * coef)
        self.table = new_table

    def get_resolution_column_index(self):
        index = -1
        f = (lambda x, y: x < y) if self.is_max else (lambda x, y: x > y)
        best = (1 if self.is_max else -1) * sys.maxsize
        for i in range(self.width + 1):
            if f(self.table[self.height - 1][i], best):
                best = self.table[self.height - 1][i]
                index = i
        return index

    def print(self, end):
        print(get_table_cell('Базис'), end='')
        for i in range(self.width):
            if i < self.width - self.restrictions_number:
                print(get_table_cell('x' + str(i+1)), end='')
            else:
                print(get_table_cell('y' + str(i - self.width + self.restrictions_number + 1)), end='')
        print(get_table_cell('bi'), end='')
        print(get_table_cell('bi/разр. ст.'))
        for i in range(len(self.basis)):
            print(get_table_cell(self.basis[i]), end='')
            for j in range(self.width+(1 if end else 2)):
                print(get_table_cell(self.table[i][j]), end='')
            print()
        print(get_table_cell('f(x)'), end='')
        for i in range(self.width+1):
            print(get_table_cell(self.table[len(self.table)-1][i]), end='')
        print()
        if not end:
            print(12 * (self.width + 3) * '-')
