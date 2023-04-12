from django.shortcuts import render

def home_screen_view(request):

    context = {}
    context['some_string'] = "this is some string that I'm passing to the view"

    return render(request, "home/home.html", context)
