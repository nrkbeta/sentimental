from django import http
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from sentimental.models import Sentence, Project
from sentimental.forms import RegistrationForm

def index(request):
    projects = Project.objects.all().order_by('-id')
    return render_to_response('sentimental/index.html', {'projects': projects})

@csrf_exempt
def register(request):
    if request.POST:
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            project = Project()
            project.name = form.cleaned_data['name']
            project.description = form.cleaned_data['description']
            project.save()
            file = form.cleaned_data['file'].read()
            for line in file.split('\n'):
                sentence = Sentence()
                sentence.project = project
                line = line.split('$$$')
                if len(line) == 1:
                    sentence.metadata = None
                    sentence.sentence = line[0]
                else:
                    sentence.metadata = line[0]
                    sentence.sentence = line[1]
                sentence.classification = None
                sentence.trained = None
                sentence.save()
            return http.HttpResponseRedirect(reverse('sentimental_project_detail', kwargs={'id': project.id}))
    else:
        form = RegistrationForm()
    return render_to_response('sentimental/register.html', {'form': form})

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    return render_to_response('sentimental/project_detail.html', {'project': project})

def trainer(request, project_id):
    project = Project.objects.get(id=project_id)
    return render_to_response('sentimental/trainer.html', {'project': project})

@csrf_exempt
def trainer_register(request):
    sentence = Sentence.objects.get(id=request.POST.get('sentence'))
    sentence.classification = int(request.POST.get('classification'))
    sentence.trained = True
    sentence.save()
    return http.HttpResponse('')

@csrf_exempt
def trainer_fetch(request):
    project = Project.objects.get(id=request.POST.get('project'))
    sentence = project.sentences.exclude(trained=True, classification__isnull=False).order_by('?')[0]
    skeleton = '''
    <div class="sentence" rel="%d">
        <p>%s</p>
        <ul>
            <li><a class="negative" href="#" rel="0">Negative</a></li>
            <li><a class="neutral" href="#" rel="1">Neutral</a></li>
            <li><a class="positive" href="#" rel="2">Positive</a></li>
        </ul>
    </div>
    ''' % (sentence.id, sentence.sentence)
    return http.HttpResponse(skeleton)