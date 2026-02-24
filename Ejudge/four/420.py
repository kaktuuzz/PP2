def solve():
    m = int(input().strip())
    g = 0
    n = 0
    
    for _ in range(m):
        scope, val = input().strip().split()
        val = int(val)
        
        if scope == "global":
            g += val
        elif scope == "nonlocal":
            n += val
        elif scope == "local":
            pass
    
    print(g, n)

if __name__ == "__main__":
    solve()