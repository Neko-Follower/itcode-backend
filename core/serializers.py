from rest_framework import serializers

from .models import Item, Category


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    characteristic = serializers.JSONField()

    class Meta:
        model = Item
        fields = ('id', 'title', 'price', 'desc', 'image', 'characteristic')


class SubCategorySerializer(serializers.ModelSerializer):
    """Serializer for lowest level category that has no children."""

    parent = serializers.SerializerMethodField(source='get_parent')

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'parent', 'image', 'characteristic']

    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.id


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category."""

    parent = serializers.SerializerMethodField(source='get_parent')
    children = serializers.SerializerMethodField(source='get_children')
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'parent', 'image', 'children', 'characteristic']

    def get_parent(self, obj):
        if obj.parent:
            temp_object = {'id': obj.parent.id, 'title': obj.parent.title}
            return temp_object

    def get_children(self, obj):
        if obj.children.exists():
            children = [child for child in obj.children.all()]
            return CategorySerializer(children, many=True).data
