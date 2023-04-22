from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import status
from .models import Cooperation, ProductExpiredNotification
from rest_framework.views import APIView
from .serializers import CooperationReadSerializer, CooperationWriteSerializer


class CooperationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cooperations = Cooperation.objects.all()
        serializer = CooperationReadSerializer(cooperations, many=True)
        return Response(serializer.data)

    def post(self, request):
        event = request.data
        serializer = CooperationWriteSerializer(data=event)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CooperationDetail(APIView):
    def get_object(self, pk):
        try:
            return Cooperation.objects.get(id=pk)
        except Cooperation.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        cooperation = self.get_object(pk)
        serializer = CooperationReadSerializer(cooperation)
        return Response(serializer.data)

    def put(self, request, pk):
        cooperation = self.get_object(pk)
        serializer = CooperationWriteSerializer(cooperation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        cooperation = self.get_object(pk)
        cooperation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




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
    notifications = ProductExpiredNotification.objects.filter(user=request.user)
    return render(request, 'events.html',
                  context={'events': Cooperation.objects.all(), 'notification_count': len(notifications)})


@login_required
def join_event(request, event_id):
    event = get_object_or_404(Cooperation, id=event_id)
    print(event.participants.all())
    if request.user not in event.participants.all():
        event.participants.add(request.user)
    print(event.participants.all())
    return redirect('event-detail', event_id)


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Cooperation, id=event_id)
    return render(request, 'event_detail.html', {'event': event,
                                                 'is_joined': event.participants.filter(id=request.user.id).exists()})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Cooperation, id=event_id)
    event.delete()
    return redirect('events')


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Cooperation, id=event_id)
    if request.user.id == event.creator.id:
        pass
    return render(request, 'event_detail.html', {'event': event})


@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Cooperation, id=event_id)
    event.participants.remove(request.user)
    event.save()
    return redirect('event-detail', event_id)


@login_required
def delete_participant(request, participant_id):
    pass


@never_cache
def refresh_events(request):
    events = Cooperation.objects.all().order_by('date')
    return render(request,'events_block.html', context={'events': events})



