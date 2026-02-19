import importlib

def solve():
    q = int(input().strip())
    
    for _ in range(q):
        module_path, attr = input().strip().split()
        
        try:
            module = importlib.import_module(module_path)
            
            if hasattr(module, attr):
                attr_obj = getattr(module, attr)
                if callable(attr_obj):
                    print("CALLABLE")
                else:
                    print("VALUE")
            else:
                print("ATTRIBUTE_NOT_FOUND")
                
        except ImportError:
            print("MODULE_NOT_FOUND")

if __name__ == "__main__":
    solve()