from django.db import models

class NotClassifiedError(Exception):
    pass


class Classification(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    has_ran = models.BooleanField(default=False)
    classifications = models.ManyToManyField(Classification)
    
    def __unicode__(self):
        return self.name
    
    def classified(self):
        return self.sentences.filter(trained=True, classification__isnull=False)
    
    def to_classify(self):
        return self.sentences.exclude(trained=True, classification__isnull=False)


class Sentence(models.Model):
    project = models.ForeignKey(Project, related_name="sentences")
    metadata = models.TextField(blank=True, null=True)
    sentence = models.TextField()
    classification = models.ForeignKey(Classification, blank=True, null=True)
    trained = models.NullBooleanField(default=False, null=True, blank=True)
    guessed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.sentence[:100]
    
    def get_classification(self):
        return self.classification.name
        