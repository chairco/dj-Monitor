# radars/search_indexs.py
from haystack import indexes

from django_q.tasks import Task


class TaskIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    task = indexes.CharField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    #result = indexes.CharField(model_attr='result')
    #group = indexes.CharField(model_attr='group')
    args = indexes.CharField(model_attr='args')
    started = indexes.DateTimeField(model_attr='started')
    stopped = indexes.DateTimeField(model_attr='stopped')
    success = indexes.BooleanField(model_attr='success')

    def get_model(self):
        return Task

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


