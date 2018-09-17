from django.shortcuts import render
from main.models import Review, Home, About, Team
from main.forms import ContactForm, ReviewForm
from django.core.mail import EmailMessage


def home(request):
    h = Home.objects.get(id=1)
    return render(request=request, template_name='main/home.html', context={'home': h})


def about(request):
    about = About.objects.get(id=1)
    reviews = Review.objects.filter(published=True)
    staff = Team.objects.filter()[0:3]
    return render(request=request, template_name='main/about.html', context={
        'about': about,
        'reviews': reviews,
        'staff': staff
    })


def delivery(request):
    return render(request=request, template_name='main/delivery.html')


def contact(request):
    config = Home.objects.get(id=1)
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            c = form.save()
            c.send_client_email()
            c.send_admin_emails()
            return render(request=request, template_name='main/contacted.html', context={
                'config': config,
                'form': form
            })
    else:
        form = ContactForm()
    return render(request=request, template_name='main/contact.html', context={
        'config': config,
        'form': form
    })
