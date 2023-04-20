import numpy


def find_path(lst, a, m, outs):
    lst_0 = []
    for l in lst:
        if l == -1 or l > max(outs):
            lst_0.append(-1)
            lst_0.append(-1)
        elif l <= max(outs):
            lst_0.append(l + a)
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
    # check if inputs are already in output
    check_0 = [inp for inp in inputs if inp in outputs]
    if len(check_0) == len(inputs):
        return 'empty'
    # check if inputs are greater than outputs (impossible to reduce)
    check_1 = [inp for inp in inputs if inp > max(outputs)]
    if check_1:
        return 'impossible'
    # find way to get to output range
    all_paths = []
    for inp in inputs:
        paths = []
        lst_inp = [inp]
        while min([inp for inp in lst_inp if inp != -1]) < min(outputs):
            lst_inp = find_path(lst_inp, a, m, outputs)
            lst_tst = [inp for inp in lst_inp if inp in outputs]
            if lst_tst:
                paths.append(lst_inp)
        all_paths.append(paths)
    possible_path = []
    for paths in all_paths:
        other_paths_0 = [paths for paths in all_paths[:all_paths.index(paths)]]
        other_paths_1 = [paths for paths in all_paths[all_paths.index(paths) + 1:]]
        if not other_paths_0:
            other_paths_0 = [[[0]]]
        if not other_paths_1:
            other_paths_1 = [[[0]]]
        for path in paths:
            if len(path) in [len(p) for p in other_paths_0[0]] or len(path) in [len(p) for p in other_paths_1[0]]:
                possible_path.append(path)
    if not possible_path:
        return 'impossible'
    small = min(possible_path)
    all_small = [path for path in possible_path if len(path) == len(small)]
    possible_inds = []
    while not possible_inds:
        p_inds = []
        for a_s in all_small:
            p_ind = [a_s.index(pt) for pt in a_s if pt in outputs]
            p_inds.append(p_ind)
        for p_ind in p_inds:
            for p_i in p_ind:
                for p in p_inds[:p_inds.index(p_ind)]:
                    if p_i in p and p_i not in possible_inds:
                        possible_inds.append(p_i)
                for p in p_inds[p_inds.index(p_ind) + 1:]:
                    if p_i in p and p_i not in possible_inds:
                        possible_inds.append(p_i)
        if not possible_inds:
            small = min([path for path in possible_path if len(path) > len(small)])
            all_small = [path for path in possible_path if len(path) == len(small)]
    tmp_inds = []
    for ind, n_path in zip(possible_inds, small):
        tmp_inds.append([ind, n_path])
    tmp_inds = sorted(tmp_inds, key=lambda x: x[1])
    inds = [ind for ind, n_path in tmp_inds]
    step = numpy.log(len(small)) / numpy.log(2)
    lst_b = [decimal_binary(ind, step) for ind in inds]
    operations = []
    for b in lst_b:
        tmp_lst = b[0]
        prev_ele = b[0]
        for ele in b[1:]:
            if ele != prev_ele:
                tmp_lst += ',' + ele
            else:
                tmp_lst += ele
            prev_ele = ele
        tmp_lst = tmp_lst.split(',')
        operation = []
        for ele in tmp_lst:
            if '0' in ele:
                operation.append(f'{len(ele)}A')
            else:
                operation.append(f'{len(ele)}M')
        operations.append(operation)
    return ' '.join(operations[0])


f = open("input.txt", 'r')
lines = f.readlines()
f.close()
inputs = []
for line in lines:
    if line != '0 0 0 0 0 0':
        line = line[:-1].split(" ")
        inputs.append([int(l) for l in line])
outputs = []
for inp in inputs:
    adding, multiplier, input_low, input_high, output_low, output_high = inp
    output = aCm(adding, multiplier, input_low, input_high, output_low, output_high)
    outputs.append(output + '\n')
f0 = open("output.txt", 'w')
f0.writelines(outputs)
f0.close()
