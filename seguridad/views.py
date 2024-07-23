from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, incidents, comment
from .forms import IncidentsForm, CommentsFrom, CustomUserCreationForm, UserRoleUpdateFrom
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from .decorators import role_required


User = get_user_model()


def index(request):
    return render(request, 'index.html')


@login_required
@role_required('upper_level')
def users_list(request):
    return render(request, 'users/users.html')


@login_required
@role_required('upper_level')
def users_delete(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return render(request, 'users/users.html')


@login_required
@role_required('upper_level')
def users_detail(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'GET':
        form = UserRoleUpdateFrom(instance=user)
        return render(request, 'users/users_detail.html', {
            'user': user,
            'form': form,
        })
    else:
        form = UserRoleUpdateFrom(request.POST, instance=user)
        try:
            if form.is_valid():
                form.save()
                return redirect('users_list')
            else:
                return render(request, 'users/users_detail.html', {
                    'error': "Error updating the user",
                    'user': user,
                    'form': form,
                    'form_errors': form.errors  # Añadido para ver los errores del formulario
                })
        except ValueError:
            return render(request, 'users/users_detail.html', {
                'user': user,
                'form': form,
                'error': "Error updating task"
            })


@login_required
@role_required('upper_level')
def users_by_role(request, role):
    users = CustomUser.objects.filter(role=role)
    return render(request, 'users/users_by_role.html', {
        'users': users,
        'role': role,
    })


@login_required
@role_required('upper_level')
def users_upper_level(request):
    return users_by_role(request, 'upper_level')


@login_required
@role_required('upper_level')
def users_medium_level(request):
    return users_by_role(request, 'medium_level')


@login_required
@role_required('upper_level')
def users_low_level(request):
    return users_by_role(request, 'low_level')


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'sign_in.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'sign_in.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect(index)


@login_required
def sign_out(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm()
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = CustomUser.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': CustomUserCreationForm(),
                    "error": 'User already exists'
                })
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm(),
            "error": 'Password do not match'
        })


@login_required
def create_incident(request):
    if request.method == 'GET':
        return render(request, 'incidents/create_incidents.html', {
            'form': IncidentsForm
        })
    else:
        form = IncidentsForm(request.POST)
        if form.is_valid():
            try:
                new_incidents = form.save(commit=False)
                new_incidents.user = request.user
                new_incidents.save()
                return render(request, 'incidents/incidents.html')
            except ValidationError:
                return render(request, 'incidents/create_incidents.html', {
                    'form': IncidentsForm(),
                    'error': 'Please provide valid data'
                })
        else:
            return render(request, 'incidents/create_incidents.html', {
                'form': form,
                'error': 'Please correct the errors below.'
            })


@login_required
def incidents_delete(request, id):
    incident = get_object_or_404(incidents, incident_id=id)
    if request.method == 'POST':
        incident.delete()
        return render(request, 'incidents/incidents.html')


@login_required
def incidents_list(request):
    return render(request, 'incidents/incidents.html')


@login_required
def incidents_detail(request, id):
    incident = get_object_or_404(incidents, incident_id=id)
    comments = comment.objects.filter(incident=incident)
    if request.method == 'GET':
        form = IncidentsForm(instance=incident)
        form2 = CommentsFrom()
        return render(request, 'incidents/incident_detail.html', {
            'incidents': incident,
            'comments': comments,
            'form': form,
            'form2': form2,
        })
    else:
        form = IncidentsForm(request.POST, instance=incident)
        form2 = CommentsFrom(request.POST)
        try:
            if incident.state == 'resolved':
                # Update status is only allowed if it is resolved
                incident.state = request.POST['state']
                incident.save()
                return redirect('incidents_list')

            if form.is_valid() and form2.is_valid():
                form.save()
                return redirect('incidents_list')
            else:
                return render(request, 'incidents/incident_detail.html', {
                    'Incident': incident,
                    'comments': comments,
                    'form': form,
                    'form2': form2,
                    'error': "Error Updating incident"
                })

        except ValueError:
            return render(request, 'incidents/incident_detail.html', {
                'Incident': incident,
                'comments': comments,
                'form': form,
                'form2': form2,
                'error': "Error Updating incident"
            })


@login_required
def incidents_by_status(request, state):
    incident = incidents.objects.filter(state=state)
    return render(request, 'incidents/incidents_by_status.html', {
        'incidents': incident,
        'state': state,

    })


@login_required
def incidents_new(request):
    return incidents_by_status(request, 'new')


@login_required
def incidents_in_progress(request):
    return incidents_by_status(request, 'in_progress')


@login_required
def incidents_resolver(request):
    return incidents_by_status(request, 'resolved')


@login_required
def incidents_closed(request):
    return incidents_by_status(request, 'closed')


@login_required
def add_comments(request, id):
    incident = get_object_or_404(incidents, incident_id=id)

    if request.method == 'GET':
        return render(request, 'incidents/create_incidents.html', {
            'form': CommentsFrom()
        })
    else:
        form = CommentsFrom(request.POST)

        if form.is_valid():
            try:
                new_comment = form.save(commit=False)
                new_comment.incident = incident
                new_comment.user = request.user
                new_comment.save()
                return redirect('incident_detail', id=incident.incident_id)

            except ValidationError:
                return render(request, 'incidents/create_incidents.html', {
                    'form': form,
                    'error': 'Please provide valid data.'
                })
        else:
            return render(request, 'incidents/create_incidents.html', {
                'form': form,
                'error': 'Please correct the errors below.'
            })
