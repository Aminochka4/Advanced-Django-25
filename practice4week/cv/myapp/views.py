from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm
from .models import CV
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

def success_view(request):
    return render(request, 'success.html')


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def share_cv_email(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)

    if request.method == "POST":
        recipient_email = request.POST.get('email')

        if recipient_email:
            send_mail(
                subject=f"{cv.name}'s CV",
                message=f"Посмотри {cv.name}'s CV: {request.build_absolute_uri(cv.profile_picture.url)}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient_email]
            )
            messages.success(request, "Резюме отправлено!")
        else:
            messages.error(request, "Введите email!")

        return redirect('cv_list')
    
    return render(request, 'share_email.html', {'cv': cv})
