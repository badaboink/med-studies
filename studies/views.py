from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from studies.models import Item, ItemReferentiel, Margot, Referentiel
from studies.serializers import ItemSerializer, MargotSerializer, ReferentielSerializer

class ItemView(APIView):
    def get(self, request):
        items = Item.objects.all().order_by("id")
        serializer = ItemSerializer(items, many=True)
        checked = items.filter(status=True).count()
        total = items.count()
        return Response({
            "items": serializer.data,
            "checked": checked,
            "total": total,
        }, status=status.HTTP_200_OK)

class MargotView(ModelViewSet):
    queryset = Margot.objects.all()
    serializer_class = MargotSerializer

class MargotViewSet(ModelViewSet):

    def list(self, request):
        queryset = Margot.objects.all()
        serializer = MargotSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            instance = Margot.objects.get(pk=pk)
        except Margot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MargotSerializer(instance)
        return Response(serializer.data)


class ReferentielView(APIView):
    def get(self, request):
        refs = Referentiel.objects.all().prefetch_related("item_referentiels__item")
        serializer = ReferentielSerializer(refs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
         
class ItemDetailView(APIView):
    def patch(self, request, item_id): 
        try:
            item = Item.objects.get(id=item_id) 
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        new_status = request.data.get("status")
        if serializer.is_valid():
            if new_status is not None:
                ItemReferentiel.objects.filter(
                    item_id=item_id
                ).update(
                    status=new_status
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReferentielItemStatusView(APIView):

    def patch(self, request, ref_id, item_id):
        try:
            relation = ItemReferentiel.objects.get(
                ref_id=ref_id,
                item_id=item_id
            )
        except ItemReferentiel.DoesNotExist:
            return Response(
                {"error": "ItemReferentiel relationship not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if "status" in request.data:
            relation.status = request.data["status"]
            relation.save(update_fields=["status"])

            relationships = ItemReferentiel.objects.filter(item_id=item_id)
            all_done = not relationships.filter(status=False).exists()

            item = Item.objects.get(id=item_id)
            item.status = all_done
            item.save()


        return Response({"item_id": relation.item_id, "ref_id": relation.ref_id,"status": relation.status})
