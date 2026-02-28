#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extraction des données RÉELLES depuis les PDFs officiels de orientation.tn
- SD_TN_2025.pdf : Scores du dernier orienté 2025 (par section bac)
- sd_par_typbac_22_23_24.pdf : Scores 2022-2023-2024 (par type bac)

La clé composite est (Code_Filiere, Section_Bac).
"""

import pdfplumber
import re
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "real_data")

# ============================================================
# ARABIC SECTION BAC DETECTION
# ============================================================

# Order matters: check longer/more specific patterns first
SECTION_PATTERNS = [
    ("علوم تجريبية", "S", "Sciences Expérimentales"),
    ("تجريبية",      "S", "Sciences Expérimentales"),
    ("العلوم التقنية","T", "Sciences Techniques"),
    ("التقنية",      "T", "Sciences Techniques"),
    ("تقنية",        "T", "Sciences Techniques"),
    ("علوم الإعلامية","I", "Sciences Informatiques"),
    ("الإعلامية",    "I", "Sciences Informatiques"),
    ("إعلامية",      "I", "Sciences Informatiques"),
    ("إقتصاد وتصرف", "E", "Économie et Gestion"),
    ("اقتصاد وتصرف", "E", "Économie et Gestion"),
    ("إقتصاد",       "E", "Économie et Gestion"),
    ("اقتصاد",       "E", "Économie et Gestion"),
    ("رياضيات",      "M", "Mathématiques"),
    ("رياضة",        "SP", "Sport"),
    ("آداب",         "L", "Lettres"),
]

# Reversed/mangled forms that appear in pdfplumber output
SECTION_PATTERNS_MANGLED = [
    ("ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ",  "S"),
    ("ﺔﻴﺒﻳﺮﺠﺗ",       "S"),
    ("ﺔﻴﻨﻘﺘﻟﺍ ﻡﻮﻠﻌﻟﺍ", "T"),
    ("ﺔﻴﻨﻘﺘﻟﺍ",       "T"),
    ("ﺔﻴﻣﻼﻋﻹﺍ ﻡﻮﻠﻋ",  "I"),
    ("ﺔﻴﻣﻼﻋﻹﺍ",       "I"),
    ("ﻑﺮﺼﺗﻭ ﺩﺎﺼﺘﻗﺇ",  "E"),
    ("ﺩﺎﺼﺘﻗﺇ",        "E"),
    ("ﺕﺎﻴﺿﺎﻳﺭ",       "M"),
    ("ﺔﺿﺎﻳﺭ",         "SP"),
    ("ﺏﺍﺩﺁ",          "L"),
]

# For page-level section detection in multi-year PDF (exact match)
SECTION_PAGE_MAP = {
    "آداب":           ("L",  "Lettres"),
    "ﺏﺍﺩﺁ":           ("L",  "Lettres"),
    "رياضيات":        ("M",  "Mathématiques"),
    "ﺕﺎﻴﺿﺎﻳﺭ":        ("M",  "Mathématiques"),
    "علوم تجريبية":   ("S",  "Sciences Expérimentales"),
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ":   ("S",  "Sciences Expérimentales"),
    "العلوم التقنية":  ("T",  "Sciences Techniques"),
    "ﺔﻴﻨﻘﺘﻟﺍ ﻡﻮﻠﻌﻟﺍ":  ("T",  "Sciences Techniques"),
    "علوم الإعلامية":  ("I",  "Sciences Informatiques"),
    "ﺔﻴﻣﻼﻋﻹﺍ ﻡﻮﻠﻋ":   ("I",  "Sciences Informatiques"),
    "إقتصاد وتصرف":   ("E",  "Économie et Gestion"),
    "اقتصاد وتصرف":   ("E",  "Économie et Gestion"),
    "ﻑﺮﺼﺗﻭ ﺩﺎﺼﺘﻗﺇ":   ("E",  "Économie et Gestion"),
    "رياضة":          ("SP", "Sport"),
    "ﺔﺿﺎﻳﺭ":          ("SP", "Sport"),
}

SECTION_NAMES = {
    "M":  "Mathématiques",
    "S":  "Sciences Expérimentales",
    "T":  "Sciences Techniques",
    "I":  "Sciences Informatiques",
    "E":  "Économie et Gestion",
    "L":  "Lettres",
    "SP": "Sport",
}

# ============================================================
# UNIVERSITY DETECTION
# ============================================================

# Sorted by length desc to match longer patterns first
UNIV_PATTERNS = [
    ("جامعة تونس المنار",  "Université de Tunis El Manar"),
    ("ﺭﺎﻨﻤﻟﺍ ﺲﻧﻮﺗ ﺔﻌﻣﺎﺟ",  "Université de Tunis El Manar"),
    ("ﺭﺎﻨﻤﻟﺍ ﺲﻧﻮﺗ",         "Université de Tunis El Manar"),
    ("جامعة تونس",          "Université de Tunis"),
    ("ﺲﻧﻮﺗ ﺔﻌﻣﺎﺟ",          "Université de Tunis"),
    ("جامعة منوبة",          "Université de La Manouba"),
    ("ﺔﺑﻮﻨﻣ ﺔﻌﻣﺎﺟ",          "Université de La Manouba"),
    ("جامعة قرطاج",          "Université de Carthage"),
    ("ﺝﺎﻃﺮﻗ ﺔﻌﻣﺎﺟ",          "Université de Carthage"),
    ("جامعة سوسة",           "Université de Sousse"),
    ("ﺔﺳﻮﺳ ﺔﻌﻣﺎﺟ",           "Université de Sousse"),
    ("جامعة المنستير",       "Université de Monastir"),
    ("ﺮﻴﺘﺴﻨﻤﻟﺍ ﺔﻌﻣﺎﺟ",       "Université de Monastir"),
    ("جامعة صفاقس",          "Université de Sfax"),
    ("ﺲﻗﺎﻔﺻ ﺔﻌﻣﺎﺟ",          "Université de Sfax"),
    ("جامعة جندوبة",         "Université de Jendouba"),
    ("ﺔﺑﻭﺪﻨﺟ ﺔﻌﻣﺎﺟ",         "Université de Jendouba"),
    ("جامعة القيروان",       "Université de Kairouan"),
    ("ﻥﺍﻭﺮﻴﻘﻟﺍ ﺔﻌﻣﺎﺟ",       "Université de Kairouan"),
    ("جامعة قابس",           "Université de Gabès"),
    ("ﺲﺑﺎﻗ ﺔﻌﻣﺎﺟ",           "Université de Gabès"),
    ("جامعة قفصة",           "Université de Gafsa"),
    ("ﺔﺼﻔﻗ ﺔﻌﻣﺎﺟ",           "Université de Gafsa"),
    ("جامعة الزيتونة",       "Université Ezzitouna"),
    ("ﺔﻧﻮﺘﻳﺰﻟﺍ ﺔﻌﻣﺎﺟ",       "Université Ezzitouna"),
]


def detect_section(text):
    """Detect bac section from Arabic text. Returns code or None."""
    # Try standard Arabic
    for pattern, code, _ in SECTION_PATTERNS:
        if pattern in text:
            return code
    # Try mangled forms from pdfplumber
    for pattern, code in SECTION_PATTERNS_MANGLED:
        if pattern in text:
            return code
    return None


def detect_university(text):
    """Try to match a university from line text."""
    for ar, fr in UNIV_PATTERNS:
        if ar in text:
            return fr
    return None


def is_ignorable(line):
    """Check if a line is a page header/footer/column-header."""
    # Page title
    if any(kw in line for kw in [
        "ﺔﻴﺴﻧﻮﺗ ﺎﻳﺭﻮﻟﺎﻜﺑ", "بكالوريا تونسية",
        "ﺎﻬﺑﺎﻌﻴﺘﺳﺍ ﺔﻗﺎﻃ", "طاقة استيعابها",
        "ﺓﺭﺍﺯﻭ", "وزارة",
        "ﻲﻤﻠﻌﻟﺍ ﺚﺤﺒﻟﺍ", "البحث العلمي",
        "ﺓﺮﻴﺧﻷﺍ ﺙﻼﺜﻟﺍ",
    ]):
        return True
    # Column header
    if ("ﺎﻳﺭﻮﻟﺎﻛﺎﺒﻟﺍ" in line and "ﺔﺒﻌﺸﻟﺍ" in line) or \
       ("الباكالوريا" in line and "الشعبة" in line):
        return True
    # Page footer
    if re.match(r'^\s*2025\s+\d+\s*-\s*82\s*$', line):
        return True
    if re.search(r'\d+\s*/\s*162', line):
        return True
    # Year header
    if re.match(r'^\s*2024\s+2023\s+2022', line):
        return True
    if "2024/2023/2022" in line:
        return True
    # Disclaimer
    if "ﻉﻮﻤﺠﻤﻟﺍ ﺔﻧﺎﺧ" in line or "المجموع" in line and "فارغة" in line:
        return True
    if "ﻲﺒﻳﺮﻘﺗ ﺮﺷﺆﻤﻛ" in line or "كمؤشر تقريبي" in line:
        return True
    return False


def get_trailing_code(line):
    """Extract 4-5 digit code at end of line."""
    m = re.search(r'\b(\d{4,5})\s*$', line)
    return m.group(1) if m else None


def get_leading_number(line):
    """Extract the first float number."""
    m = re.match(r'^\s*(\d+\.?\d*)\s', line)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None
    return None


# ============================================================
# PARSE SD_TN_2025.pdf
# ============================================================

def parse_2025():
    """
    Returns list of dicts: {code, section, score_2025, filiere_ar, univ, etab_ar}
    Each row is one (filière, section) combination.
    """
    pdf_path = os.path.join(PDF_DIR, "SD_TN_2025.pdf")
    if not os.path.exists(pdf_path):
        print(f"[ERREUR] {pdf_path} introuvable")
        return []

    print("Parsing SD_TN_2025.pdf ...")
    pdf = pdfplumber.open(pdf_path)

    records = []
    cur_univ = ""
    cur_etab = ""
    cur_code = ""
    cur_filiere = ""

    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue

        for line in text.split('\n'):
            line = line.strip()
            if not line or is_ignorable(line):
                continue

            # University?
            univ = detect_university(line)
            if univ and not re.search(r'\d{2,}\.\d', line):
                cur_univ = univ
                continue

            # Leading score?
            score = get_leading_number(line)
            if score is None:
                # No number -> establishment name
                if len(line) > 5:
                    cur_etab = line
                continue

            # Skip unrealistic scores
            if score < 40 or score > 420:
                continue

            code = get_trailing_code(line)
            # Detect section
            sec = detect_section(line)

            if code:
                # Header row: Score Section Filière Code
                cur_code = code
                # Extract Arabic text (everything between score and code)
                body = re.sub(r'^\s*\d+\.?\d*\s*', '', line)
                body = re.sub(r'\s*\d{4,5}\s*$', '', body).strip()
                cur_filiere = body

                if sec:
                    records.append({
                        "code": code, "section": sec,
                        "score_2025": score,
                        "filiere_ar": cur_filiere,
                        "univ": cur_univ, "etab_ar": cur_etab,
                    })
            else:
                # Continuation: Score Section
                if sec and cur_code:
                    records.append({
                        "code": cur_code, "section": sec,
                        "score_2025": score,
                        "filiere_ar": cur_filiere,
                        "univ": cur_univ, "etab_ar": cur_etab,
                    })

    pdf.close()
    print(f"  -> {len(records)} rows extracted (2025)")
    return records


# ============================================================
# PARSE sd_par_typbac_22_23_24.pdf
# ============================================================

def parse_multiyear():
    """
    Returns list of dicts: {code, section, score_2022, score_2023, score_2024,
                            filiere_ar, univ, etab_ar}
    """
    pdf_path = os.path.join(PDF_DIR, "sd_par_typbac_22_23_24.pdf")
    if not os.path.exists(pdf_path):
        print(f"[ERREUR] {pdf_path} introuvable")
        return []

    print("Parsing sd_par_typbac_22_23_24.pdf ...")
    pdf = pdfplumber.open(pdf_path)

    records = []
    cur_section = ""
    cur_univ = ""
    cur_etab = ""

    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue

        lines = text.split('\n')

        # Detect page-level section from early lines
        for ln in lines[:8]:
            ln_s = ln.strip()
            for key, (code, _) in SECTION_PAGE_MAP.items():
                if ln_s == key:
                    cur_section = code
                    break

        for line in lines:
            line = line.strip()
            if not line or is_ignorable(line):
                continue

            # University?
            univ = detect_university(line)
            if univ and not re.search(r'\d{2,}\.\d', line):
                cur_univ = univ
                continue

            # Must have code at end
            code = get_trailing_code(line)
            if not code:
                score = get_leading_number(line)
                if score is None and len(line) > 5:
                    cur_etab = line
                continue

            # Extract all numbers
            nums = re.findall(r'(\d+\.?\d*)', line)
            if len(nums) < 4:
                continue  # need 3 scores + 1 code

            try:
                s2024 = float(nums[0])
                s2023 = float(nums[1])
                s2022 = float(nums[2])
            except (ValueError, IndexError):
                continue

            if any(s < 40 or s > 420 for s in [s2024, s2023, s2022]):
                continue

            body = re.sub(r'^\s*[\d.\s]+', '', line)  # remove leading numbers
            body = re.sub(r'\s*\d{4,5}\s*$', '', body).strip()  # remove code

            records.append({
                "code": code, "section": cur_section,
                "score_2022": s2022, "score_2023": s2023, "score_2024": s2024,
                "filiere_ar": body,
                "univ": cur_univ, "etab_ar": cur_etab,
            })

    pdf.close()
    print(f"  -> {len(records)} rows extracted (2022-2024)")
    return records


# ============================================================
# MERGE & BUILD CSV
# ============================================================

def main():
    data_2025 = parse_2025()
    data_multi = parse_multiyear()

    merged = {}

    for r in data_multi:
        key = (r["code"], r["section"])
        merged[key] = {
            "Code_Filiere":     r["code"],
            "Section_Bac":      r["section"],
            "Section_Bac_Nom":  SECTION_NAMES.get(r["section"], r["section"]),
            "Filiere_AR":       r["filiere_ar"],
            "Universite":       r["univ"],
            "Etablissement_AR": r["etab_ar"],
            "Score_2022":       r["score_2022"],
            "Score_2023":       r["score_2023"],
            "Score_2024":       r["score_2024"],
            "Score_2025":       "",
        }

    m_count, n_count = 0, 0
    for r in data_2025:
        key = (r["code"], r["section"])
        if key in merged:
            merged[key]["Score_2025"] = r["score_2025"]
            if not merged[key]["Universite"]:
                merged[key]["Universite"] = r["univ"]
            if not merged[key]["Etablissement_AR"]:
                merged[key]["Etablissement_AR"] = r["etab_ar"]
            m_count += 1
        else:
            merged[key] = {
                "Code_Filiere":     r["code"],
                "Section_Bac":      r["section"],
                "Section_Bac_Nom":  SECTION_NAMES.get(r["section"], r["section"]),
                "Filiere_AR":       r["filiere_ar"],
                "Universite":       r["univ"],
                "Etablissement_AR": r["etab_ar"],
                "Score_2022":       "",
                "Score_2023":       "",
                "Score_2024":       "",
                "Score_2025":       r["score_2025"],
            }
            n_count += 1

    print(f"\n--- MERGE ---")
    print(f"  2025 matched: {m_count}")
    print(f"  2025 new:     {n_count}")
    print(f"  Total:        {len(merged)}")

    sec_order = {"L": 0, "M": 1, "S": 2, "T": 3, "I": 4, "E": 5, "SP": 6}
    rows = sorted(merged.values(),
                  key=lambda r: (r["Code_Filiere"], sec_order.get(r["Section_Bac"], 99)))

    out = os.path.join(BASE_DIR, "tunisie_orientation_complete.csv")
    cols = [
        "Code_Filiere", "Universite", "Etablissement_AR", "Filiere_AR",
        "Section_Bac", "Section_Bac_Nom",
        "Score_2022", "Score_2023", "Score_2024", "Score_2025",
    ]

    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    # --- Stats ---
    h22 = sum(1 for r in rows if r["Score_2022"])
    h23 = sum(1 for r in rows if r["Score_2023"])
    h24 = sum(1 for r in rows if r["Score_2024"])
    h25 = sum(1 for r in rows if r["Score_2025"])
    univs = sorted(set(r["Universite"] for r in rows if r["Universite"]))
    secs  = sorted(set(r["Section_Bac"] for r in rows if r["Section_Bac"]))
    codes = set(r["Code_Filiere"] for r in rows)

    print(f"\n{'='*60}")
    print(f"  DATASET RÉEL GÉNÉRÉ")
    print(f"{'='*60}")
    print(f"  Fichier : {out}")
    print(f"  Lignes  : {len(rows)}")
    print(f"  Codes   : {len(codes)} filières uniques")
    print(f"  Score 2022: {h22} | 2023: {h23} | 2024: {h24} | 2025: {h25}")
    print(f"  Universités ({len(univs)}): {univs}")
    print(f"  Sections: {secs}")
    print(f"\n  Aperçu:")
    for r in rows[:15]:
        print(f"    {r['Code_Filiere']} {r['Section_Bac']:2s} "
              f"| {str(r['Score_2022']):>8s} {str(r['Score_2023']):>8s} "
              f"{str(r['Score_2024']):>8s} {str(r['Score_2025']):>8s} "
              f"| {r['Filiere_AR'][:50]}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
