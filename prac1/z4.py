def opt_dist(s, D):
    n = len(s)
    cnt_1 = [0 for i in range(n+1)]
    for i in range(1, n+1):
        cnt_1[i] = cnt_1[i-1]
        if s[i-1]:
            cnt_1[i] += 1
    
    mx = 0
    for i in range(1, n+2-D):
        flips = 2*(cnt_1[i+D-1] - cnt_1[i-1])
        mx = max(mx, flips)

    return D + cnt_1[n] - mx

if __name__ == '__main__':
    #print(opt_dist('0000000001', 0))
    with open('zad4_input.txt', 'r') as inp, open('zad4_output.txt', 'w') as out:
        for test in inp:
            s, D  = test.split()
            arr_s = [int(x) for x in s]
            res = str(opt_dist(arr_s, int(D))) + '\n'
            out.write(res)
