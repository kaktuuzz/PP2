class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def total_salary(self):
        return self.base_salary


class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        super().__init__(name, base_salary)
        self.bonus_percent = bonus_percent

    def total_salary(self):
        return self.base_salary * (1 + self.bonus_percent / 100)


class Developer(Employee):
    def __init__(self, name, base_salary, completed_projects):
        super().__init__(name, base_salary)
        self.completed_projects = completed_projects

    def total_salary(self):
        return self.base_salary + self.completed_projects * 500


class Intern(Employee):
    pass



data = input().split()
role = data[0]

if role == "Manager":
    _, name, base_salary, bonus = data
    emp = Manager(name, int(base_salary), int(bonus))

elif role == "Developer":
    _, name, base_salary, projects = data
    emp = Developer(name, int(base_salary), int(projects))

else:  
    _, name, base_salary = data
    emp = Intern(name, int(base_salary))


print(f"Name: {emp.name}, Total: {emp.total_salary():.2f}")
