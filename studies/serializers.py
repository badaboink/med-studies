from rest_framework import serializers
from studies.models import ItemReferentiel, Item, Margot, Referentiel

class ItemReferentielSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ref.id")
    title = serializers.CharField(source="ref.title")
    short = serializers.CharField(source="ref.short")

    class Meta:
        model = ItemReferentiel
        fields = ["id", "title", "short", "status"]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "title", "status"]

class MargotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Margot
        fields = '__all__'
        
class ReferentielItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="item.id")
    title = serializers.CharField(source="item.title")

    class Meta:
        model = ItemReferentiel
        fields = ["id", "title", "status"]

class ReferentielSerializer(serializers.ModelSerializer):

    count = serializers.SerializerMethodField()
    done = serializers.SerializerMethodField()

    items = ReferentielItemSerializer(
        source="item_referentiels",
        many=True
    )

    class Meta:
        model = Referentiel
        fields = ["id","title","short","count","done","items"]

    def get_count(self, obj):
        return obj.item_referentiels.count()

    def get_done(self, obj):
        return obj.item_referentiels.filter(status=True).count()