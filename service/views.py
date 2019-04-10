from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render, render_to_response, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json

from .models import Candidate, Jedi, Orden, Answer
from .forms import CandidateForm


def index(request):
    return render(request, 'service/index.html')


def candidate_data(request):
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
        form = CandidateForm(request.POST)
        return render(request, 'service/candidate.html', {'form': form})


@csrf_exempt
def test(request, candidate_id, planet_id):
    orden = get_object_or_404(Orden.objects.select_related('tests').prefetch_related('tests__questions'),
                              planet_id=planet_id)
    if request.method == "POST":
        answer_list = []
        for id, question in enumerate(orden.tests.questions.all()):
            answer_list.append({
                'question': question.question,
                'answer': request.POST['question_' + str(id+1)]
            })
        Answer.objects.create(candidate_id=candidate_id, answers=json.dumps(answer_list))
        return render_to_response('service/end_test.html')
    else:
        return render_to_response('service/test.html', {'orden': orden, 'candidate_id': candidate_id})


def jedi(request):
    jedi_list = Jedi.objects.order_by('name')
    # jedi_list = get_list_or_404(Jedi)
    context = {'jedi_list': jedi_list}
    return render(request, 'service/jedi.html', context)


def candidate_list(request, jedi_id, planet_id):
    candidate_list = Candidate.objects.filter(residence_planet_id=planet_id, padawan='False')
    context = {'candidate_list': candidate_list}
    return render(request, 'service/candidate_list.html', context)


def candidate_test(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        candidate.padawan = True
        candidate.save()

        title = 'О зачислении в падаваны'
        message = 'По результатам пройденного теста вы зачислены в падаваны.'
        from_mail = 'zyabrin.v@yandex.ru'
        to_mail = candidate.email
        send_mail(title, message, from_mail, [to_mail], fail_silently=False,)

        context = {'candidate': candidate}
        return render_to_response('service/end_review.html', context)

    else:
        # answer = Answer.objects.filter(candidate_id=candidate_id)
        answer = get_object_or_404(Answer, candidate_id=candidate_id)
        context = {'candidate': candidate, 'test': json.loads(answer.answers)}
        return render(request, 'service/candidate_test.html', context)

