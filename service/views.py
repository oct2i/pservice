from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, redirect, get_object_or_404, get_list_or_404

import json

from .models import Candidate, Jedi, Orden, Answer
from .forms import CandidateForm


def index(request):
    return render(request, 'service/index.html')


def candidate_registration(request):
    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save()
            url = reverse('service:test', kwargs={
                'candidate_id': candidate.id,
                'planet_id': candidate.residence_planet_id
            })
            return redirect(url)
    else:
        form = CandidateForm()
        context = {'form': form}
        return render(request, 'service/candidate_registration.html', context)


@csrf_exempt
def test_trial(request, candidate_id, planet_id):
    orden = get_object_or_404(Orden.objects.select_related('tests').prefetch_related('tests__questions'),
                              planet_id=planet_id)
    if request.method == "POST":
        answer_list = []
        for id, question in enumerate(orden.tests.questions.all()):
            answer_list.append({
                'question': question.question,
                'answer': request.POST['question_' + str(id+1)]
            })
        answer_json = json.dumps(answer_list)
        Answer.objects.create(candidate_id=candidate_id, answers=answer_json)
        return render_to_response('service/test_end.html')
    else:
        context = {
            'candidate_id': candidate_id,
            'orden': orden
        }
        return render_to_response('service/test.html', context)


def jedi_list(request):
    jedi_list = Jedi.objects.order_by('name')
    context = {'jedi_list': jedi_list}
    return render(request, 'service/jedi_list.html', context)


def candidate_list(request, jedi_id, planet_id):
    candidate_list = Candidate.objects.filter(residence_planet_id=planet_id, padawan_id=None)
    context = {
        'jedi_id': jedi_id,
        'planet_id': planet_id,
        'candidate_list': candidate_list
    }
    return render(request, 'service/candidate_list.html', context)


def test_trial_results(request, jedi_id, planet_id, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        candidate.padawan_id = jedi_id
        candidate.save()
        sending_email(candidate.email)
        context = {
            'jedi_id': jedi_id,
            'planet_id': planet_id,
            'candidate': candidate
        }
        return render_to_response('service/test_results_end.html', context)
    else:
        answer = get_object_or_404(Answer, candidate_id=candidate_id)
        context = {
            'candidate': candidate,
            'test': json.loads(answer.answers)
        }
        return render(request, 'service/test_results.html', context)


def sending_email(email):
    title = 'О зачислении в падаваны'
    message = 'По результатам пройденного теста вы зачислены в падаваны.'
    from_mail = 'oct2i@yandex.ru'
    to_mail = email
    send_mail(title, message, from_mail, [to_mail], fail_silently=False, )
