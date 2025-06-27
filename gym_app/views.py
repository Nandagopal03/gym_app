from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from .models import Attendance, Fee, ClientProfile, DietPlan, Announcement
from .forms import AttendanceForm, ClientProfileForm, DietPlanForm, AnnouncementForm
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



@login_required
def view_profile(request):
    if not request.user.groups.filter(name='Client').exists():
        return redirect('dashboard')

    profile = get_object_or_404(ClientProfile, user=request.user)
    return render(request, 'view_profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    if not request.user.groups.filter(name='Client').exists():
        return redirect('dashboard')

    profile, created = ClientProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ClientProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


from django.db.models import Q

@login_required
@user_passes_test(is_trainer)
def client_list(request):
    query = request.GET.get('q')
    clients = ClientProfile.objects.all()

    if query:
        clients = clients.filter(
            Q(user__username__icontains=query) |
            Q(full_name__icontains=query)
        )

    return render(request, 'trainer/client_list.html', {
        'clients': clients,
        'query': query
    })
    
@login_required
@user_passes_test(is_trainer)
def view_client_profile(request, user_id):
    profile = get_object_or_404(ClientProfile, user__id=user_id)
    return render(request, 'trainer/view_client_profile.html', {'profile': profile})


@login_required
@user_passes_test(is_trainer)
def edit_diet_plan(request, user_id):
    client = get_object_or_404(User, id=user_id)
    diet, created = DietPlan.objects.get_or_create(client=client)

    if request.method == 'POST':
        form = DietPlanForm(request.POST, instance=diet)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.created_by = request.user
            plan.save()
            return redirect('client_list')  # or view_client_profile
    else:
        form = DietPlanForm(instance=diet)

    return render(request, 'trainer/edit_diet_plan.html', {
        'form': form,
        'client': client
    })
    
@login_required
def view_my_diet_plan(request):
    if not request.user.groups.filter(name='Client').exists():
        return redirect('dashboard')

    try:
        plan = request.user.diet_plan
    except DietPlan.DoesNotExist:
        plan = None

    return render(request, 'client/view_diet_plan.html', {'plan': plan})

@login_required
def announcements_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    is_trainer = request.user.groups.filter(name='Trainer').exists()  # or your logic
    return render(request, 'announcements/list.html', {
        'announcements': announcements,
        'is_trainer': is_trainer,
    })

@login_required
@user_passes_test(is_trainer)
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.posted_by = request.user
            announcement.save()
            return redirect('announcements_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/create.html', {'form': form})