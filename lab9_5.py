def create_report(employee): 
    for key, value in employee.items():
        print(f"{key}: {value}")

#Вызоваем функцию (пример)
employee = {
    "Name": "Skribka-Filatova",
    "Age": 21,
    "Department": "Analyst",
    "Salary": 30000,
    "Bonus": 5000,
    "Performance Score": 5
}

create_report(employee)
