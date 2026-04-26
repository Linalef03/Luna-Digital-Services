from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Service
from .forms import ServiceForm
from logs.utils import create_log


@login_required
def service_list(request):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez aucune autorité.")
        return redirect('services:home')

    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})


@login_required
def add_service(request):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez aucune autorité.")
        return redirect('services:home')

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()

            create_log(request.user, f"Ajout d'un nouveau service : {service.name}")

            messages.success(request, " Service ajouté avec succès ")
            return redirect('services:service_list')
    else:
        form = ServiceForm()

    return render(request, 'services/service_form.html', {'form': form})


@login_required
def edit_service(request, service_id):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez aucune autorité.")
        return redirect('services:home')

    service = get_object_or_404(Service, id=service_id)

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()

            create_log(request.user, f"modifier du service : {service.name}")

            messages.success(request," Le service a été modifié avec succès ")
            return redirect('services:service_list')
    else:
        form = ServiceForm(instance=service)

    return render(request, 'services/service_form.html', {'form': form})


@login_required
def delete_service(request, service_id):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez aucune autorité.")
        return redirect('services:home')

    service = get_object_or_404(Service, id=service_id)

    if request.method == "POST":
        create_log(request.user, f"Supprimer le service : {service.name}")

        service.delete()

        messages.success(request, " Le service a été supprimé ")
        return redirect('services:service_list')

    return render(request, 'services/service_confirm_delete.html', {'service': service})
