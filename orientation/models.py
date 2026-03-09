from django.db import models


class OrientationRecord(models.Model):
    code_filiere = models.CharField(max_length=64, verbose_name="Code Filière")
    universite = models.CharField(max_length=255, verbose_name="Université")
    etablissement = models.CharField(max_length=255, verbose_name="Établissement")
    filiere = models.CharField(max_length=255, verbose_name="Filière")
    section_bac = models.CharField(max_length=10, verbose_name="Section Bac (code)")
    section_bac_nom = models.CharField(max_length=255, verbose_name="Section Bac (nom)")
    score_2022 = models.FloatField(null=True, blank=True, verbose_name="Score 2022")
    score_2023 = models.FloatField(null=True, blank=True, verbose_name="Score 2023")
    score_2024 = models.FloatField(null=True, blank=True, verbose_name="Score 2024")
    score_2025 = models.FloatField(null=True, blank=True, verbose_name="Score 2025")

    class Meta:
        verbose_name = "Dossier d'orientation"
        verbose_name_plural = "Dossiers d'orientation"
        unique_together = ("code_filiere", "section_bac")
        ordering = ["universite", "etablissement", "filiere"]

    def __str__(self):
        return f"{self.filiere} — {self.etablissement} ({self.section_bac_nom})"
