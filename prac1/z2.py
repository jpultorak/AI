import numpy as np

def retrieve(l, r, dp, s):
    if dp[l][r][1] == r:
        return s[l:r+1]
    
    k = dp[l][r][1]
    return retrieve(l, k, dp, s) + " " + retrieve(k+1, r, dp, s)

def add_spaces(s, words):
    n = len(s)
    dp = np.full((n, n, 2), -1, dtype = int)
    
    for sz in range(1, n+1):
        for l in range(0, n-sz+1):
            r = l + sz - 1
            if s[l:r+1] in words:
                dp[l][r] = [sz*sz, r]
            else:
                for k in range(l, r):
                    if dp[l][k][0] == -1 or dp[k+1][r][0] == -1:
                        continue
                    val = dp[l][k][0] + dp[k+1][r][0]
                    if val > dp[l][r][0]:
                        dp[l][r] = [val, k]

    # retrieve words from dp
    if dp[0][n-1][0] == -1:
        return None
    return retrieve(0, n-1, dp, s)

if __name__ == '__main__':
    # words = set(['matematyk', 'matematyka', 'a', 'ale', 'mur'])
    # res = add_spaces('matematykalemur', words)
    with open('words_for_ai1.txt', 'r', encoding='utf-8') as wrd, open('pan_tadeusz_bez_spacji.txt', 'r', encoding='utf-8') as inp, open('zad2_output.txt', 'w', encoding='utf-8') as out:
        words = set([word.strip('\n') for word in wrd.readlines()])
        lines = [line.strip('\n') for line in inp.readlines()]
        for line in lines:
            new_line = add_spaces(line, words)
            out.write(new_line + '\n')
        