import statistics

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import viewsets

from .serializers import SalarySerializer
from .forms import SalaryForm
from .models import Salary


@login_required(login_url='login')
def salary_list(request):
    salaries_obj = Salary.objects.all()
    salaries = []
    for salary in salaries_obj:
        salaries.append(salary.salary)
    if len(salaries) > 0:
        best_salary = max(salaries)
        worst_salary = min(salaries)
        average_wages = statistics.mean(salaries)
    else:
        best_salary = None
        worst_salary = None
        average_wages = None
    discounts = []
    for discount in salaries_obj:
        discounts.append(discount.discounts)
    if len(discounts) > 0:
        average_discounts = statistics.mean(discounts)
    else:
        average_discounts = None
    context = {
        'salary_list': salaries_obj,
        'best_salary': best_salary,
        'worst_salary': worst_salary,
        'average_wages': average_wages,
        'average_discounts': average_discounts
    }
    return render(request, "salary_register/salary_list.html", context)


@login_required(login_url='login')
def salary_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = SalaryForm()
        else:
            salary = Salary.objects.get(pk=id)
            form = SalaryForm(instance=salary)
        return render(request, "salary_register/salary_form.html", {'form': form})
    else:
        if id == 0:
            form = SalaryForm(request.POST)
        else:
            salary = Salary.objects.get(pk=id)
            form = SalaryForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("<script>alert('Please do not try to insert fake data. Date must be in mm/dd/yyyy format.')</script>")
        return redirect('/salaries')


@login_required(login_url='login')
def salary_delete(request, id):
    salary = Salary.objects.get(pk=id)
    salary.delete()
    return redirect('/salaries')


class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all().order_by('salary')
    serializer_class = SalarySerializer
