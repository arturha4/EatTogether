from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cooperation


@login_required
def cooperation(request):
    if request.method == 'POST':
        print(request.POST)
        event = Cooperation.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            date=request.POST.get('date'),
            creator=request.user
        )
        event.participants.add(request.user)
        event.save()
        return redirect('event-detail', event.id)
    return render(request, 'events.html', context={'events': Cooperation.objects.all()})


@login_required
def join_event(request, event_id):
    event = get_object_or_404(Cooperation, id=event_id)
    if request.user not in event.participants.all():
        event.participants.add(request.user)
    return redirect('event-detail', event_id)


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Cooperation, id=event_id)
    return render(request, 'event_detail.html', {'event': event})


def delete_event(request, event_id):
    event = get_object_or_404(Cooperation, id=event_id)
    event.delete()
    return redirect(request, 'events')


def edit_event(request, event_id):
    event = get_object_or_404(Cooperation, id=event_id)
    return render(request, 'event_detail.html', {'event': event})
