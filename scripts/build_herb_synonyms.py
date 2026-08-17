#!/usr/bin/env python3
"""
Build herb_synonyms.json from existing 10 herb profiles + glossary
Maps: Sanskrit names ↔ Botanical name ↔ Common names
"""
import json
import os
import re
from pathlib import Path

ROOT = Path("/home/shiva/ayurshakti.shop")

# Known mappings from existing 10 profiles (ground truth)
GROUND_TRUTH = {
    "ashwagandha": {
        "botanical": "Withania somnifera",
        "sanskrit": ["Ashwagandha", "Varada", "Balada", "Turagagandha", "Hayahvaya"],
        "hindi": ["Ashwagandha", "Asgandh"],
        "english": ["Indian Ginseng", "Winter Cherry", "Poison Gooseberry"],
        "tamil": ["Amukkara"],
        "telugu": ["Penneru"],
        "arabic": ["Kaknaj-e-Hindi"],
        "chinese": ["Nanyinren", "Suan Zao Ren"],
        "family": "Solanaceae"
    },
    "shatavari": {
        "botanical": "Asparagus racemosus",
        "sanskrit": ["Shatavari", "Shatamuli", "Bahusuta", "Naraya", "Atirasa"],
        "hindi": ["Shatavari", "Satavari"],
        "english": ["Wild Asparagus", "Asparagus Root"],
        "family": "Asparagaceae"
    },
    "giloy": {
        "botanical": "Tinospora cordifolia",
        "sanskrit": ["Guduchi", "Amrita", "Chhinnaruha", "Vayastha", "Vishalya"],
        "hindi": ["Giloy", "Gurach", "Gurcha"],
        "english": ["Heart-leaved Moonseed", "Indian Tinospora", "Heavenly Elixir"],
        "tamil": ["Seenthil Kodi"],
        "telugu": ["Tippa Teega"],
        "arabic": ["Gilo-e-Hindi"],
        "chinese": ["Ku Mu Teng"],
        "family": "Menispermaceae"
    },
    "triphala": {
        "botanical": "Triphala (3-fruit blend)",
        "sanskrit": ["Triphala", "Vara", "Phala"],
        "components": ["amalaki", "haritaki", "bibhitaki"],
        "is_combination": True
    },
    "brahmi": {
        "botanical": "Bacopa monnieri",
        "sanskrit": ["Brahmi", "Sarasvati", "Jalanimba", "Somavalli"],
        "hindi": ["Brahmi", "Jalanimba"],
        "english": ["Water Hyssop", "Herb of Grace"],
        "family": "Plantaginaceae"
    },
    "tulsi": {
        "botanical": "Ocimum sanctum",
        "sanskrit": ["Tulsi", "Surasa", "Gramya", "Sulabha", "Bahumanjari"],
        "hindi": ["Tulsi", "Holy Basil"],
        "english": ["Holy Basil", "Sacred Basil"],
        "family": "Lamiaceae"
    },
    "turmeric": {
        "botanical": "Curcuma longa",
        "sanskrit": ["Haridra", "Kanchani", "Nisha", "Gauri", "Krimighni"],
        "hindi": ["Haldi", "Haridra"],
        "english": ["Turmeric", "Indian Saffron"],
        "family": "Zingiberaceae"
    },
    "amalaki": {
        "botanical": "Phyllanthus emblica",
        "sanskrit": ["Amalaki", "Dhatri", "Amrita", "Shriphala", "Tishyaphala"],
        "hindi": ["Amla", "Amalaki"],
        "english": ["Indian Gooseberry", "Emblic Myrobalan"],
        "family": "Phyllanthaceae"
    },
    "haritaki": {
        "botanical": "Terminalia chebula",
        "sanskrit": ["Haritaki", "Abhaya", "Pathya", "Vijaya", "Chetaki"],
        "hindi": ["Harad", "Haritaki"],
        "english": ["Chebulic Myrobalan", "Black Myrobalan"],
        "family": "Combretaceae"
    },
    "bibhitaki": {
        "botanical": "Terminalia bellirica",
        "sanskrit": ["Bibhitaki", "Vibhitaki", "Aksha", "Karshaphala"],
        "hindi": ["Bahera", "Bibhitaki"],
        "english": ["Beleric Myrobalan", "Bastard Myrobalan"],
        "family": "Combretaceae"
    }
}

# Additional herbs from glossary + classical texts
ADDITIONAL_HERBS = {
    "arjuna": {"botanical": "Terminalia arjuna", "sanskrit": ["Arjuna", "Kakubha", "Veeravriksha"], "family": "Combretaceae"},
    "guggulu": {"botanical": "Commiphora mukul", "sanskrit": ["Guggulu", "Devadhupa", "Mahishaksha"], "family": "Burseraceae"},
    "punarnava": {"botanical": "Boerhavia diffusa", "sanskrit": ["Punarnava", "Shothaghni", "Kathillaka"], "family": "Nyctaginaceae"},
    "manjishtha": {"botanical": "Rubia cordifolia", "sanskrit": ["Manjishtha", "Samanga", "Lohitamanjari"], "family": "Rubiaceae"},
    "neem": {"botanical": "Azadirachta indica", "sanskrit": ["Nimba", "Arishta", "Pichumarda"], "family": "Meliaceae"},
    "kutki": {"botanical": "Picrorhiza kurroa", "sanskrit": ["Katuki", "Katurohini", "Rohini"], "family": "Plantaginaceae"},
    "bhumyamalaki": {"botanical": "Phyllanthus niruri", "sanskrit": ["Bhumyamalaki", "Bahupatra", "Tamalaki"], "family": "Phyllanthaceae"},
    "shilajit": {"botanical": "Asphaltum punjabianum", "sanskrit": ["Shilajatu", "Silajatu", "Girija"], "family": "Mineral"},
    "pippali": {"botanical": "Piper longum", "sanskrit": ["Pippali", "Magadhi", "Upakunchika"], "family": "Piperaceae"},
    "shankhpushpi": {"botanical": "Convolvulus pluricaulis", "sanskrit": ["Shankhpushpi", "MangalyaKusuma"], "family": "Convolvulaceae"},
    "jatamansi": {"botanical": "Nardostachys jatamansi", "sanskrit": ["Jatamansi", "Bhutajata", "Tapasvini"], "family": "Caprifoliaceae"},
    "kapikacchu": {"botanical": "Mucuna pruriens", "sanskrit": ["Kapikacchu", "Atmagupta", "Markati"], "family": "Fabaceae"},
    "vidarikanda": {"botanical": "Pueraria tuberosa", "sanskrit": ["Vidarikanda", "Bhumikushmanda", "Ikshugandha"], "family": "Fabaceae"},
    "bala": {"botanical": "Sida cordifolia", "sanskrit": ["Bala", "Mahabala", "Atibala"], "family": "Malvaceae"},
    "dashmool": {"botanical": "Dashmool (10-root blend)", "sanskrit": ["Dashmoola", "Dashamula"], "components": ["bilva","agnimantha","shyonaka","patala","gambhari","brihati","kantakari","gokshura","shalaparni","prishniparni"], "is_combination": True},
    "kantakari": {"botanical": "Solanum xanthocarpum", "sanskrit": ["Kantakari", "Vyaghri", "Kshudra"], "family": "Solanaceae"},
    "vasaka": {"botanical": "Justicia adhatoda", "sanskrit": ["Vasaka", "Arusha", "Vasira"], "family": "Acanthaceae"},
    "khadir": {"botanical": "Acacia catechu", "sanskrit": ["Khadira", "Gayatri", "Raktasara"], "family": "Fabaceae"},
    "sariva": {"botanical": "Hemidesmus indicus", "sanskrit": ["Sariva", "Anantamula", "Gopi"], "family": "Apocynaceae"},
    "yashtimadhu": {"botanical": "Glycyrrhiza glabra", "sanskrit": ["Yashtimadhu", "Madhuka", "Klitaka"], "family": "Fabaceae"},
    "musta": {"botanical": "Cyperus rotundus", "sanskrit": ["Musta", "Kuruvinda", "Gandhahrina"], "family": "Cyperaceae"},
    "chitraka": {"botanical": "Plumbago zeylanica", "sanskrit": ["Chitraka", "Agni", "Vahni"], "family": "Plumbaginaceae"},
    "kutaja": {"botanical": "Holarrhena antidysenterica", "sanskrit": ["Kutaja", "Vatsaka", "Girimalika"], "family": "Apocynaceae"},
    "bilva": {"botanical": "Aegle marmelos", "sanskrit": ["Bilva", "Shivadruma", "Maloora"], "family": "Rutaceae"},
    "ashoka": {"botanical": "Saraca asoca", "sanskrit": ["Ashoka", "Hemapushpa", "Kankeli"], "family": "Fabaceae"},
    "lodhra": {"botanical": "Symplocos racemosa", "sanskrit": ["Lodhra", "Tilvaka", "Shavara"], "family": "Symplocaceae"},
    "gokshura": {"botanical": "Tribulus terrestris", "sanskrit": ["Gokshura", "Trikantaka", "SvaduKantaka"], "family": "Zygophyllaceae"},
    "jyotishmati": {"botanical": "Celastrus paniculatus", "sanskrit": ["Jyotishmati", "Malkangani", "Katabhi"], "family": "Celastraceae"},
    "kushmanda": {"botanical": "Benincasa hispida", "sanskrit": ["Kushmanda", "Brihatphala", "Pushtiphala"], "family": "Cucurbitaceae"},
    "karkati": {"botanical": "Cucumis anguria", "sanskrit": ["Karkati", "Chirbhita"], "family": "Cucurbitaceae"},
    "kalambi": {"botanical": "Mitragyna parvifolia", "sanskrit": ["Kalambi", "Kadambaka"], "family": "Rubiaceae"},
    "kadali": {"botanical": "Musa paradisiaca", "sanskrit": ["Kadali", "Rambha", "Kadalika"], "family": "Musaceae"},
}

# Load glossary terms for additional Sanskrit names
def load_glossary_terms():
    glossary_dir = ROOT / "content" / "glossary"
    terms = {}
    for f in glossary_dir.glob("glossary_*.json"):
        try:
            with open(f) as fp:
                data = json.load(fp)
                for term in data.get("terms", []):
                    if isinstance(term, dict) and "term" in term:
                        t = term["term"].lower().strip()
                        if t not in terms:
                            terms[t] = term.get("definition", "")
        except:
            pass
    return terms

def main():
    # Merge all herbs
    all_herbs = {}
    all_herbs.update(GROUND_TRUTH)
    all_herbs.update(ADDITIONAL_HERBS)
    
    # Build synonyms index
    synonyms = {
        "by_slug": {},
        "by_botanical": {},
        "by_sanskrit": {},
        "by_hindi": {},
        "by_english": {},
        "combination_formulas": {}
    }
    
    for slug, data in all_herbs.items():
        synonyms["by_slug"][slug] = data
        
        # Botanical mapping
        if "botanical" in data:
            synonyms["by_botanical"][data["botanical"].lower()] = slug
        
        # Sanskrit names
        for name in data.get("sanskrit", []):
            synonyms["by_sanskrit"][name.lower()] = slug
        
        # Hindi names
        for name in data.get("hindi", []):
            synonyms["by_hindi"][name.lower()] = slug
            
        # English names
        for name in data.get("english", []):
            synonyms["by_english"][name.lower()] = slug
        
        # Combination formulas
        if data.get("is_combination"):
            synonyms["combination_formulas"][slug] = data.get("components", [])
    
    # Save
    output = ROOT / "data" / "herb_synonyms.json"
    with open(output, "w") as f:
        json.dump(synonyms, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Built herb_synonyms.json with {len(synonyms['by_slug'])} herbs")
    print(f"   Sanskrit names: {len(synonyms['by_sanskrit'])}")
    print(f"   Combination formulas: {len(synonyms['combination_formulas'])}")
    print(f"   Output: {output}")

if __name__ == "__main__":
    main()
