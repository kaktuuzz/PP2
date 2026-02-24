import math

def solve():
    R = float(input().strip())
    x1, y1 = map(float, input().strip().split())
    x2, y2 = map(float, input().strip().split())
    
    vx = x2 - x1
    vy = y2 - y1
    
    a = vx*vx + vy*vy
    b = 2 * (x1*vx + y1*vy)
    c = x1*x1 + y1*y1 - R*R
    
    if a == 0:
        print("0.0000000000")
        return
    
    discriminant = b*b - 4*a*c
    
    if discriminant < 0:
        print("0.0000000000")
        return
    
    sqrt_disc = math.sqrt(discriminant)
    t1 = (-b - sqrt_disc) / (2*a)
    t2 = (-b + sqrt_disc) / (2*a)
    
    if t1 > t2:
        t1, t2 = t2, t1
    
    valid_t = []
    for t in [t1, t2]:
        if 0 <= t <= 1:
            valid_t.append(t)
    
    endpoints_inside = []
    if x1*x1 + y1*y1 <= R*R:
        endpoints_inside.append(0)
    if x2*x2 + y2*y2 <= R*R:
        endpoints_inside.append(1)
    
    all_points = valid_t + endpoints_inside
    
    if not all_points:
        print("0.0000000000")
        return
    
    t_min = min(all_points)
    t_max = max(all_points)
    
    length = math.sqrt(a) * (t_max - t_min)
    
    print(f"{length:.10f}")

if __name__ == "__main__":
    solve()