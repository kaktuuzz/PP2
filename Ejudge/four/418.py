def solve():
    x1, y1 = map(float, input().strip().split())
    x2, y2 = map(float, input().strip().split())
    
    x = x1 + y1 * (x2 - x1) / (y2 + y1)
    
    print(f"{x:.10f} 0.0000000000")

if __name__ == "__main__":
    solve()