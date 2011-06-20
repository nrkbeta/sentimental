from django.db import models

class NotClassifiedError(Exception):
    pass

class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    has_ran = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class Sentence(models.Model):
    project = models.ForeignKey(Project, related_name="sentences")
    metadata = models.TextField(blank=True, null=True)
    sentence = models.TextField()
    classification = models.CharField(blank=True, max_length=5, null=True)
    trained = models.NullBooleanField(default=False, null=True, blank=True)
    
    def __unicode__(self):
        return self.sentence[:100]
    
    def is_positive(self):
        if self.classification == None:
            raise NotClassifiedError()
        if self.classification == 0:
            return False # Negative
        if self.classification == 1:
            return True # Positive
        if self.classification == 2:
            return None # Neutral