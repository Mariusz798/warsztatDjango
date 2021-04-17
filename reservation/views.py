import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from reservation.models import ConferenceRoom, ReservationModel


def index(request):
    return render(request, 'base.html')


class AddRoom(View):

    def get(self, request):
        return render(request, 'form_to_add_room.html')

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity', 0)
        projector = bool(request.POST.get('projector'))
        if not name:
            return render(request, 'msg.html', {'msg': 'Nazwa sali nie została podana'})
        if int(capacity) < 0:
            return render(request, 'msg.html', {'msg': 'Pojemność sali jest niepoprawna'})
        if ConferenceRoom.objects.filter(name=name):
            return render(request, 'msg.html', {'msg': 'Sala o takiej nazwie już istnieje w bazie danych'})
        cr = ConferenceRoom(name=name, capacity=capacity, projector_availability=projector)
        cr.save()
        return redirect('http://127.0.0.1:8000/')


def rooms_view(request):
    try:
        rooms = ConferenceRoom.objects.all()
        return render(request, 'rooms_view.html', {'rooms': rooms})
    except:
        return render(request, 'msg.html', {'msg': 'Brak dostępnych sal'})


class DeleteRoom(View):

    def get(self, request):
        rooms = ConferenceRoom.objects.all()
        return render(request, 'form_to_del_room.html', {'rooms': rooms})

    def post(self, request):
        try:
            room = request.POST.get('id_room')
            room.delete()
            return redirect('/rooms_view/', 'msg.html', {'msg': 'Sala została usunięta'})
        except:
            return render(request, 'msg.html', {'msg': 'Nie znaleziono sali o takim id'})


class ModifyRoom(View):

    def get(self, request, id):
        room = ConferenceRoom.objects.get(pk=id)
        return render(request, 'change_room.html', {'room': room})

    def post(self, request, id):
        if not request.POST.get('name'):
            return render(request, 'msg.html', {'msg': 'Nazwa sali nie została podana'})
        if int(request.POST.get('capacity', 0)) < 0:
            return render(request, 'msg.html', {'msg': 'Pojemność sali jest niepoprawna'})
        # if ConferenceRoom.objects.filter(name=request.POST.get('name')):
        #     return render(request, 'msg.html', {'msg': 'Sala o takiej nazwie już istnieje w bazie danych'})
        room = ConferenceRoom.objects.get(pk=id)
        room.name = request.POST.get('name')
        room.capacity = request.POST.get('capacity', 0)
        room.projector_availability = bool(request.POST.get('projector'))
        room.save()
        return redirect('/rooms_view/')


class ReservationRoom(View):

    def get(self, request, id):
        return render(request, 'form_to_reservation_room.html', {'room':ConferenceRoom.objects.get(pk=id)})

    def post(self, request, id):
        room = ConferenceRoom.objects.get(pk=id)
        now_date = datetime.date.today()
        date = request.POST.get('date')
        comment = request.POST.get('comment')
        if ReservationModel.objects.filter(room=room, date=date):
            return render(request, 'msg.html', {'msg': f'Sala {room.name} jest już zarezerwowana na ten dzień'})
        if date < str(now_date):
            return render(request, 'msg.html', {'msg': f'{date} to przeszłość'})
        r = ReservationModel()
        r.date = date
        r.room = room
        r.comment = comment
        r.save()
        return redirect('/rooms_view/', 'msg.html', {'msg':'Rezerwacja sali została zapisana'})


def detail_room_view(request, id):
    room = ConferenceRoom.objects.get(pk=id)
    return render(request, 'detail_room_view.html', {'room':room})