import json 

from django import http
from django.conf import settings
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from sentimental.models import Sentence, Project, Classification
from sentimental.forms import RegistrationForm

def index(request):
    projects = Project.objects.all().order_by('-id')
    return render_to_response('sentimental/index.html', {'projects': projects})

@csrf_exempt
def register(request):
    if not getattr(settings, 'ALLOW_UPLOADS', False):
        return http.HttpResponse('Uploads not allowed at this time')
    if request.POST:
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            project = Project()
            project.name = form.cleaned_data['name']
            project.description = form.cleaned_data['description']
            project.save()
            for choice in request.POST.getlist('choice'):
                classification = Classification()
                classification.name = choice
                classification.save()
                project.classifications.add(classification)
            project.save()
            file = form.cleaned_data['file'].read()
            for line in file.split('\n'):
                sentence = Sentence()
                sentence.project = project
                sentence.guessed = False
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
            return http.HttpResponseRedirect(reverse('sentimental_project_detail', kwargs={'project_id': project.id}))
    else:
        form = RegistrationForm()
    return render_to_response('sentimental/register.html', {'form': form})

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    return render_to_response('sentimental/project_detail.html', {'project': project, 'trained': project.sentences.filter(trained=True, classification__isnull=False).count()})

def project_classifications(request, project_id):
    project = Project.objects.get(id=project_id)
    return render_to_response('sentimental/project_classifications.html', {'project': project})

def trainer(request, project_id):
    project = Project.objects.get(id=project_id)
    return render_to_response('sentimental/trainer.html', {'project': project})

@csrf_exempt
def trainer_register(request):
    sentence = Sentence.objects.get(id=request.POST.get('sentence'))
    sentence.classification_id = int(request.POST.get('classification'))
    sentence.trained = True
    sentence.save()
    return http.HttpResponse('')

@csrf_exempt
def trainer_fetch(request):
    project = Project.objects.get(id=request.POST.get('project'))
    sentence = project.sentences.exclude(trained=True, classification__isnull=False).order_by('?')[0]
    choices = []
    for n, choice in enumerate(project.classifications.all()):
        choices.append('<li><a class="choice_%d" href="#" rel="%d">%s</a></li>' % (n+1, choice.id, choice.name))
    
    meta = json.loads(sentence.metadata)
    mk = ''
    for key, value in meta.values():
        mk += '%s: %s -' % (key, value)
    mk = mk[:len(mk-2)]
    skeleton = '''
    <div class="sentence" rel="%d">
        <p>%s</p>
        <p class="meta">%s</p>
        <ul>
            %s
            <li><a class="close" href="#" rel="close" title="Next">I don't know</a></li>
        </ul>
    </div>
    ''' % (sentence.id, sentence.sentence, mk, "\n".join(choices))
    return http.HttpResponse(skeleton)