from sentimental.models import Sentence, Project
from reverend.thomas import Bayes


class Guesser(object):
    
    def __init__(self, project):
        self.project = project
        self.bayes = Bayes()
        self._train()
        self.data = []
        self.best = []
    
    def _train(self):
        for sentence in self.project.classified():
            self.bayes.train(sentence.get_classification(), sentence.sentence)
    
    def guess(self):
        for sentence in self.project.to_classify():
            data = {'sentence_id': sentence.id}
            data['guesses'] = self.bayes.guess(sentence.sentence)
            self.data.append(data)
        return self.data
    
    def best_matches(self):
        if not self.data: return []
        for matches in self.data:
            try:
                matches['guesses'] = sorted(matches['guesses'], key=lambda x:x[1], reverse=True)[0]
            except:
                matches['guesses'] = (None, None)
            self.best.append(matches)
        return self.best
            
