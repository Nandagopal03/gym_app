from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from .models import Attendance, Fee
from .forms import AttendanceForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now

def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


@login_required
def dashboard(request):
    user = request.user
    is_trainer = user.groups.filter(name='Trainer').exists()
    is_client = user.groups.filter(name='Client').exists()

    return render(request, 'dashboard.html', {
        'is_trainer': is_trainer,
        'is_client': is_client,
    })
# gym_app/views.py


def is_trainer(user):
    return user.groups.filter(name='Trainer').exists()

@login_required
@user_passes_test(is_trainer)
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            selected_clients = form.cleaned_data['clients']

            for client in selected_clients:
                Attendance.objects.update_or_create(
                    client=client,
                    date=date,
                    defaults={'present': True}
                )
            return redirect('dashboard')
    else:
        form = AttendanceForm()
    return render(request, 'mark_attendance.html', {'form': form})


@login_required
def view_attendance(request):
    if request.user.groups.filter(name='Client').exists():
        records = Attendance.objects.filter(client=request.user).order_by('-date')
        return render(request, 'view_attendance.html', {'records': records})
    return redirect('dashboard')




def is_trainer(user):
    return user.groups.filter(name='Trainer').exists()

@login_required
@user_passes_test(is_trainer)
def view_all_fees(request):
    # Show all fee records sorted by client name and due date
    fees = Fee.objects.all().order_by('client__username', 'due_date')
    return render(request, 'view_all_fees.html', {'fees': fees})


@login_required
def view_fees(request):
    if request.user.groups.filter(name='Client').exists():
        fees = Fee.objects.filter(client=request.user).order_by('-due_date')
        next_due = fees.filter(paid=False, due_date__gte=now().date()).order_by('due_date').first()
        return render(request, 'view_fees.html', {
            'fees': fees,
            'next_due': next_due
        })
    return redirect('dashboard')
