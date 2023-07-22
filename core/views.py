from django.db.models import Max
from django.db.models.fields.json import KT
from rest_framework import viewsets
from core import models
from core.serializers import ItemSerializer, CategorySerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = models.Item.objects.all().order_by('id')
    serializer_class = ItemSerializer

    def get_queryset(self):
        objects = models.Item.objects.all()
        query_params = self.request.query_params
        print(objects.annotate(max_cores=KT('characteristic__cores')).aggregate(max_cores=Max('max_cores')))

        print(query_params)
        offset = 0
        limit = None
        filter_dict = {}
        for param in query_params:
            if param == 'categoryId':
                objects = objects.filter(category=int(query_params[param]))
            elif param == 'offset':
                offset = int(query_params['offset'])
            elif param == 'limit':
                limit = int(query_params['limit'])
            else:
                if query_params[param].isdigit():
                    filter_dict['characteristic__' + param] = int(query_params[param])
                elif query_params[param].replace(".", "", 1).isdigit():
                    filter_dict['characteristic__' + param] = float(query_params[param])
                else:
                    filter_dict['characteristic__' + param + '__in'] = query_params[param].split(',')
        if filter_dict:
            objects = objects.filter(**filter_dict)
        objects = objects[offset:]
        objects = objects[:limit]
        return objects


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all().order_by('id')
    serializer_class = CategorySerializer

    def get_queryset(self):
        query_params = self.request.query_params
        if 'id' in query_params:
            return models.Category.objects.get(pk=query_params['id']).get_children()
        return models.Category.objects.all()
