import math
from itertools import groupby


class Node(object):
    def __init__(self, value, weight, n, steps):
        self.value = value
        self.weight = weight
        self.n = n
        self.steps = steps
        self.dif_val = weight - value
        self.add_rule = False


def lt(val):
    return val[1] * len(val[2])


def small(lst):
    return len(lst)


def acm(a, m, i_l, i_h, o_l, o_h):
    inputs, outputs = list(range(i_l, i_h + 1)), list(range(o_l, o_h + 1))
    # check for base cases impossible
    if len(inputs) > len(outputs):
        return 'impossible'
    if [inp for inp in inputs if inp > max(outputs)]:
        return 'impossible'
    # check for base case empty
    if len([inp for inp in inputs if inp in outputs]) == len(inputs):
        return 'empty'
    # find path to output range
    max_n, paths = math.floor(math.log((o_h - o_l) / (i_h - i_l), m)), []
    node = Node(i_l, o_h - (i_h - i_l) * (m ** 0), 0, '')
    nodes, cur_node, rule = [[node, node.dif_val, node.steps]], node, [0]
    while rule:
        if paths:
            rule = [n for n in nodes if len(n[2]) < min([len(path) for path in paths])]
        nodes = [n for n in nodes if n[0].steps != '']
        add_node = Node(cur_node.value + a, cur_node.weight, cur_node.n, cur_node.steps + '0')
        if o_l <= cur_node.value <= cur_node.weight:
            paths.append(cur_node.steps)
        else:
            if not cur_node.add_rule:
                if add_node.dif_val >= 0:
                    nodes.append([add_node, add_node.dif_val, add_node.steps])
                if cur_node.n < max_n:
                    mul_node = Node(cur_node.value * m, o_h - (i_h - i_l) * (m ** (cur_node.n + 1)), cur_node.n + 1,
                                    cur_node.steps + '1')
                    if mul_node.dif_val < 0:
                        add_node.add_rule = True
                    elif mul_node.n == max_n:
                        mul_node.add_rule = True
                    if mul_node.n <= max_n and mul_node.dif_val >= 0:
                        nodes.append([mul_node, mul_node.dif_val, mul_node.steps])
            else:
                if cur_node.value + math.ceil((o_l - cur_node.value) / a) * a <= cur_node.weight:
                    paths.append(cur_node.steps + f'{"0" * math.ceil((o_l - cur_node.value) / a)}')
        if nodes:
            nodes.sort(key=lt)
            cur_node = nodes.pop(0)[0]
        elif not nodes and not paths:
            return 'impossible'
    if not paths:
        return 'impossible'
    if o_l <= cur_node.value <= cur_node.weight:
        paths.append(cur_node.steps)
    paths.sort(key=small)
    return ' '.join([str(len(x)) + 'M' if '1' in x else str(len(x)) + 'A' for x in
                     [''.join(g) for _, g in groupby(paths[0])]])


f = open("input.txt", 'r')
lines = f.readlines()
f.close()
input_lst = []
for line in lines:
    if line != '0 0 0 0 0 0':
        line = line[:-1].split(" ")
        input_lst.append([int(li) for li in line])
output_lst = []
for i in input_lst:
    adding, multiplier, input_low, input_high, output_low, output_high = i
    output = acm(adding, multiplier, input_low, input_high, output_low, output_high)
    print(i, output)
    output_lst.append(output + '\n')
f0 = open("output.txt", 'w')
f0.writelines(output_lst)
f0.close()
