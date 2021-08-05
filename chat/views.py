from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
# from googletrans import Translator, LANGCODES
from deep_translator import GoogleTranslator


def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    language = request.GET.get('language')
    #accesam baza de date pt detalii
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
        'language': language
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    language = request.POST['language']
#verificam daca exista camera de chat sau daca trebuie creata una noua
    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username+'&language='+language)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username+'&language='+language)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    language = request.GET.get('language')
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    # print(messages.values('value'))
    # if language in LANGCODES.keys():
    for m in messages:
        # if m.translated:
        #     continue

        m.translated = True
        # translator = Translator()
        old_message = str(m.value)
        # trans = translator.translate(old_message, dest=LANGCODES[language])
        trans = GoogleTranslator(source='auto', target=language).translate(old_message)
        # print('original:', old_message, 'tradus:', trans)
        m.value = trans
        m.save()

    return JsonResponse({"messages":list(messages.values())})