from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Test
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') 
import io
import base64

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello World")

def greet(request, name):
    return HttpResponse(f"Hi! {name}, Greetings for the day!")

def dashboard(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        unit = request.POST.get('unit')
        Test.objects.create(name=name,age=age,unit=unit)
        return redirect('dashboard')
    # Fetch all employee data
    else:
        res = Test.objects.all()
        data = []
        for i in res:
            emp_data = {
                'id': i.id,
                'name': i.name,
                'age': i.age,
                'unit': i.unit,
            }
            data.append(emp_data)
        
        context = {'data': data}  # Pass the data to the template
        return render(request, 'index.html', context)



def edit_emp(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        age = request.POST.get('age')
        unit = request.POST.get('unit')

        # Update the employee data in the database
        Test.objects.filter(pk=id).update(name=name, age=age, unit=unit)
        
        # Redirect to dashboard after updating
        return redirect('dashboard')

    else:
        # If the method is GET, fetch the employee details to edit
        id = request.GET.get('id')
        emp_data = Test.objects.get(pk=id)
        
        context = {
            'id': id,
            'name': emp_data.name,
            'age': emp_data.age,
            'unit': emp_data.unit,
        }
        
        return render(request, 'edit.html', context)
# Statistics View
def statistics(request):
    employees = Test.objects.all()

    # Unit-wise count
    unit_count = {}
    for emp in employees:
        unit_count[emp.unit] = unit_count.get(emp.unit, 0) + 1

    plt.figure(figsize=(6, 4))
    plt.bar(unit_count.keys(), unit_count.values(), color='skyblue')
    plt.title('Employee Count by Unit')
    plt.xlabel('Unit')
    plt.ylabel('Count')
    unit_chart = io.BytesIO()
    plt.savefig(unit_chart, format='png')
    unit_chart.seek(0)
    unit_chart_base64 = base64.b64encode(unit_chart.getvalue()).decode()

    # Age distribution
    age_data = [emp.age for emp in employees]
    plt.figure(figsize=(6, 4))
    plt.hist(age_data, bins=5, color='lightgreen', edgecolor='black')
    plt.title('Employee Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    age_chart = io.BytesIO()
    plt.savefig(age_chart, format='png')
    age_chart.seek(0)
    age_chart_base64 = base64.b64encode(age_chart.getvalue()).decode()

    context = {
        'unit_chart': unit_chart_base64,
        'age_chart': age_chart_base64,
    }
    return render(request, 'statistics.html', context)