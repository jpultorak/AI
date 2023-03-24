
def opt_dist(row, row_desc):
    n = len(row)
    k = len(row_desc)
    ones = [0 for _ in range(n+1)]
    for i in range(1, n+1):
        ones[i] = ones[i-1]
        if row[i-1] == 1:
            ones[i] += 1

    dp = [[1000 for _ in range(n+1)] for _ in range(k+2)]
    for j in range(1, n+1):
        dp[k+1][j] = ones[n] - ones[j-1]

    for i in range(k, 0, -1):
        # place ith block
        block_len = row_desc[i-1]
        for j in range(1, n+1):
            # placing the block on position [l, p + block_len -1]
            for l in range(j, n-block_len+2):
                r = l+block_len-1
                #print(i, j)
                
                # number of flips needed in the chosen positions
                n1 = block_len - (ones[r] - ones[l-1])
                # number of flips needed to turn [j, l-1] to blanks
                n2 = 0
                if l != j:
                    n2 = ones[j] - ones[l-1]
                # after block we need a blank
                n3 = 0 
                if p+block_len != n+1 and row[p+block_len-1] == 1:
                    n3 = 1
                n4 = 1000
                
                    #print(i+1, j+p+block_len+1, dp[i+1][j+p+block_len+1])
                if i+1 == k and j+p+block_len+1 > n:
                    n4 = 0
                elif j+p+block_len+1 <= n:    
                    n4 = dp[i+1][j+p+block_len+1]
                
                print(i, j, p, n4, n1, n2, n3)                   
                #print(j+p+block_len+1, p, block_len)
                dp[i][j] = min(dp[i][j], n4 + n1 + n2 + n3)
            
            
    print(dp[1][1])

if __name__ == '__main__':
    row = [0,1, 0]
    row_desc = [1, 1]
    opt_dist(row, row_desc)