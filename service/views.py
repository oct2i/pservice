from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render, render_to_response, redirect
from django.urls import reverse

from .models import Candidate, Jedi, Orden
from .forms import CandidateForm


def index(request):
    return HttpResponse("Кто ты?")


def candidate(request):
    return HttpResponse('Ты кандидат')


def candidate_data(request):
    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save()
            url = reverse('service:test_list', kwargs={
                'candidate_id': candidate.id,
                'planet_id': candidate.residence_planet_id
            })
            return redirect(url)
    else:
        form = CandidateForm(request.POST)
        return render(request, 'service/candidate.html', {'form': form})


def test(request, candidate_id, planet_id):
    orden = get_object_or_404(Orden.objects.select_related('tests').prefetch_related('tests__questions'),
                              planet_id=planet_id)
    if request.method == "POST":
        print(request)
    else:
        return render_to_response('service/test.html', {'orden': orden})





# def candidate_data(request):
    # return render_to_response('service/candidate.html')





def jedi(request):
    jedi_list = Jedi.objects.order_by('name')
    # jedi_list = get_list_or_404(Jedi)
    context = {'jedi_list': jedi_list}
    return render(request, 'service/jedi.html', context)


def detail(request, jedi_id):
    return HttpResponse("You're voting on question %s." % jedi_id)


