from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cooperation

@login_required
def create_event(request):
    if request.method == 'POST':
        event = Cooperation.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            date=request.POST['date'],
            creator=request.user
        )
        event.participants.add(request.user)
        return redirect('event_detail', event.id)
    return render(request, 'create_event.html')

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Cooperation, id=event_id)
    if request.user not in event.participants.all():
        event.participants.add(request.user)
    return redirect('event_detail', event_id)

def event_detail(request, event_id):
    event = get_object_or_404(Cooperation, id=event_id)
    return render(request, 'C.html', {'event': event})