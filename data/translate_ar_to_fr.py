#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Traduction arabe -> français des noms d'établissements et filières
dans tunisie_orientation_complete.csv
"""

import pandas as pd
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "tunisie_orientation_complete.csv")

# ============================================================
# ETABLISSEMENTS : Arabe -> Français
# ============================================================
ETAB_MAP = {
    # ── Université de Tunis ──
    "ﺲﻧﻮﺘﺑ ﺔﻴﻋﺎﻤﺘﺟﻹﺍﻭ ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences Humaines et Sociales de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﻴﺳﺎﻴﺴﻟﺍ ﻡﻮﻠﻌﻟﺍﻭ ﻕﻮﻘﺤﻟﺍ ﺔﻴﻠﻛ": "Faculté de Droit et des Sciences Politiques de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﻳﺭﺎﺠﺘﻟﺍﻭ ﺔﻳﺩﺎﺼﺘﻗﻹﺍ ﻡﻮﻠﻌﻠﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESSECT - École Supérieure des Sciences Économiques et Commerciales de Tunis",
    "ﺲﻧﻮﺘﺑ ﻑﺮﺼﺘﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISG - Institut Supérieur de Gestion de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﻠﻴﻤﺠﻟﺍ ﻥﻮﻨﻔﻠﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISBAT - Institut Supérieur des Beaux-Arts de Tunis",
    "ﺲﻧﻮﺘﺑ ﻰﻘﻴﺳﻮﻤﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISM - Institut Supérieur de Musique de Tunis",
    "ﺲﻧﻮﺘﺑ ﻲﺣﺮﺴﻤﻟﺍ ﻦﻔﻠﻟ ﻲﻟﺎﻌﻟﺍﺪﻬﻌﻤﻟﺍ": "ISAD - Institut Supérieur d'Art Dramatique de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻟﺍﻭ ﺔﻴﺑﺩﻷﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻱﺮﻴﻀﺤﺘﻟﺍ ﺪﻬﻌﻤﻟﺍ": "IPEHLST - Institut Préparatoire aux Études Littéraires et de Sciences Humaines de Tunis",
    "ﻱﺎﺒﻟﺍ ﺮﺌﺒﺑ ﻲﻓﺎﻘﺜﻟﺍﻭ ﻲﺑﺎﺒﺸﻟﺍ ﻂﻴﺸﻨﺘﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISAJC - Institut Supérieur de l'Animation pour la Jeunesse et la Culture de Bir El Bey",
    "ﺭﺎﺒﺧﻹﺍ ﻡﻮﻠﻋﻭ ﺔﻓﺎﺤﺼﻟﺍ ﺪﻬﻌﻣ": "IPSI - Institut de Presse et des Sciences de l'Information",
    "ﺲﻧﻮﺘﺑ ﻖﻴﺛﻮﺘﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISD - Institut Supérieur de Documentation de Tunis",
    "ﺔﺼﺘﺨﻤﻟﺍ ﺔﻴﺑﺮﺘﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur de l'Éducation Spécialisée",
    "ﺲﻧﻮﺘﺑ ﺙﺍﺮﺘﻟﺍ ﻦﻬﻤﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Métiers du Patrimoine de Tunis",
    "ﺲﻧﻮﺘﺑ ﺕﺎﻐﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Langues de Tunis",
    "ﺲﻧﻮﺘﺑ ﻑﺮﺼﺘﻟﺍﻭ ﺔﻳﺩﺎﺼﺘﻗﻹﺍ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences Économiques et de Gestion de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﻴﺳﺪﻨﻬﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻱﺮﻴﻀﺤﺘﻟﺍ ﺪﻬﻌﻤﻟﺍ": "IPEIT - Institut Préparatoire aux Études d'Ingénieurs de Tunis",
    "ﺲﻧﻮﺘﺑ ﻝﺎﻤﻋﻸﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Affaires de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﻴﺒﻄﻟﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺘﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Technologies Médicales de Tunis",
    "ﺲﻧﻮﺘﺑ ﺕﻼﺻﺍﻮﻤﻟﺍ ﻲﻓ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Études Technologiques en Communications de Tunis",

    # ── Université de Tunis El Manar ──
    "ﺲﻧﻮﺘﺑ ﺐﻄﻟﺍ ﺔﻴﻠﻛ": "Faculté de Médecine de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﺤﺼﻟﺍ ﺕﺎﻴﻨﻘﺗﻭ ﻡﻮﻠﻌﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESSTST - École Supérieure des Sciences et Techniques de la Santé de Tunis",
    "ﺲﻧﻮﺘﺑ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﻴﻋﺎﻤﺘﺟﻹﺍ ﺕﺎﺳﺍﺭﺪﻟﺍﻭ ﻞﻐﺸﻠﻟ ﻲﻨﻃﻮﻟﺍ ﺪﻬﻌﻤﻟﺍ": "INTES - Institut National du Travail et des Études Sociales de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﻴﻋﺎﻤﺘﺟﻹﺍﻭ ﺔﻴﺳﺎﻴﺴﻟﺍﻭ ﺔﻴﻧﻮﻧﺎﻘﻟﺍ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences Juridiques, Politiques et Sociales de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences Humaines de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﺔﻴﺟﻮﻟﻮﻴﺒﻟﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSBAT - Institut Supérieur des Sciences Biologiques Appliquées de Tunis",
    "ﺲﻧﻮﺘﺑ ﺾﻳﺮﻤﺘﻟﺍ ﻡﻮﻠﻌﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSIT - Institut Supérieur des Sciences Infirmières de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﻴﻤﻗﺮﻟﺍ ﺔﺳﺪﻨﻬﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur de l'Ingénierie Numérique de Tunis",
    "ﺭﺎﻨﻤﻟﺎﺑ ﺔﻴﺳﺪﻨﻬﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻱﺮﻴﻀﺤﺘﻟﺍ ﺪﻬﻌﻤﻟﺍ": "IPEIEM - Institut Préparatoire aux Études d'Ingénieurs d'El Manar",

    # ── Université de La Manouba ──
    "ﺔﺑﻮﻨﻤﺑ ﺕﺎﻴﻧﺎﺴﻧﻹﺍﻭ ﻥﻮﻨﻔﻟﺍﻭ ﺏﺍﺩﻵﺍ ﺔﻴﻠﻛ": "FLAHM - Faculté des Lettres, des Arts et des Humanités de La Manouba",
    "ﺔﺑﻮﻨﻤﺑ ﺎﻳﺪﻴﻤﺘﻠﻤﻟﺍ ﻥﻮﻨﻔﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISAMM - Institut Supérieur des Arts Multimédia de La Manouba",
    "ﻢﻴﻤﺼﺘﻟﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺗ ﻭ ﻡﻮﻠﻌﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESSTED - École Supérieure des Sciences et Technologies du Design",
    "ﺪﻴﻌﺴﻟﺍ ﺮﺼﻘﺑ ﺔﻴﻧﺪﺒﻟﺍ ﺔﻴﺑﺮﺘﻟﺍ ﻭ ﺔﺿﺎﻳﺮﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSEP Ksar Said - Institut Supérieur du Sport et de l'Éducation Physique",
    "ﺔﺑﻮﻨﻤﺑ ﺕﺎﺴـﺳﺆﻤﻟﺍ ﺓﺭﺍﺩﺇ ﻭ ﺔﺒﺳﺎﺤﻤﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISCAE - Institut Supérieur de Comptabilité et d'Administration des Entreprises de La Manouba",
    "ﺔﺑﻮﻨﻤﺑ ﺓﺭﺎﺠﺘﻠﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESC Manouba - École Supérieure de Commerce de La Manouba",
    "ﺔﺑﻮﻨﻤﺑ ﻦﻴﺳﺪﻨﻬﻤﻠﻟ ﺔﻴﻨﻃﻮﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ENIMM - École Nationale d'Ingénieurs de La Manouba",
    "ﺔﺑﻮﻨﻤﺑ ﻲﻤﻗﺮﻟﺍ ﺩﺎﺼﺘﻗﻺﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "École Supérieure de l'Économie Numérique de La Manouba",

    # ── Université de Carthage ──
    "ﺲﻧﻮﺘﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍﻭ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻨﻃﻮﻟﺍ ﺪﻬﻌﻤﻟﺍ": "INSAT - Institut National des Sciences Appliquées et de Technologie",
    "ﺲﻧﻮﺘﺑ ﺮﻴﻤﻌﺘﻟﺍ ﻭ ﺔﻳﺭﺎﻤﻌﻤﻟﺍ ﺔﺳﺪﻨﻬﻠﻟ ﺔﻴﻨﻃﻮﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ENAU - École Nationale d'Architecture et d'Urbanisme",
    "ﺖﺑﺎﺛ ﻱﺪﻴﺴﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺗﻮﻴﺒﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISBST - Institut Supérieur de Biotechnologie de Sidi Thabet",
    "ﺶﻣﺭﺩ ﺝﺎﻃﺮﻘﺑ ﺔﻟﻮﻔﻄﻟﺍ ﺕﺍﺭﺎﻃﻹ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Cadres de l'Enfance de Carthage Dermech",
    "ﺕﺭﺰﻨﺒﺑ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences de Bizerte",
    "ﺕﺭﺰﻨﺒﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Bizerte - Institut Supérieur des Études Technologiques de Bizerte",
    "ﺕﺭﺰﻨﺒﺑ ﺔﻴﺳﺪﻨﻬﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻱﺮﻴﻀﺤﺘﻟﺍ ﺪﻬﻌﻤﻟﺍ": "IPEIB - Institut Préparatoire aux Études d'Ingénieurs de Bizerte",
    "ﺕﺭﺰﻨﺒﺑ ﺭﺎﺤﺒﻟﺍ ﻡﻮﻠﻌﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSMB - Institut Supérieur des Sciences de la Mer de Bizerte",
    "ﺕﺭﺰﻨﺒﺑ ﻑﺮﺼﺘﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISG Bizerte - Institut Supérieur de Gestion de Bizerte",
    "ﻞﺑﺎﻨﺑ ﺔﻠﻴﻤﺠﻟﺍ ﻥﻮﻨﻔﻠﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISBAN - Institut Supérieur des Beaux-Arts de Nabeul",
    "ﻞﺑﺎﻨﺑ ﺕﺎﻐﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Langues de Nabeul",
    "ﻞﺑﺎﻨﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Nabeul - Institut Supérieur des Études Technologiques de Nabeul",
    "ﻞﺑﺎﻨﺑ ﺔﻴﺳﺪﻨﻬﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻱﺮﻴﻀﺤﺘﻟﺍ ﺪﻬﻌﻤﻟﺍ": "IPEIN - Institut Préparatoire aux Études d'Ingénieurs de Nabeul",
    "ﻞﺑﺎﻨﺑ ﻑﺮﺼﺘﻟﺍﻭ ﺔﻳﺩﺎﺼﺘﻗﻹﺍ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences Économiques et de Gestion de Nabeul",
    "ﻥﺎﻴﻨﺒﻟﺍﻭ ﻥﺍﺮﻤﻌﻟﺍﻭ ﺔﺌﻴﺒﻟﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Technologies de l'Environnement, de l'Urbanisme et du Bâtiment",
    "ﻒﻳﺮﻈﻟﺍ ﻱﺪﻴﺴﺑ ﺔﻴﻗﺪﻨﻔﻟﺍﻭ ﺔﻴﺣﺎﻴﺴﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISHET - Institut Supérieur des Hautes Études Touristiques et Hôtelières de Sidi Dhrif",
    "ﺝﺎﻃﺮﻘﺑ ﺎﻴﻠﻌﻟﺍ ﺔﻳﺭﺎﺠﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻟﺍ ﺪﻬﻌﻣ": "IHEC Carthage - Institut des Hautes Études Commerciales de Carthage",
    "ﺱﺩﺍﺮﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Radès - Institut Supérieur des Études Technologiques de Radès",
    "ﺮﻃﺎﻤﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﻭ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSAT Mateur - Institut Supérieur des Sciences Appliquées et de Technologie de Mateur",
    "ﺮﻃﺎﻤﺑ ﺔﺣﻼﻔﻠﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESA Mateur - École Supérieure d'Agriculture de Mateur",
    "ﺔﻴﺒﻴﻠﻘﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Kélibia - Institut Supérieur des Études Technologiques de Kélibia",
    "ﻥﺍﻮﻏﺰﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Zaghouan - Institut Supérieur des Études Technologiques de Zaghouan",
    "ﻥﺍﻮﻏﺰﺑ ﺕﺎﻴﻧﺎﺴﻧﻹﺍ ﻲﻓ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Études Appliquées en Humanités de Zaghouan",
    "ﺲﻧﻮﺘﺑ ﺔﻴﺋﺍﺬﻐﻟﺍ ﺕﺎﻋﺎﻨﺼﻠﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESIAT - École Supérieure des Industries Alimentaires de Tunis",
    "ﻥﺮﻘﻤﺑ ﺔﺣﻼﻔﻠﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESA Mograne - École Supérieure d'Agriculture de Mograne",

    # ── Université de Sousse ──
    "ﺔﺳﻮﺴﺑ ﺐﻄﻟﺍ ﺔﻴﻠﻛ": "Faculté de Médecine de Sousse",
    "ﺔﺳﻮﺴﺑ ﺔﻴﺳﺎﻴﺴﻟﺍ ﻡﻮﻠﻌﻟﺍﻭ ﻕﻮﻘﺤﻟﺍ ﺔﻴﻠﻛ": "Faculté de Droit et des Sciences Politiques de Sousse",
    "ﺔﺳﻮﺴﺑ ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻟﺍﻭ ﺏﺍﺩﻵﺍ ﺔﻴﻠﻛ": "Faculté des Lettres et des Sciences Humaines de Sousse",
    "ﺔﺳﻮﺴﺑ ﻑﺮﺼﺘﻟﺍﻭ ﺔﻳﺩﺎﺼﺘﻗﻹﺍ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences Économiques et de Gestion de Sousse",
    "ﺔﺳﻮﺴﺑ ﻑﺮﺼﺘﻠﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISG Sousse - Institut Supérieur de Gestion de Sousse",
    "ﺔﺳﻮﺴﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﻭ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSAT Sousse - Institut Supérieur des Sciences Appliquées et de Technologie de Sousse",
    "ﺔﺳﻮﺴﺑ ﺔﺤﺼﻟﺍ ﺕﺎﻴﻨﻘﺗ ﻭ ﻡﻮﻠﻌﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESSTSS - École Supérieure des Sciences et Techniques de la Santé de Sousse",
    "ﺔﺳﻮﺴﺑ ﺔﻠﻴﻤﺠﻟﺍ ﻥﻮﻨﻔﻠﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Beaux-Arts de Sousse",
    "ﺔﺳﻮﺴﺑ ﻰﻘﻴﺳﻮﻤﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur de Musique de Sousse",
    "ﺔﺳﻮﺴﺑ ﺔﻴﺘﺴﺟﻮﻠﻟﺍﻭ ﻞﻘﻨﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur du Transport et de la Logistique de Sousse",
    "ﺔﺳﻮﺴﺑ ﺔﻳﺎﺒﺠﻟﺍ ﻭ ﺔﻴﻟﺎﻤﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISFFS - Institut Supérieur de Finances et de Fiscalité de Sousse",
    "ﺔﺳﻮﺴﺑ ﺾﻳﺮﻤﺘﻟﺍ ﻡﻮﻠﻌﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences Infirmières de Sousse",
    "ﺔﺳﻮﺴﺑ ﺎﻴﻠﻌﻟﺍ ﺔﻳﺭﺎﺠﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻟﺍ ﺪﻬﻌﻣ": "IHEC Sousse - Institut des Hautes Études Commerciales de Sousse",
    "ﺔﺳﻮﺴﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Sousse - Institut Supérieur des Études Technologiques de Sousse",
    "ﺔﺳﻮﺴﺑ ﻝﺎﺼﺗﻻﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺗ ﻭ ﺔﻴﻣﻼﻋﻼﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur de l'Informatique et des Technologies de Communication de Sousse",
    "ﺔﺳﻮﺳ ﻡﺎﻤﺤﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍﻭ ﻡﻮﻠﻌﻠﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "École Supérieure des Sciences et de la Technologie de Hammam Sousse",

    # ── Université de Monastir ──
    "ﺮﻴﺘﺴﻨﻤﻟﺎﺑ ﺐﻄﻟﺍ ﺔﻴﻠﻛ": "Faculté de Médecine de Monastir",
    "ﺮﻴﺘﺴﻨﻤﻟﺎﺑ ﺔﻟﺪﻴﺼﻟﺍ ﺔﻴﻠﻛ": "Faculté de Pharmacie de Monastir",
    "ﺮﻴﺘﺴﻨﻤﻟﺎﺑ ﻥﺎﻨﺳﻷﺍ ﺐﻃ ﺔﻴﻠﻛ": "Faculté de Médecine Dentaire de Monastir",
    "ﺮﻴﺘﺴﻨﻤﻟﺎﺑ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences de Monastir",
    "ﺮﻴﺘﺴﻨﻤﻟﺎﺑ ﺔﺤﺼﻟﺍ ﺕﺎﻴﻨﻘﺗﻭ ﻡﻮﻠﻌﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESSTSS - École Supérieure des Sciences et Techniques de la Santé de Monastir",
    "ﺮﻴﺘﺴﻨﻤﻟﺎﺑ ﺕﺎﻴﺿﺎﻳﺮﻟﺍ ﻭ ﺔﻴﻣﻼﻋﻺﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISIMM - Institut Supérieur d'Informatique et de Mathématiques de Monastir",
    "ﺮﻴﺘﺴﻨﻤﻟﺎﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺗﻮﻴﺒﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISBM - Institut Supérieur de Biotechnologie de Monastir",
    "ﺮﻴﺘﺴﻨﻤﻟﺎﺑ ﺔﺿﻮﻤﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur de la Mode de Monastir",
    "ﺮﻴﺘﺴﻨﻤﻟﺎﺑ ﺔﻴﺳﺪﻨﻬﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻱﺮﻴﻀﺤﺘﻟﺍ ﺪﻬﻌﻤﻟﺍ": "IPEIM - Institut Préparatoire aux Études d'Ingénieurs de Monastir",
    "ﻦﻴﻧﺪﻤﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Médenine - Institut Supérieur des Études Technologiques de Médenine",
    "ﻦﻴﻧﺪﻤﺑ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﺎﻴﺟﻮﻟﻮﻴﺒﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISBAM - Institut Supérieur de Biologie Appliquée de Médenine",
    "ﻦﻴﻧﺪﻤﺑ ﺔﻴﻣﻼﻋﻺﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur d'Informatique de Médenine",
    "ﻦﻴﻧﺪﻤﺑ ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences Humaines de Médenine",
    "ﻦﻴﻨﻜﻤﻟﺎﺑ ﺕﺎﻐﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Langues d'El Maknine",
    "ﻦﻴﻧﺪﻤﺑ ﻑﺮﺤﻟﺍ ﻭ ﻥﻮﻨﻔﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Arts et Métiers de Médenine",

    # ── Université de Sfax ──
    "ﺲﻗﺎﻔﺼﺑ ﺐﻄﻟﺍ ﺔﻴﻠﻛ": "Faculté de Médecine de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﻑﺮﺼﺘﻟﺍﻭ ﺔﻳﺩﺎﺼﺘﻗﻹﺍ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "FSEGS - Faculté des Sciences Économiques et de Gestion de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﻕﻮﻘﺤﻟﺍ ﺔﻴﻠﻛ": "Faculté de Droit de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻟﺍﻭ ﺏﺍﺩﻵﺍ ﺔﻴﻠﻛ": "Faculté des Lettres et des Sciences Humaines de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﺔﺤﺼﻟﺍ ﺕﺎﻴﻨﻘﺗﻭ ﻡﻮﻠﻌﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESSTSS - École Supérieure des Sciences et Techniques de la Santé de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﺓﺭﺎﺠﺘﻠﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESC Sfax - École Supérieure de Commerce de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﺕﻻﺎﺼﺗﻹﺍﻭ ﻚﻴﻧﻭﺮﺘﻜﻟﻺﻟ ﺔﻴﻨﻃﻮﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ENIS - École Nationale d'Ingénieurs de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺗﻮﻴﺒﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur de Biotechnologie de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﺎﻳﺪﻴﻤﺘﻠﻤﻟﺍ ﻭ ﺔﻴﻣﻼﻋﻼﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISIMS - Institut Supérieur d'Informatique et de Multimédia de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﻰﻘﻴﺳﻮﻤﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur de Musique de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﺔﻴﺳﺪﻨﻬﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻱﺮﻴﻀﺤﺘﻟﺍ ﺪﻬﻌﻤﻟﺍ": "IPEIS - Institut Préparatoire aux Études d'Ingénieurs de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Sfax - Institut Supérieur des Études Technologiques de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﺔﻴﻧﺪﺒﻟﺍ ﺔﻴﺑﺮﺘﻟﺍ ﻭ ﺔﺿﺎﻳﺮﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSEP Sfax - Institut Supérieur du Sport et de l'Éducation Physique de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﾾﻳﺮﻤﺘﻟﺍ ﻡﻮﻠﻌﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences Infirmières de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﺾﻳﺮﻤﺘﻟﺍ ﻡﻮﻠﻌﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences Infirmières de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﻑﺮﺤﻟﺍ ﻭ ﻥﻮﻨﻔﻠﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Arts et Métiers de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﺔﻳﺭﺎﺠﺘﻟﺍ ﺎﻴﻠﻌﻟﺍ ﺕﺎﺳﺍﺭﺪﻟﺍ ﺪﻬﻌﻣ": "IHEC Sfax - Institut des Hautes Études Commerciales de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﻝﺎﻤﻋﻻﺍ ﺓﺭﺍﺩﻻ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISAAS - Institut Supérieur d'Administration des Affaires de Sfax",
    "ﺲﻗﺎﻔﺼﺑ ﻲﻋﺎﻨﺼﻟﺍ ﻑﺮﺼﺘﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur de Gestion Industrielle de Sfax",
    "ﺏﺎﺒﻟﺍ ﺯﺎﺠﻤﺑ ﻦﻴﺳﺪﻨﻬﻤﻠﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "École Supérieure d'Ingénieurs de Medjez El Bab",

    # ── Université de Gabès ──
    "ﺲﺑﺎﻘﺑ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences de Gabès",
    "ﺲﺑﺎﻘﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﻭ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSAT Gabès - Institut Supérieur des Sciences Appliquées et de Technologie de Gabès",
    "ﺲﺑﺎﻘﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Gabès - Institut Supérieur des Études Technologiques de Gabès",
    "ﺲﺑﺎﻘﺑ ﺔﻴﺳﺪﻨﻬﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻱﺮﻴﻀﺤﺘﻟﺍ ﺪﻬﻌﻤﻟﺍ": "IPEIG - Institut Préparatoire aux Études d'Ingénieurs de Gabès",
    "ﺲﺑﺎﻘﺑ ﺕﺎﻐﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Langues de Gabès",
    "ﺲﺑﺎﻘﺑ ﻑﺮﺼﺘﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISG Gabès - Institut Supérieur de Gestion de Gabès",
    "ﺲﺑﺎﻘﺑ ﺎﻳﺪﻴﻤﻴﺘﻠﻤﻟﺍ ﻭ ﺔﻴﻣﻼﻋﻺﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur d'Informatique et de Multimédia de Gabès",
    "ﺲﺑﺎﻘﺑ ﺔﻴﻋﺎﻨﺼﻟﺍ ﺕﺎﻣﻮﻈﻨﻤﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Systèmes Industriels de Gabès",
    "ﺲﺑﺎﻘﺑ ﺔﻴﻧﻮﻧﺎﻘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Études Juridiques de Gabès",
    "ﺲﺑﺎﻘﺑ ﺾﻳﺮﻤﺘﻟﺍ ﻡﻮﻠﻌﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences Infirmières de Gabès",
    "ﺲﺑﺎﻘﺑ ﻑﺮﺤﻟﺍ ﻭ ﻥﻮﻨﻔﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Arts et Métiers de Gabès",
    "ﺲﺑﺎﻘﺑ ﻩﺎﻴﻤﻟﺍ ﺕﺎﻴﻨﻘﺗ ﻭ ﻡﻮﻠﻌﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences et Techniques des Eaux de Gabès",
    "ﺔﺑﺮﺠﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Djerba - Institut Supérieur des Études Technologiques de Djerba",
    "ﺭﺯﻮﺘﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Tozeur - Institut Supérieur des Études Technologiques de Tozeur",
    "ﺭﺯﻮﺘﺑ ﺕﺎﻴﻧﺎﺴﻧﻹﺍ ﻲﻓ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Études Appliquées en Humanités de Tozeur",
    "ﻲﻠﺒﻘﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Kébili - Institut Supérieur des Études Technologiques de Kébili",
    "ﺔﻳﺪﻬﻤﻟﺎﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﻭ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSAT Mahdia - Institut Supérieur des Sciences Appliquées et de Technologie de Mahdia",
    "ﺔﻳﺪﻬﻤﻟﺎﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Mahdia - Institut Supérieur des Études Technologiques de Mahdia",
    "ﺔﻳﺪﻬﻤﻟﺎﺑ ﺔﻴﻣﻼﻋﻺﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur d'Informatique de Mahdia",
    "ﺔﻳﺪﻬﻤﻟﺎﺑ ﺕﺎﻴﻧﺎﺴﻧﻻﺍ ﻲﻓ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Études Appliquées en Humanités de Mahdia",
    "ﺔﻳﺪﻬﻤﻟﺎﺑ ﻑﺮﺤﻟﺍ ﻭ ﻥﻮﻨﻔﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Arts et Métiers de Mahdia",
    "ﺔﻳﺪﻬﻤﻟﺎﺑ ﻑﺮﺼﺘﻟﺍﻭ ﺔﻳﺩﺎﺼﺘﻗﻹﺍ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences Économiques et de Gestion de Mahdia",

    # ── Université de Jendouba ──
    "ﺔﺑﻭﺪﻨﺠﺑ ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences Humaines de Jendouba",
    "ﺔﺑﻭﺪﻨﺠﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Jendouba - Institut Supérieur des Études Technologiques de Jendouba",
    "ﺔﺑﻭﺪﻨﺠﺑ ﻑﺮﺼﺘﻟﺍﻭ ﺔﻳﺩﺎﺼﺘﻗﻹﺍﻭ ﺔﻴﻧﻮﻧﺎﻘﻟﺍ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences Juridiques, Économiques et de Gestion de Jendouba",
    "ﺔﻗﺮﺒﻄﺑ ﻲﻋﺍﺮﻤﻟﺍﻭ ﺕﺎﺑﺎﻐﻟﺍ ﺪﻬﻌﻣ": "Institut Sylvo-Pastoral de Tabarka",
    "ﺔﺟﺎﺒﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺗﻮﻴﺒﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur de Biotechnologie de Béja",
    "ﺔﺟﺎﺒﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Béja - Institut Supérieur des Études Technologiques de Béja",
    "ﺔﺟﺎﺒﺑ ﺔﻴﻣﻼﻋﻻﺍ ﻭ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﺕﺎﻐﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Langues Appliquées et de l'Informatique de Béja",

    # ── Université de Kairouan ──
    "ﻥﺍﻭﺮﻴﻘﻟﺎﺑ ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻟﺍﻭ ﺏﺍﺩﻵﺍ ﺔﻴﻠﻛ": "Faculté des Lettres et des Sciences Humaines de Kairouan",
    "ﻥﺍﻭﺮﻴﻘﻟﺎﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﻭ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSAT Kairouan - Institut Supérieur des Sciences Appliquées et de Technologie de Kairouan",
    "ﻥﺍﻭﺮﻴﻘﻟﺎﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Kairouan - Institut Supérieur des Études Technologiques de Kairouan",
    "ﻥﺍﻭﺮﻴﻘﻟﺎﺑ ﺔﻴﺳﺪﻨﻬﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻱﺮﻴﻀﺤﺘﻟﺍ ﺪﻬﻌﻤﻟﺍ": "IPEIK - Institut Préparatoire aux Études d'Ingénieurs de Kairouan",
    "ﻥﺍﻭﺮﻴﻘﻟﺎﺑ ﺔﻴﺳﺎﻴﺴﻟﺍﻭ ﺔﻴﻧﻮﻧﺎﻘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Études Juridiques et Politiques de Kairouan",
    "ﻥﺍﻭﺮﻴﻘﻟﺎﺑ ﺔﻴﻣﻼﺳﻹﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences Islamiques de Kairouan",
    "ﻥﺍﻭﺮﻴﻘﻟﺎﺑ ﺔﻴﻣﻼﻋﻹﺍﻭ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﺕﺎﻴﺿﺎﻳﺮﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISMAI - Institut Supérieur des Mathématiques Appliquées et de l'Informatique de Kairouan",
    "ﻥﺍﻭﺮﻴﻘﻟﺎﺑ ﻑﺮﺤﻟﺍﻭ ﻥﻮﻨﻔﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Arts et Métiers de Kairouan",
    "ﻥﺍﻭﺮﻴﻘﻟﺎﺑ ﻑﺮﺼﺘﻟﺍ ﻭ ﺔﻴﻣﻼﻋﻺﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur d'Informatique et de Gestion de Kairouan",
    "ﺔﻠﻄﻴﺒﺴﺑ ﺕﺎﻴﻧﺎﺴﻧﻻﺍ ﻲﻓ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Études Appliquées en Humanités de Sbeitla",
    "ﻦﻳﺮﺼﻘﻟﺎﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﻭ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSAT Kasserine - Institut Supérieur des Sciences Appliquées et de Technologie de Kasserine",
    "ﻦﻳﺮﺼﻘﻟﺎﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Kasserine - Institut Supérieur des Études Technologiques de Kasserine",
    "ﻦﻳﺮﺼﻘﻟﺎﺑ ﻑﺮﺤﻟﺍ ﻭ ﻥﻮﻨﻔﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Arts et Métiers de Kasserine",
    "ﻦﻳﻭﺎﻄﺘﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Tataouine - Institut Supérieur des Études Technologiques de Tataouine",
    "ﻦﻳﻭﺎﻄﺘﺑ ﻑﺮﺤﻟﺍ ﻭ ﻥﻮﻨﻔﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Arts et Métiers de Tataouine",

    # ── Université de Gafsa ──
    "ﺔﺼﻔﻘﺑ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences de Gafsa",
    "ﺔﺼﻔﻘﺑ ﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﻭ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSAT Gafsa - Institut Supérieur des Sciences Appliquées et de Technologie de Gafsa",
    "ﺔﺼﻔﻘﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Gafsa - Institut Supérieur des Études Technologiques de Gafsa",
    "ﺔﺼﻔﻘﺑ ﺔﻴﺳﺪﻨﻬﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻱﺮﻴﻀﺤﺘﻟﺍ ﺪﻬﻌﻤﻟﺍ": "IPEIG - Institut Préparatoire aux Études d'Ingénieurs de Gafsa",
    "ﺔﺼﻔﻘﺑ ﺔﻴﺑﺮﺘﻟﺍﻭ ﺔﻴﻋﺎﻤﺘﺟﻻﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences Sociales et de l'Éducation de Gafsa",
    "ﺔﺼﻔﻘﺑ ﺔﻴﻧﺪﺒﻟﺍ ﺔﻴﺑﺮﺘﻟﺍ ﻭ ﺔﺿﺎﻳﺮﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSEP Gafsa - Institut Supérieur du Sport et de l'Éducation Physique de Gafsa",
    "ﺔﺼﻔﻘﺑ ﺕﺎﺴﺳﺆﻤﻟﺍ ﺓﺭﺍﺩﻹ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur d'Administration des Entreprises de Gafsa",
    "ﺔﺼﻔﻘﺑ ﺕﺎﻴﻧﺎﺴﻧﻻﺍ ﻲﻓ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Études Appliquées en Humanités de Gafsa",
    "ﺔﺼﻔﻘﺑ ﻑﺮﺤﻟﺍ ﻭ ﻥﻮﻨﻔﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Arts et Métiers de Gafsa",
    "ﺔﺼﻔﻘﺑ ﺔﺤﺼﻟﺍ ﺕﺎﻴﻨﻘﺗ ﻭ ﻡﻮﻠﻌﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESSTSS Gafsa - École Supérieure des Sciences et Techniques de la Santé de Gafsa",

    # ── Université Ezzitouna ──
    "ﺲﻧﻮﺘﺑ ﻦﻳﺪﻟﺍ ﻝﻮﺻﻷ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur de Théologie de Tunis",
    "ﺲﻧﻮﺘﺑ ﺔﻴﻣﻼﺳﻹﺍ ﺓﺭﺎﻀﺤﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur de Civilisation Islamique de Tunis",
    "ﻥﺍﻭﺮﻴﻘﻟﺎﺑ ﺔﻴﻣﻼﺳﻹﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences Islamiques de Kairouan",

    # ── Divers ──
    "ﺔﻴﻣﻼﻋﻼﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISI - Institut Supérieur d'Informatique",
    "ﺓﺮﻜﺴﺑ ﺎﻴﺟﻮﻟﻮﺠﻟﺍ ﻭ ﺎﻴﺟﻮﻟﻮﻴﺒﻟﺍ ﻲﻓ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "IPEST - Institut Préparatoire aux Études Scientifiques et Techniques de Tunis",
    "ﻢﻳﺮﻣ ﻂﺸﺑ ﺔﻴﺣﻼﻔﻟﺍ ﻡﻮﻠﻌﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "INAT - Institut National Agronomique de Tunisie",
    "ﺪﻳﺯﻮﺑ ﻱﺪﻴﺴﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Sidi Bouzid - Institut Supérieur des Études Technologiques de Sidi Bouzid",
    "ﺪﻳﺯﻮﺑ ﻱﺪﻴﺴﺑ ﺕﺎﻴﻨﻘﺘﻟﺍ ﻭ ﻡﻮﻠﻌﻟﺍ ﺔﻴﻠﻛ": "Faculté des Sciences et Techniques de Sidi Bouzid",
    "ﺪﻳﺯﻮﺑ ﻱﺪﻴﺴﺑ ﻑﺮﺤﻟﺍﻭ ﻥﻮﻨﻔﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Arts et Métiers de Sidi Bouzid",
    "ﺔﻧﺎﻴﻠﺴﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Siliana - Institut Supérieur des Études Technologiques de Siliana",
    "ﺔﻧﺎﻴﻠﺴﺑ ﻑﺮﺤﻟﺍ ﻭ ﻥﻮﻨﻔﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Arts et Métiers de Siliana",
    "ﺔﻳﺭﺪﺴﻟﺍ ﺝﺮﺒﺑ ﺔﺌﻴﺒﻟﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺗ ﻭ ﻡﻮﻠﻌﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences et Technologies de l'Environnement de Borj Cedria",
    "ﺔﻳﺭﺪﺴﻟﺍ ﺝﺮﺒﺑ ﻝﺎﺼﺗﻹﺍﻭ ﺕﺎﻣﻮﻠﻌﻤﻟﺍ ﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "SUP'COM - Institut Supérieur des Technologies de l'Information et de la Communication de Borj Cedria",
    "ﺔﻴﻗﺮﺸﻟﺎﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Charguia - Institut Supérieur des Études Technologiques de Charguia",
    "ﻝﻼﻫ ﺮﺼﻗ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Ksar Hellal - Institut Supérieur des Études Technologiques de Ksar Hellal",
    "ﻑﺎﻜﻟﺎﺑ ﺔﺣﻼﻔﻠﻟ ﺎﻴﻠﻌﻟﺍ ﺔﺳﺭﺪﻤﻟﺍ": "ESA Le Kef - École Supérieure d'Agriculture du Kef",
    "ﻑﺎﻜﻟﺎﺑ ﺔﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻰﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISET Le Kef - Institut Supérieur des Études Technologiques du Kef",
    "ﻑﺎﻜﻟﺎﺑ ﺔﻴﻣﻼﻋﻺﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur d'Informatique du Kef",
    "ﻑﺎﻜﻟﺎﺑ ﺔﻴﻧﺪﺒﻟﺍ ﺔﻴﺑﺮﺘﻟﺍﻭ ﺔﺿﺎﻳﺮﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "ISSEP Le Kef - Institut Supérieur du Sport et de l'Éducation Physique du Kef",
    "ﻑﺎﻜﻟﺎﺑ ﺕﺎﻴﻧﺎﺴﻧﻹﺍ ﻲﻓ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﺕﺎﺳﺍﺭﺪﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Études Appliquées en Humanités du Kef",
    "ﻑﺎﻜﻟﺎﺑ ﺡﺮﺴﻤﻟﺍ ﻭ ﻰﻘﻴﺳﻮﻤﻠﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur de Musique et de Théâtre du Kef",
    "ﻑﺎﻜﻟﺎﺑ ﺾﻳﺮﻤﺘﻟﺍ ﻡﻮﻠﻌﻟ ﻲﻟﺎﻌﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut Supérieur des Sciences Infirmières du Kef",
    "ﻑﺎﻜﻟﺎﺑ ﻡﻮﻠﻌﻟﺍﻭ ﺎﻴﺟﻮﻟﻮﻨﻜﺘﻠﻟ ﻲﻨﻃﻮﻟﺍ ﺪﻬﻌﻤﻟﺍ": "Institut National des Sciences et de la Technologie du Kef",
}

# ============================================================
# FILIERES : Patterns arabe -> Français
# ============================================================
FILIERE_MAP = {
    # ── Médecine / Pharmacie / Dentaire ──
    "ﺐــﻄـﻟﺍ": "Médecine",
    "ﺔــــﻟﺪــــﻴـﺼـﻟﺍ": "Pharmacie",
    "ﻥﺎـــﻨـﺳﻷﺍ ﺐـــﻃ": "Médecine Dentaire",
    "ﺔﻳﺭﺎﻤﻌﻤﻟﺍ ﺔﺳﺪﻨﻬﻟﺍ": "Architecture",

    # ── Langues ──
    "ﺔﻴﺑﺮﻌﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Arabe",
    "ﺏﺍﺩﺁ ﺔﻴﺑﺮﻌﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Arabe",
    "ﺔﻳﺰﻴﻠﻘﻧﻹﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Anglais",
    "ﺏﺍﺩﺁ ﺔﻳﺰﻴﻠﻘﻧﻹﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Anglais",
    "ﺔﻴﺴﻧﺮﻔﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Français",
    "ﺏﺍﺩﺁ ﺔﻴﺴﻧﺮﻔﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Français",
    "ﺔﻴﻧﺎﺒﺳﻹﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Espagnol",
    "ﺏﺍﺩﺁ ﺔﻴﻧﺎﺒﺳﻹﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Espagnol",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﺔﻴﻧﺎﺒﺳﻹﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Espagnol",
    "ﺔﻴﻟﺎﻄﻳﻹﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Italien",
    "ﺏﺍﺩﺁ ﺔﻴﻟﺎﻄﻳﻹﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Italien",
    "ﺔﻴﻧﺎﻤﻟﻷﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Allemand",
    "ﺏﺍﺩﺁ ﺔﻴﻧﺎﻤﻟﻷﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Allemand",
    "ﺔﻴﺳﻭﺮﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Russe",
    "ﺏﺍﺩﺁ ﺔﻴﺳﻭﺮﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Russe",
    "ﺔﻴﻨﻴﺼﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Chinois",
    "ﺏﺍﺩﺁ ﺔﻴﻨﻴﺼﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Chinois",
    "ﺕﺍﺭﺎﺷﻹﺍ ﺔﻐﻟ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Langue des Signes",
    "ﺏﺍﺩﺁ ﺕﺍﺭﺎﺷﻹﺍ ﺔﻐﻟ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Langue des Signes",
    "ﺔﻤﺟﺮﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Traduction",
    "ﺏﺍﺩﺁ ﺔﻤﺟﺮﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Traduction",

    # ── Sciences Humaines ──
    "ﺲـــﻔـﻨﻟﺍ ﻢﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Psychologie",
    "ﻉﺎﻤﺘﺟﻻﺍ ﻢــﻠـﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sociologie",
    "ﺏﺍﺩﺁ ﻉﺎﻤﺘﺟﻻﺍ ﻢــﻠـﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sociologie",
    "ﺔــﻔــﺴﻠـﻔﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Philosophie",
    "ﺏﺍﺩﺁ ﺔــﻔــﺴﻠـﻔﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Philosophie",
    "ﺦﻳﺭﺎﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Histoire",
    "ﺏﺍﺩﺁ ﺦﻳﺭﺎﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Histoire",
    "ﺎﻴﻓﺍﺮﻐﺠﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Géographie",
    "ﺏﺍﺩﺁ ﺎﻴﻓﺍﺮﻐﺠﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Géographie",
    "ﺎﻴﺟﻮﻟﻮﺑﻭﺮﺘﻧﻷﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Anthropologie",
    "ﺏﺍﺩﺁ ﺎﻴﺟﻮﻟﻮﺑﻭﺮﺘﻧﻷﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Anthropologie",
    "ﺭﺎﺛﻵﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Archéologie",
    "ﺏﺍﺩﺁ ﺭﺎﺛﻵﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Archéologie",

    # ── Droit / Gestion / Économie ──
    "ﻥﻮﻧﺎﻘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Droit",
    "ﺏﺍﺩﺁ ﻥﻮﻧﺎﻘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Droit",
    "ﻑﺮﺼﺘﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de Gestion",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﻑﺮﺼﺘﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de Gestion",
    "ﺔﻳﺩﺎﺼﺘﻗﻻﺍ ﻡﻮﻠﻌﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Sciences Économiques",
    "ﻑﺮـﺼـﺘﻟﺍ ﺔﻴﻣﻼﻋﺇ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Informatique de Gestion",
    "ﻝﺎﻤﻋﻷﺍ ﺓﺭﺍﺩﺇ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Administration des Affaires",
    "ﺕﺎﻴﺿﺎﻳﺭ ﻝﺎﻤﻋﻷﺍ ﺓﺭﺍﺩﺇ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Administration des Affaires",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﻝﺎﻤﻋﻷﺍ ﺓﺭﺍﺩﺇ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Administration des Affaires",
    "ﻝﺎﻤﻋﻷﺍ ﺓﺭﺍﺩﺇ ﻲﻓ ﺱﻮﻳﺭﻮﻟﺎﻜﺒﻟﺍ": "Bachelor en Administration des Affaires",
    "ﺕﺎﻴﺿﺎﻳﺭ ﻝﺎﻤﻋﻷﺍ ﺓﺭﺍﺩﺇ ﻲﻓ ﺱﻮﻳﺭﻮﻟﺎﻜﺒﻟﺍ": "Bachelor en Administration des Affaires",
    "ﺔﻴﻟﺎﻤﻟﺍ ﻭ ﺔﺒﺳﺎﺤﻤﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Comptabilité et Finance",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺔﻴﻟﺎﻤﻟﺍ ﻭ ﺔﺒﺳﺎﺤﻤﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Comptabilité et Finance",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﺔﻴﻟﺎﻤﻟﺍ ﻭ ﺔﺒﺳﺎﺤﻤﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Comptabilité et Finance",
    "ﻲﻋﺎﻤﺘﺟﻻﺍ ﻥﻮﻧﺎﻘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Droit Social",
    "ﻞﻐﺸﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Sciences du Travail",
    "ﺔﻴﻋﺎﻤﺘﺟﻻﺍ ﺔﻣﺪﺨﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Service Social",
    "ﻲﻋﺎﻤﺘﺟﻻﺍ ﻞﺧﺪﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Intervention Sociale",
    "ﻊﻳﺯﻮﺘﻟﺍﻭ ﺓﺭﺎﺠﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Commerce et Distribution",
    "ﻝﺎﺼﺗﻻﺍﻭ ﺕﺎﻣﻮﻠﻌﻤﻟﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺗ ﻲﻓ ﻑﺮﺼﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Gestion des TIC",

    # ── Arts / Design ──
    "ﺔﻴﻠﻴﻜﺸﺘﻟﺍ ﻥﻮﻨﻔﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Arts Plastiques",
    "ﺏﺍﺩﺁ ﺔﻴﻠﻴﻜﺸﺘﻟﺍ ﻥﻮﻨﻔﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Arts Plastiques",
    "ﺀﺎﻀﻔﻟﺍ ﻢﻴﻤﺼﺗ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Design d'Espace",
    "ﺏﺍﺩﺁ ﺀﺎﻀﻔﻟﺍ ﻢﻴﻤﺼﺗ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Design d'Espace",
    "ﺝﻮﺘﻨﻤﻟﺍ ﻢﻴﻤﺼﺗ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Design Produit",
    "ﺏﺍﺩﺁ ﺝﻮﺘﻨﻤﻟﺍ ﻢﻴﻤﺼﺗ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Design Produit",
    "ﺓﺭﻮﺼﻟﺍ ﻢﻴﻤﺼﺗ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Design Image",
    "ﺏﺍﺩﺁ ﺓﺭﻮﺼﻟﺍ ﻢﻴﻤﺼﺗ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Design Image",
    "ﺔﻴﻘﻴﺳﻮﻤﻟﺍ ﻡﻮﻠﻌﻟﺍ ﻭ ﻰﻘﻴﺳﻮﻤﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Musique et Musicologie",
    "ﺏﺍﺩﺁ ﺔﻴﻘﻴﺳﻮﻤﻟﺍ ﻡﻮﻠﻌﻟﺍ ﻭ ﻰﻘﻴﺳﻮﻤﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Musique et Musicologie",
    "ﺽﺮﻌﻟﺍ ﻥﻮﻨﻓ ﻭ ﺡﺮﺴﻤﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Théâtre et Arts du Spectacle",
    "ﻱﺮﺼﺒﻟﺍ ﻲﻌﻤﺴﻟﺍﻭ ﺎﻤﻨﻴﺴﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Cinéma et Audiovisuel",
    "ﻂﺋﺎﺳﻮﻟﺍ ﻭ ﻥﻮﻨﻔﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Arts et Médias",

    # ── Sciences / Maths / Informatique ──
    "ﺕﺎﻴﺿﺎﻳﺮﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Mathématiques",
    "ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﺕﺎﻴﺿﺎﻳﺮﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Mathématiques Appliquées",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﺔﻴﻘﻴﺒﻄﺘﻟﺍ ﺕﺎﻴﺿﺎﻳﺮﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Mathématiques Appliquées",
    "ﺔﻴﻣﻼﻋﻹﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences Informatiques",
    "ﺔﻴﻣﻼﻋﻹﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺗ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Technologies de l'Informatique",
    "ﺕﻻﺎﺼﺗﻻﺍﻭ ﺕﺎﻣﻮﻠﻌﻤﻟﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺗ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en TIC",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺕﻻﺎﺼﺗﻻﺍﻭ ﺕﺎﻣﻮﻠﻌﻤﻟﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺗ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en TIC",
    "ﺕﻻﺎﺼﺗﻻﺍﻭ ﺕﺎﻣﻮﻠﻌﻤﻟﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺗﻭ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences et Technologies de l'Information",
    "ﺔﻴﻣﻼﻋﻹﺍ ﻢﻈﻧ ﺔﺳﺪﻨﻫ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Ingénierie des Systèmes Informatiques",
    "ﺀﺎﻳﺰﻴﻔﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Physique",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﺀﺎﻳﺰﻴﻔﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Physique",
    "ﺀﺎﻴﻤﻴﻜﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Chimie",
    "ﺀﺎﻴﻤﻴﻜﻟﺍ ﻭ ﺀﺎﻳﺰﻴﻔﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Physique-Chimie",
    "ﺀﺎﻴﺣﻷﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de la Vie",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺀﺎﻴﺣﻷﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de la Vie",
    "ﺀﺎﻴﺣﻷﺍ ﻢﻠﻋ - ﺀﺎﻴﻤﻴﻜﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Chimie-Biologie",
    "ﺽﺭﻷﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de la Terre",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺽﺭﻷﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de la Terre",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﺽﺭﻷﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de la Terre",
    "ﺽﺭﻷﺍ ﻭ ﺓﺎﻴﺤﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de la Vie et de la Terre",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺽﺭﻷﺍ ﻭ ﺓﺎﻴﺤﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de la Vie et de la Terre",
    "ﻂﻴﺤﻤﻟﺍ ﻭ ﺀﺎﻴﺣﻷﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Biologie de l'Environnement",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﻂﻴﺤﻤﻟﺍ ﻭ ﺀﺎﻴﺣﻷﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Biologie de l'Environnement",
    "ﺩﺍﻮﻤﻟﺍ ﺀﺎﻳﺰﻴﻓ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Physique des Matériaux",
    "ﺔﻗﺎﻄﻟﺍ ﻭ ﺀﺎﻳﺰﻴﻔﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Physique et Énergie",
    "ﺎﻴﺟﻮﻟﻮﻨﻜﺗﻮﻴﺒﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Biotechnologie",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺎﻴﺟﻮﻟﻮﻨﻜﺗﻮﻴﺒﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Biotechnologie",
    "ﺕﺎﻘﻴﺒﻄﺘﻟﺍﻭ ﻚﻴﺗﺎﻣﻮﻴﺠﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Géomatique et Applications",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﺕﺎﻘﻴﺒﻄﺘﻟﺍﻭ ﻚﻴﺗﺎﻣﻮﻴﺠﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Géomatique et Applications",
    "ﺔﺌﻴﻬﺘﻟﺍ ﻭ ﺮﻴﻤﻌﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Urbanisme et Aménagement",
    "ﺔﺌﻴﻬﺘﻟﺍﻭ ﺔﺌﻴﺒﻟﺍﻭ ﻚﻴﺗﺎﻣﻮﻴﺠﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Géomatique, Environnement et Aménagement",
    "ﺔﺌﻴﻬﺘﻟﺍﻭ ﻚﻴﺗﺎﻣﻮﻴﺠﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Géomatique et Aménagement",
    "ﺔﺌﻴﺒﻟﺍ ﺔﻴﻓﺍﺮﻐﺟ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Géographie de l'Environnement",
    "ﺏﺍﺩﺁ ﺔﺌﻴﺒﻟﺍ ﺔﻴﻓﺍﺮﻐﺟ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Géographie de l'Environnement",

    # ── Ingénierie ──
    "ﺔــﻴـﺋﺎـﺑﺮـﻬﻜﻟﺍ ﺔـﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Génie Électrique",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﺔــﻴـﺋﺎـﺑﺮـﻬﻜﻟﺍ ﺔـﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Génie Électrique",
    "ﺔـﻴـﻜـﻴـﻧﺎﻜﻴﻤﻟﺍ ﺔـﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Génie Mécanique",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺔـﻴـﻜـﻴـﻧﺎﻜﻴﻤﻟﺍ ﺔـﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Génie Mécanique",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﺔـﻴـﻜـﻴـﻧﺎﻜﻴﻤﻟﺍ ﺔـﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Génie Mécanique",
    "ﺔﻴﻧﺪﻤﻟﺍ ﺔـﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Génie Civil",
    "ﺔﻴﻟﻵﺍﻭ ﺔﻴﻨﻘﺗﻭﺮﻬﻜﻟﺍﻭ ﻚﻴﻧﻭﺮﺘﻜﻟﻹﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Électronique, Électrotechnique et Automatique",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﺔﻴﻟﻵﺍﻭ ﺔﻴﻨﻘﺗﻭﺮﻬﻜﻟﺍﻭ ﻚﻴﻧﻭﺮﺘﻜﻟﻹﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Électronique, Électrotechnique et Automatique",
    "ﻚﻴﻧﺎﻜﻴﻣﻭﺮﺘﻜﻟﻹﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Électromécanique",
    "ﺔﻴﻘﻴﺒﻄﺗ ﺎﻴﺟﻮﻟﻮـﻴـﺑ - ﺀﺎـﻴـﻤـﻴـﻛ :ﺔﺠﻣﺪﻨﻣ ﺔﻳﺮﻴﻀﺤﺗ ﺔﻠﺣﺮﻣ": "Cycle Préparatoire Intégré : Chimie-Biologie Appliquée",
    "ﺐﻴﻟﺎﺳﻷﺍ ﺔﺳﺪﻨﻫ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Génie des Procédés",
    "ﺔﻴﻋﺎﻨﺼﻟﺍ ﺐﻴﻟﺎﺳﻷﺍ ﺔﺳﺪﻨﻫ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Génie des Procédés Industriels",
    "ﺔﻴﺒﻳﺮﺠﺗ ﻡﻮﻠﻋ ﺔﻴﻋﺎﻨﺼﻟﺍ ﺐﻴﻟﺎﺳﻷﺍ ﺔﺳﺪﻨﻫ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Génie des Procédés Industriels",
    "ﺔﻴﻋﺎﻨﺼﻟﺍ ﺔﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Génie Industriel",
    "ﺔﻴﻗﺎﻄﻟﺍ ﺔﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Génie Énergétique",
    "ﺓﺩﺪﺠﺘﻤﻟﺍ ﺕﺎﻗﺎﻄﻟﺍﻭ ﺔﻳﺭﺍﺮﺤﻟﺍ ﺔﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Génie Thermique et Énergies Renouvelables",
    "ﺔﻴﺘﺴﺟﻮﻠﻟﺍ ﺔﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Génie Logistique",
    "ﺞﻴﺴﻨﻟﺍ ﺔﺳﺪﻨﻫ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Génie Textile",
    "ﺔﻴﺒﻃﻮﻴﺒﻟﺍ ﺔﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Génie Biomédical",
    "ﺔﻴﻨﻘﺘﻟﺍ ﻡﻮﻠﻌﻟﺍ ﻚﻴﻧﺎﻜﻴﻣﻭﺭﺪﻴﻬﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Hydromécanique",
    "ﺔﺜﻳﺪﺤﻟﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍﻭ ﺕﻮﺼﻟﺍ ﺔﺳﺪﻨﻫ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Ingénierie du Son et Technologies Modernes",
    "ﺕﻮﺼﻟﺍ ﺕﺎﻴﻨﻘﺗﻭ ﺔﺳﺪﻨﻫ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Ingénierie et Techniques du Son",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺕﻮﺼﻟﺍ ﺕﺎﻴﻨﻘﺗﻭ ﺔﺳﺪﻨﻫ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Ingénierie et Techniques du Son",
    "ﻞﻘﻨﻟﺍ ﺔﺳﺪﻨﻫﻭ ﺎﻴﺟﻮﻟﻮﻨﻜﺗ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Technologie et Génie du Transport",
    "ﻞﻘﻨﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Sciences du Transport",
    "ﺔﻴﺗﺍﻭﺩﻷﺍﻭ ﺕﺎﺳﺎﻴﻘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Instrumentation et Mesure",

    # ── Santé ──
    "ﻂﻴﺤﻤﻟﺍﻭ ﺔﻳﺎﻗﻮﻟﺍﻭ ﺔﺤﺼﻟﺍ ﻆﻔﺣ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Hygiène, Sécurité et Environnement",
    "ﻡﻼﻜﻟﺍﻭ ﻖـﻄﻨﻟﺍ ﻢـﻳﻮﻘﺗ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Orthophonie",
    "ﺔﻳﺮﺸﺒﻟﺍ ﺔﻳﺬﻐﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Nutrition Humaine",
    "ﻞﻤﻌﻟﺎﺑ ﺝﻼﻌﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Ergothérapie",
    "ﻞﻔﻄﻠﻟ ﺔﻴﺤﺼﻟﺍ ﺔـﻳﺎـﻋﺮﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Soins de Santé Infantile",
    "ﺔﻠﺑﺎﻗ - ﺪـــﻴـﻟﻮــﺘـﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de l'Obstétrique - Sage-femme",
    "ﺙﺎﻧﺍ-ﺾﻳﺮﻤﺘﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences Infirmières (Femmes)",
    "ﺭﻮﻛﺫ-ﺾﻳﺮﻤﺘﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences Infirmières (Hommes)",
    "ﻲﻌﻴﺒﻄﻟﺍ ﺝﻼﻌﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Physiothérapie",
    "ﺏﺍﺩﺁ ﻲﻌﻴﺒﻄﻟﺍ ﺝﻼﻌﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Physiothérapie",
    "ﺔﻴﺒﻄﻟﺍ ﺎﻴﺟﻮﻟﻮﻴﺒﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Biologie Médicale",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺔﻴﺒﻄﻟﺍ ﺎﻴﺟﻮﻟﻮﻴﺒﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Biologie Médicale",
    "ﺔﻴﺒﻄﻟﺍ ﺎﻴﺟﻮﻟﻮﻨﻜﺗﻮﻴﺒﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Biotechnologie Médicale",
    "ﺔﻴﺒﻄﻟﺍ ﺕﺍﺭﺎﻈﻨﻟﺍ ﻭ ﺕﺎﻳﺮﺼﺒﻤﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Optique et Lunetterie Médicale",
    "ﺔﻌﺷﻷﺎﺑ ﺓﺍﻭﺍﺪﻤﻟﺍﻭ ﻲﺒﻄﻟﺍ ﺮﻳﻮﺼﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Imagerie Médicale et Radiothérapie",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺔﻌﺷﻷﺎﺑ ﺓﺍﻭﺍﺪﻤﻟﺍﻭ ﻲﺒﻄﻟﺍ ﺮﻳﻮﺼﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Imagerie Médicale et Radiothérapie",
    "ﺵﺎﻌﻧﻹﺍﻭ ﺞـﻴـﻨـﺒـﺘـﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Anesthésie et Réanimation",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺵﺎﻌﻧﻹﺍﻭ ﺞـﻴـﻨـﺒـﺘـﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Anesthésie et Réanimation",
    "ﺵﺎﻌﻧﻻﺍﻭ ﺔﻴﻟﺎﺠﻌﺘﺳﻹﺍ ﺔﻴﺤﺼﻟﺍ ﺔﻳﺎﻋﺮﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Soins d'Urgence et Réanimation",
    "ﺏﺍﺩﺁ ﺵﺎﻌﻧﻻﺍﻭ ﺔﻴﻟﺎﺠﻌﺘﺳﻹﺍ ﺔﻴﺤﺼﻟﺍ ﺔﻳﺎﻋﺮﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Soins d'Urgence et Réanimation",
    "ﺔﻴﺣﺍﺮﺠﻟﺍ ﺕﺎﻴﻠﻤﻌﻟﺍ ﺔﻋﺎﻗ ﺔﻴﺗﺍﻭﺩﺃ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Instrumentation du Bloc Opératoire",
    "ﻥﺎـﻨـﺳﻷﺍ ﻞﺋﺍﺪﺑ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Prothèse Dentaire",
    "ﻡﺎﻈﻌﻟﺍ ﺔﺣﺍﺮﺟ ﺓﺰﻬﺟﺃ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Appareillage Orthopédique",
    "ﻊﻤﺳ ﺔﻟﺁ ﻝﺎﻤﻌﺘﺳﺇ ﻭ ﺐﻴﻛﺮﺗ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Audioprothèse",
    "ﺔﻴﻨﻬﻤﻟﺍ ﺔﻣﻼﺴﻟﺍﻭ ﺔﺤﺼﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Santé et Sécurité au Travail",
    "ﻙﺭﺎﺤﺒﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de la Mer",
    "ﺙﺎﻧﺍ-ﺭﺎﺤﺒﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de la Mer (Femmes)",
    "ﺭﻮﻛﺫ-ﺭﺎﺤﺒﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de la Mer (Hommes)",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺭﺎﺤﺒﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de la Mer",

    # ── Éducation / Communication / Religion ──
    "ﻢﻴﻠﻌﺘﻟﺍﻭ ﺔﻴﺑﺮﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Éducation et Enseignement",
    "ﺔﻴﺑﺮﺘﻟﺍ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences de l'Éducation",
    "ﺔﺼﺘﺨﻤﻟﺍ ﺔﻴﺑﺮﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Éducation Spécialisée",
    "ﺔﻓﺎﺤﺼﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Journalisme",
    "ﻝﺎﺼﺗﻻﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Communication",
    "ﻒﻴﺷﺭﻷﺍﻭ ﺕﺎﺒﺘﻜﻤﻟﺍ ﻡﻮﻠﻋﻭ ﻖﻴﺛﻮﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Documentation, Bibliothéconomie et Archivistique",
    "ﻖﺋﺎﺛﻮﻟﺍ ﻭ ﺕﺎﻣﻮﻠﻌﻤﻟﺍ ﻲﻓ ﻲﻧﻭﺮﺘﻜﻟﻹﺍ ﻑﺮﺼﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Gestion Électronique de l'Information et des Documents",
    "ﺔﻴﻋﺮﺸﻟﺍ ﻡﻮﻠﻌﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences Religieuses",
    "ﺔﻴﻣﻼﺳﻹﺍ ﻡﻮﻠﻌﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences Islamiques",
    "ﺏﺍﺩﺁ ﺔﻴﻣﻼﺳﻹﺍ ﻡﻮﻠﻌﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences Islamiques",
    "ﻲﻣﻼﺳﻹﺍ ﺙﺍﺮﺘﻟﺍ ﻥﻮﻨﻓ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Arts du Patrimoine Islamique",
    "ﺏﺍﺩﺁ ﻲﻣﻼﺳﻹﺍ ﺙﺍﺮﺘﻟﺍ ﻥﻮﻨﻓ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Arts du Patrimoine Islamique",

    # ── Sport / Tourisme / Patrimoine ──
    "ﺔﺿﺎﻳﺮﻟﺍﻭ ﺔﻴﻧﺪﺒﻟﺍ ﺔﻄﺸﻧﻷﺍ ﺕﺎﻴﻨﻘﺗﻭ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en STAPS",
    "ﻂﻴﺸﻨﺘﻟﺍﻭ ﺔﻃﺎﺳﻮﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Médiation et Animation",
    "ﺔﺣﺎﻴﺴﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Tourisme",
    "ﺔﻗﺪﻨﻔﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Hôtellerie",
    "ﺏﺍﺩﺁ ﻲﺣﺎﻴﺴﻟﺍ ﻂﻴﺸﻨﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Animation Touristique",
    "ﻲﺣﺎﻴﺴﻟﺍ ﻂﻴﺸﻨﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Animation Touristique",
    "ﺎﻬﻤﻴﻣﺮﺗ ﻭ ﺔﻴﻓﺎﻘﺜﻟﺍ ﺕﺎﻜﻠﺘﻤﻤﻟﺍ ﻰﻠﻋ ﺔﻈﻓﺎﺤﻤﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Conservation et Restauration du Patrimoine Culturel",
    "ﺏﺍﺩﺁ ﺎﻬﻤﻴﻣﺮﺗ ﻭ ﺔﻴﻓﺎﻘﺜﻟﺍ ﺕﺎﻜﻠﺘﻤﻤﻟﺍ ﻰﻠﻋ ﺔﻈﻓﺎﺤﻤﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Conservation et Restauration du Patrimoine Culturel",
    "ﺔﻴﻓﺎﻘﺜﻟﺍ ﺕﺎﻜﻠﺘﻤﻤﻟﺍ ﻆﻔﺣ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Préservation du Patrimoine Culturel",
    "ﺏﺍﺩﺁ ﺔﻴﻓﺎﻘﺜﻟﺍ ﺕﺎﻜﻠﺘﻤﻤﻟﺍ ﻆﻔﺣ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Préservation du Patrimoine Culturel",
    "ﻡﺪﻘﻟﺍ ﻢﻳﺭﺪﺗﻭ ﺚﺤﺒﻣ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Football (Recherche et Entraînement)",

    # ── Agronomie / Alimentation ──
    "ﺔﻴﺣﻼﻔﻟﺍ ﻡﻮﻠﻌﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences Agronomiques",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺔﻴﺣﻼﻔﻟﺍ ﻡﻮﻠﻌﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences Agronomiques",
    "ﺔﻳﺬﻏﻷﺍ ﺕﺎﻴﻨﻘﺗﻭ ﻡﻮﻠﻋ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Sciences et Techniques Alimentaires",
    "ﺔﻴﺋﺍﺬﻐﻟﺍ ﺕﺎﻋﺎﻨﺼﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Industries Alimentaires",
    "ﻂﻴﺤﻤﻟﺍﻭ ﺔﻴﺋﺍﺬﻐﻟﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Technologies Alimentaires et Environnement",
    "ﺏﺍﺩﺁ ﻂﻴﺤﻤﻟﺍﻭ ﺔﻴﺋﺍﺬﻐﻟﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺘﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻹﺍ": "Licence en Technologies Alimentaires et Environnement",
    "ﺔﻴﻟﻭﺪﻟﺍ ﺕﺎﻗﻼﻌﻟﺍ ﻭ ﻚﻴﺘﻴﻟﻮﺑﻮﻴﺠﻟﺍ ﻲﻓ ﺓﺯﺎﺟﻻﺍ": "Licence en Géopolitique et Relations Internationales",
    "ﺔﺤﺼﻟﺍ ﺕﺎﻴﺟﻮﻟﻮﻨﻜﺗﻮﻴﺑ ﺔﺳﺪﻨﻫ ﻲﻓ ﺔﺠﻣﺪﻨﻣ ﺔﻳﺮﻴﻀﺤﺗ ﺔﻠﺣﺮﻣ": "Cycle Préparatoire Intégré en Génie Biotechnologie de la Santé",

    # ── Cycles Préparatoires ──
    "ﺔﻴﻤﻠﻋ ﺔﻳﺮﻴﻀﺤﺗ ﺔﻠﺣﺮﻣ": "Cycle Préparatoire Scientifique",
    "ﺔﻴﻤﻠﻋ-ﺔﺠﻣﺪﻨﻣ ﺔﻳﺮﻴﻀﺤﺗ ﺔﻠﺣﺮﻣ": "Cycle Préparatoire Intégré Scientifique",
    "ﺔﺠﻣﺪﻨﻣ ﺔﻳﺮﻴﻀﺤﺗ ﺔﻠﺣﺮﻣ": "Cycle Préparatoire Intégré",
    "ﺕﺎﻴﺿﺎﻳﺭ ﺔﺠﻣﺪﻨﻣ ﺔﻳﺮﻴﻀﺤﺗ ﺔﻠﺣﺮﻣ": "Cycle Préparatoire Intégré",
    "ﺎﻴﺟﻮﻟﻮﻨﻜﺗ - ﺔﻳﺮﻴﻀﺤﺗ ﺔﻠﺣﺮﻣ": "Cycle Préparatoire Technologique",
    "ﺎﻴﺟﻮﻟﻮﻴﺟ - ﺎﻴﺟﻮﻟﻮﻴﺑ :ﺔﻳﺮﻴﻀﺤﺗ ﺔﻠﺣﺮﻣ": "Cycle Préparatoire : Biologie-Géologie",
    "ﺔﻴﺒﻃﻮﻴﺒﻟﺍ ﺔﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺔﺠﻣﺪﻨﻣ ﺔﻳﺮﻴﻀﺤﺗ ﺔﻠﺣﺮﻣ": "Cycle Préparatoire Intégré en Génie Biomédical",
    "ﺔﻴﺒﻃﻮﻴﺒﻟﺍﻭ ﺔﻴﺟﻮﻟﻮﻴﺒﻟﺍ ﺔﺳﺪﻨﻬﻟﺍ ﻲﻓ ﺔﺠﻣﺪﻨﻣ ﺔﻳﺮﻴﻀﺤﺗ ﺔﻠﺣﺮﻣ": "Cycle Préparatoire Intégré en Génie Biologique et Biomédical",
    "ﺀﺎﻳﺰﻴﻓ - ﺕﺎﻴﺿﺎﻳﺭ:ﺔﻴﻤﻠﻌﻟﺍ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺔﻠﺣﺮﻤﻟﺍ": "Cycle Préparatoire Scientifique : Maths-Physique",
    "ﺀﺎﻴﻤﻴﻛ - ﺀﺎﻳﺰﻴﻓ :ﺔﻴﻤﻠﻌﻟﺍ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺔﻠﺣﺮﻤﻟﺍ": "Cycle Préparatoire Scientifique : Physique-Chimie",
    "ﺀﺎﻴﻤﻴﻛ -ﺀﺎﻳﺰﻴﻓ -ﺕﺎﻴﺿﺎﻳﺭ :ﺔﺠﻣﺪﻨﻣ ﺔﻳﺮﻴﻀﺤﺗ ﺔﻠﺣﺮﻣ": "Cycle Préparatoire Intégré : Maths-Physique-Chimie",
    "ﺔـﻴـﻣﻼﻋﺇ ﻭ ﺀﺎﻳﺰﻴﻓ -ﺕﺎﻴﺿﺎﻳﺭ :ﺔﺠﻣﺪﻨﻣ ﺔﻳﺮﻴﻀﺤﺗ ﺔﻠﺣﺮﻣ": "Cycle Préparatoire Intégré : Maths-Physique-Informatique",

    # ── Préparatoires Lettres ──
    "ﺔﻴﺑﺮﻋ:ﺏﺍﺩﻵﺍﻭ ﺕﺎﻐﻠﻟ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺔﻠﺣﺮﻤﻟﺍ": "Cycle Préparatoire Langues et Lettres : Arabe",
    "ﺏﺍﺩﺁ ﺔﻴﺑﺮﻋ:ﺏﺍﺩﻵﺍﻭ ﺕﺎﻐﻠﻟ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺔﻠﺣﺮﻤﻟﺍ": "Cycle Préparatoire Langues et Lettres : Arabe",
    "ﺔﻴﺴﻧﺮﻓ:ﺏﺍﺩﻵﺍﻭ ﺕﺎﻐﻠﻟ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺔﻠﺣﺮﻤﻟﺍ": "Cycle Préparatoire Langues et Lettres : Français",
    "ﺏﺍﺩﺁ ﺔﻴﺴﻧﺮﻓ:ﺏﺍﺩﻵﺍﻭ ﺕﺎﻐﻠﻟ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺔﻠﺣﺮﻤﻟﺍ": "Cycle Préparatoire Langues et Lettres : Français",
    "ﺔﻳﺰﻴﻠﻘﻧﺍ:ﺏﺍﺩﻵﺍﻭ ﺕﺎﻐﻠﻟ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺔﻠﺣﺮﻤﻟﺍ": "Cycle Préparatoire Langues et Lettres : Anglais",
    "ﺦﻳﺭﺎﺗ:ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻠﻟ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺔﻠﺣﺮﻤﻟﺍ": "Cycle Préparatoire Sciences Humaines : Histoire",
    "ﺏﺍﺩﺁ ﺦﻳﺭﺎﺗ:ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻠﻟ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺔﻠﺣﺮﻤﻟﺍ": "Cycle Préparatoire Sciences Humaines : Histoire",
    "ﺎﻴﻓﺍﺮﻐﺟ:ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻠﻟ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺔﻠﺣﺮﻤﻟﺍ": "Cycle Préparatoire Sciences Humaines : Géographie",
    "ﺔﻔﺴﻠﻓ:ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻠﻟ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺔﻠﺣﺮﻤﻟﺍ": "Cycle Préparatoire Sciences Humaines : Philosophie",
    "ﺏﺍﺩﺁ ﺔﻔﺴﻠﻓ:ﺔﻴﻧﺎﺴﻧﻹﺍ ﻡﻮﻠﻌﻠﻟ ﺔﻳﺮﻴﻀﺤﺘﻟﺍ ﺔﻠﺣﺮﻤﻟﺍ": "Cycle Préparatoire Sciences Humaines : Philosophie",
}


def translate_csv():
    """Apply Arabic -> French translations to the CSV."""
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    print(f"Loaded {len(df)} rows")

    # Translate Etablissement_AR -> Etablissement
    def translate_etab(ar):
        return ETAB_MAP.get(ar, ar)

    # Translate Filiere_AR -> Filiere
    def translate_filiere(ar):
        return FILIERE_MAP.get(ar, ar)

    df["Etablissement"] = df["Etablissement_AR"].apply(translate_etab)
    df["Filiere"] = df["Filiere_AR"].apply(translate_filiere)

    # Check untranslated
    untranslated_etab = df[df["Etablissement"] == df["Etablissement_AR"]]["Etablissement_AR"].unique()
    untranslated_fil = df[df["Filiere"] == df["Filiere_AR"]]["Filiere_AR"].unique()

    print(f"\nÉtablissements non traduits: {len(untranslated_etab)}")
    for e in untranslated_etab:
        print(f"  [{e}]")

    print(f"\nFilières non traduites: {len(untranslated_fil)}")
    for f in untranslated_fil:
        print(f"  [{f}]")

    # Reorder columns: put French first, keep Arabic
    cols = [
        "Code_Filiere", "Universite", "Etablissement", "Filiere",
        "Section_Bac", "Section_Bac_Nom",
        "Score_2022", "Score_2023", "Score_2024", "Score_2025",
        "Etablissement_AR", "Filiere_AR",
    ]
    df = df[cols]

    # Save
    df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
    print(f"\nSauvegardé: {CSV_PATH}")
    print(f"Colonnes: {list(df.columns)}")
    print(f"\nAperçu:")
    print(df[["Code_Filiere", "Etablissement", "Filiere", "Section_Bac"]].head(15).to_string())


if __name__ == "__main__":
    translate_csv()
