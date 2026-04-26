from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LogEntry

@login_required
def logs_list(request):
    if not request.user.is_superuser:
        messages.error(request,"Vous n'avez pas accès aux dossiers.")
        return redirect('services:home')

    logs = LogEntry.objects.all()
    context = {'logs': logs}
    return render(request, 'logs/logs_list.html', context)
