from django.contrib import admin
from .models import OrientationRecord


@admin.register(OrientationRecord)
class OrientationRecordAdmin(admin.ModelAdmin):
    list_display = (
        "code_filiere",
        "filiere",
        "etablissement",
        "universite",
        "section_bac_nom",
        "score_2022",
        "score_2023",
        "score_2024",
        "score_2025",
    )
    list_filter = ("universite", "section_bac_nom")
    search_fields = ("filiere", "etablissement", "universite", "section_bac_nom")
