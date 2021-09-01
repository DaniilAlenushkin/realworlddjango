from threading import Thread
from time import sleep

from django.db.models import F
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from mail.models import Subscriber, Letter
from realworlddjango.settings import env


@require_POST
def create_letters_view(request):
    emails = request.POST.getlist('email', None)
    subject = request.POST.getlist('subject', '')[0]
    text = request.POST.getlist('text', '')[0]
    if emails and subject and text:
        Letter.create_letters(emails, subject, text)

    return JsonResponse({'subscribers': Subscriber.get_objects_list()})


def send_mails(letter):
    mail = []
    subject = letter.subject.replace('[', '').replace(']', '')
    text = letter.text.replace('[', '').replace(']', '')
    mail.append(letter.mail)
    send_mail(
        subject,
        text,
        env('EMAIL_HOST_USER'),
        mail,
        fail_silently=False,
    )


def portion(part):
    for letter in part:
        th = Thread(target=send_mails, args=(letter,))
        th.start()


@require_POST
def send_letters_view(request):
    list_email_sent = Letter.objects.select_related('to').annotate(
        mail=F('to__email')
    ).filter(is_sent=False).all()

    threads_list = []
    id_list = []
    counter, step = 0, 0

    while step < list_email_sent.count():
        for i in range(50):
            if counter < list_email_sent.count():
                id_list.append(list_email_sent[counter].id)
                counter += 1

        part = list_email_sent[step:(step+50)]
        step += 50

        th = Thread(target=portion, args=(part, ))
        th.start()
        threads_list.append(th)

    for thread in threads_list:
        thread.join()

    Letter.objects.filter(id__in=id_list).update(is_sent=True)

    return JsonResponse({'subscribers': Subscriber.get_objects_list()})


def get_subscribers_view(request):
    list_emails_sent = Letter.objects.filter(is_sent=False).values_list('is_sent', flat=True)
    if list_emails_sent:
        all_emails_sent = True
    else:
        all_emails_sent = False

    return JsonResponse({
        'subscribers': Subscriber.get_objects_list(),
        'all_emails_sent': all_emails_sent,
    })
