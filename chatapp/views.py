from django.shortcuts import render, redirect
from .utils.chat_engine import generate_response
from django.views.decorators.http import require_POST

@require_POST
def clear_chat(request):
   
    if 'chat_history' in request.session:
        del request.session['chat_history']
    return redirect('chatapp:chatbot')  

def chatbot_view(request):
   
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    if request.method == 'POST' and 'user_input' in request.POST:
        user_input = request.POST.get('user_input')
        bot_response = generate_response(user_input)

        chat_history = request.session['chat_history']
        chat_history.append((user_input, bot_response))
        request.session['chat_history'] = chat_history

    return render(request, 'chatapp/chat.html', {
        'chat_history': request.session.get('chat_history', [])
    })