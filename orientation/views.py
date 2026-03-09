from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import OrientationRecord
from .serializers import OrientationRecordSerializer


class OrientationRecordViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API read-only endpoint for orientation records.

    Filtering examples:
      /api/orientations/?section_bac_nom=Mathématiques
      /api/orientations/?universite=Université+de+Tunis
      /api/orientations/?search=informatique
    """

    queryset = OrientationRecord.objects.all()
    serializer_class = OrientationRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Exact-match filters
    filterset_fields = {
        "section_bac_nom": ["exact", "icontains"],
        "section_bac": ["exact"],
        "universite": ["exact", "icontains"],
        "etablissement": ["exact", "icontains"],
        "filiere": ["exact", "icontains"],
        "code_filiere": ["exact"],
    }

    # Full-text search across these fields
    search_fields = ["filiere", "etablissement", "universite", "section_bac_nom"]

    # Allow sorting
    ordering_fields = [
        "universite",
        "etablissement",
        "filiere",
        "score_2022",
        "score_2023",
        "score_2024",
        "score_2025",
    ]
