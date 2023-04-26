import numpy


def find_path(lst, a, m, outs):
    lst_0 = []
    for l in lst:
        if l + a > max(outs) or l == -1:
            lst_0.append(-1)
        else:
            lst_0.append(l + a)
        if l * m > max(outs) or l == -1 or l * m == l:
            lst_0.append(-1)
        else:
            lst_0.append(l * m)
    return lst_0


def decimal_binary(n, s):
    b = "{0:b}".format(int(n))
    while len(b) < s:
        b = '0' + b
    return b


def aCm(a, m, i_l, i_h, o_l, o_h):
    inputs = list(range(i_l, i_h + 1))
    outputs = list(range(o_l, o_h + 1))
    if len(inputs) > len(outputs):
        return 'impossible'
    # check if inputs are already in output
    check_0 = [inp for inp in inputs if inp in outputs]
    if len(check_0) == len(inputs):
        return 'empty'
    # check if inputs are greater than outputs (impossible to reduce)
    if [inp for inp in inputs if inp > max(outputs)]:
        return 'impossible'
    # find fastest path to output range
    lst_inp = [inputs[0]]
    operation = []
    while not operation:
        while max(lst_inp) not in outputs:
            lst_inp = find_path(lst_inp, a, m, outputs)
            if lst_inp == [-1] * len(lst_inp):
                return 'impossible'
        lst_ind = [lst_inp.index(inp) for inp in lst_inp if inp in outputs]
        step = numpy.log(len(lst_inp)) / numpy.log(2)
        lst_bin = [decimal_binary(ind, step) for ind in lst_ind]
        for str_bin in lst_bin:
            for inp in inputs[1:]:
                tmp_inp = inp
                for op in str_bin:
                    if op == '0':
                        tmp_inp += a
                    else:
                        tmp_inp = tmp_inp * m
                if tmp_inp in outputs:
                    operation.append(str_bin)
            if len(operation) == len(inputs) - 1:
                break
            else:
                operation = []
                lst_inp = find_path(lst_inp, a, m, outputs)
    if len(operation[0]) > 1:
        path, prev_ele = operation[0][0], operation[0][0]
        for next_ele in operation[0][1:]:
            if prev_ele == next_ele:
                path += next_ele
            else:
                path += ',' + next_ele
                prev_ele = next_ele
        path = path.split(',')
    else:
        path = [operation[0]]
    final_path = ''
    for p in path:
        l = str(len(p))
        if p[0] == '0':
            l += 'A '
        else:
            l += 'M '
        final_path += l
    return final_path


f = open("input.txt", 'r')
lines = f.readlines()
f.close()
input_lst = []
for line in lines:
    if line != '0 0 0 0 0 0':
        line = line[:-1].split(" ")
        input_lst.append([int(l) for l in line])
output_lst = []
for inp in input_lst:
    adding, multiplier, input_low, input_high, output_low, output_high = inp
    output = aCm(adding, multiplier, input_low, input_high, output_low, output_high)
    print(inp, output)
    output_lst.append(output + '\n')
f0 = open("output.txt", 'w')
f0.writelines(output_lst)
f0.close()
