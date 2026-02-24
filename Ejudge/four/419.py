import math

def solve():
    R = float(input().strip())
    x1, y1 = map(float, input().strip().split())
    x2, y2 = map(float, input().strip().split())
    
    d1 = x1*x1 + y1*y1
    d2 = x2*x2 + y2*y2
    d_ab = math.hypot(x2 - x1, y2 - y1)
    
    if d_ab == 0:
        print("0.0000000000")
        return
    
    
    vx = x2 - x1
    vy = y2 - y1
    a = vx*vx + vy*vy
    b = 2 * (x1*vx + y1*vy)
    c = d1 - R*R
    
    discriminant = b*b - 4*a*c
    
   
    if discriminant > 0:
        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b - sqrt_disc) / (2*a)
        t2 = (-b + sqrt_disc) / (2*a)
        
        if (0 <= t1 <= 1) or (0 <= t2 <= 1):
            l1 = math.sqrt(max(0, d1 - R*R))
            l2 = math.sqrt(max(0, d2 - R*R))
            
            dot = x1*x2 + y1*y2
            cos_phi = dot / (math.sqrt(d1 * d2))
            cos_phi = max(-1, min(1, cos_phi))
            phi = math.acos(cos_phi)
            
            alpha1 = math.acos(R / math.sqrt(d1))
            alpha2 = math.acos(R / math.sqrt(d2))
            
            central_angle = phi - alpha1 - alpha2
            if central_angle < 0:
                central_angle = 2*math.pi - (alpha1 + alpha2 + phi)
                if central_angle > math.pi:
                    central_angle = 2*math.pi - central_angle
            
            central_angle = abs(central_angle)
            arc_length = R * central_angle
            total_length = l1 + arc_length + l2
            
            print(f"{total_length:.10f}")
            return

    print(f"{d_ab:.10f}")

if __name__ == "__main__":
    solve()