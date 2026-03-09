"""
Management command: import_csv
Usage: python manage.py import_csv [--path data/tunisie_orientation_complete.csv] [--clear]
"""
import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from orientation.models import OrientationRecord


def _safe_float(value: str):
    """Return float or None for empty / non-numeric values."""
    if value is None:
        return None
    value = value.strip().replace(",", ".")
    if value == "" or value.lower() in ("nan", "null", "none", "#n/a"):
        return None
    try:
        return float(value)
    except ValueError:
        return None


class Command(BaseCommand):
    help = "Import the orientation CSV file into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default="data/tunisie_orientation_complete.csv",
            help="Relative (to BASE_DIR) or absolute path to the CSV file.",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            default=False,
            help="Delete all existing records before importing.",
        )

    def handle(self, *args, **options):
        from django.conf import settings

        csv_path = Path(options["path"])
        if not csv_path.is_absolute():
            csv_path = settings.BASE_DIR / csv_path

        if not csv_path.exists():
            raise CommandError(f"File not found: {csv_path}")

        if options["clear"]:
            deleted, _ = OrientationRecord.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Cleared {deleted} existing records."))

        # Try UTF-8 first, fall back to latin-1
        for encoding in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
            try:
                with open(csv_path, newline="", encoding=encoding) as fh:
                    fh.read(512)
                break
            except UnicodeDecodeError:
                continue
        else:
            encoding = "latin-1"

        self.stdout.write(f"Reading '{csv_path}' with encoding '{encoding}' …")

        created_count = 0
        updated_count = 0
        error_count = 0

        with open(csv_path, newline="", encoding=encoding) as fh:
            reader = csv.DictReader(fh)
            for line_no, row in enumerate(reader, start=2):
                try:
                    code_filiere = row.get("Code_Filiere", "").strip()
                    section_bac = row.get("Section_Bac", "").strip()

                    if not code_filiere or not section_bac:
                        self.stderr.write(
                            f"Line {line_no}: skipped — missing Code_Filiere or Section_Bac."
                        )
                        error_count += 1
                        continue

                    defaults = {
                        "universite": row.get("Universite", "").strip(),
                        "etablissement": row.get("Etablissement", "").strip(),
                        "filiere": row.get("Filiere", "").strip(),
                        "section_bac_nom": row.get("Section_Bac_Nom", "").strip(),
                        "score_2022": _safe_float(row.get("Score_2022")),
                        "score_2023": _safe_float(row.get("Score_2023")),
                        "score_2024": _safe_float(row.get("Score_2024")),
                        "score_2025": _safe_float(row.get("Score_2025")),
                    }

                    _, created = OrientationRecord.objects.update_or_create(
                        code_filiere=code_filiere,
                        section_bac=section_bac,
                        defaults=defaults,
                    )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except Exception as exc:
                    self.stderr.write(f"Line {line_no}: error — {exc}")
                    error_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created: {created_count} | Updated: {updated_count} | Errors: {error_count}"
            )
        )
