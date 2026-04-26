from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmployeeForm
from .models import Employee
from logs.utils import create_log


# ================================
# dashboard de admin
# ================================
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request,"Vous n'êtes pas autorisé à entrer ici")
        return redirect('dashboard:admin_dashboard')

    orders = Order.objects.all().order_by('-created_at')
    employees = User.objects.filter(is_superuser=False)

    return render(request, 'dashboard/admin_dashboard.html', {
        'orders': orders,
        'employees': employees,
    })


# ================================
# Attribution de la demande à un employé
# ================================
@login_required
def assign_order(request, order_id):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez aucune autorité")
        return redirect('dashboard:admin_dashboard')

    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        employee = get_object_or_404(User, id=employee_id, is_superuser=False)

        order.employee = employee
        order.status = 'assigned'
        order.save()

        create_log(request.user, f"Il a fixé la demande #{order.id} À l'employé{employee.username}")

        messages.success(request, f"Demande #{order.id} à {employee.username}")
        return redirect('dashboard:admin_dashboard')

    employees = User.objects.filter(is_superuser=False)
    return render(request, 'dashboard/assign_order.html', {
        'order': order,
        'employees': employees
    })


# ================================
# liste des employees
# ================================
@login_required
def employees_list(request):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez aucune autorité")
        return redirect('dashboard:admin_dashboard')

    employees = Employee.objects.select_related('user').all()

    return render(request, 'dashboard/employee_list.html', {'employees': employees})


# ================================
# ajouter employee
# ================================
@login_required
def add_employee(request):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez aucune autorité")
        return redirect('dashboard:admin_dashboard')

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(email=email).exists():
                messages.error(request, " L email est déjà utilisé. ")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)

                employee = form.save(commit=False)
                employee.user = user
                employee.save()

                create_log(request.user, f"Il a ajouté un nouvel employé nommé {username}")

                messages.success(request, f"L'employé a été ajouté {username} Avec succès !")
                return redirect('dashboard:employees_list')
    else:
        form = EmployeeForm()

    return render(request, 'dashboard/add_employee.html', {'form': form})


# ================================
#  modifier employee
# ================================
@login_required
def edit_employee(request, employee_id):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez aucune autorité")
        return redirect('dashboard:admin_dashboard')

    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        role = request.POST.get('role')
        password = request.POST.get('password')

        if username:
            employee.user.username = username
        if email:
            employee.user.email = email
        if password:
            employee.user.set_password(password)
        employee.user.save()

        employee.phone = phone
        employee.address = address
        employee.role = role
        employee.save()

        create_log(request.user, f" Modifier les données des employee {employee.user.username}")

        messages.success(request, f"L'employé a été modifié {employee.user.username}")
        return redirect('dashboard:employees_list')

    return render(request, 'dashboard/edit_employee.html', {'employee': employee})


# ================================
# supprimer employee
# ================================
@login_required
def delete_employee(request, employee_id):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez aucune autorité")
        return redirect('dashboard:admin_dashboard')

    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        create_log(request.user, f" Supprimer l'employé {employee.user.username}")

        employee.user.delete()
        employee.delete()

        messages.success(request, " L'employé a été supprimé avec succès. ")
        return redirect('dashboard:employees_list')

    return render(request, 'dashboard/delete_employee.html', {'employee': employee})


# ================================
# dashboard de employee
# ================================
@login_required
def employee_dashboard(request):
    if request.user.is_superuser:
        messages.error(request, " Le panneau réservé aux employés n'appartient pas au gérant. ")
        return redirect('dashboard:admin_dashboard')

    orders = Order.objects.filter(employee=request.user).order_by('-created_at')

    return render(request, 'dashboard/employee_dashboard.html', {
        'orders': orders
    })


# ================================
# Début du traitement de la demande
# ================================
@login_required
def start_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.employee != request.user:
        messages.error(request, "❌ Vous ne pouvez pas initier cette requête car elle ne vous est pas destinée.")
        return redirect('dashboard:employee_dashboard')

    order.status = 'in_progress'
    order.save()

    create_log(request.user, f"Les travaux ont commencé à la demande # {order.id}")

    messages.success(request, f"Les travaux ont commencé sur la demande # {order.id}")
    return redirect('dashboard:employee_dashboard')


# ================================
# finie la commande
# ================================
@login_required
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.employee != request.user:
        messages.error(request, "❌ Vous ne pouvez pas initier cette requête car elle ne vous est pas destinée.")
        return redirect('dashboard:employee_dashboard')

    if request.method == 'POST':
       
        final_file = request.FILES.get('final_file')
        if final_file:
            order.final_file = final_file

        order.status = 'completed'
        order.save()

      
        create_log(request.user, f"Commande terminée #{order.id}")

        messages.success(request, f"✔ Commande terminée #{order.id}")
        return redirect('dashboard:employee_dashboard')

    return render(request, 'dashboard/complete_order.html', {'order': order})


# ================================
# mange orders
# ================================
@login_required
def manage_orders(request):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez aucune autorité")
        return redirect('dashboard:admin_dashboard')

    orders = Order.objects.all().order_by('-created_at')
    employees = User.objects.filter(employee__isnull=False)

    return render(request, 'dashboard/manage_orders.html', {
        'orders': orders,
        'employees': employees,
    })
