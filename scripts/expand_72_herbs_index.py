#!/usr/bin/env python3
"""
Expand data/herb_index.json to cover 72 classical Ayurvedic botanicals and formulations.
"""

import json
from pathlib import Path

ROOT = Path("/home/shiva/ayurshakti.shop")
INDEX_FILE = ROOT / "data" / "herb_index.json"

with open(INDEX_FILE, encoding="utf-8") as f:
    herb_index = json.load(f)

NEW_30_HERBS = {
    "nagakesar": {
        "botanical_name": "Mesua ferrea",
        "family": "Calophyllaceae",
        "all_sanskrit_names": ["Nagakesara", "Nagapushpa", "Champeya"],
        "hindi_names": ["Nagkesar"],
        "english_names": ["Ceylon Ironwood", "Cobra Saffron"],
        "tamil_names": ["Nagamalligai"],
        "telugu_names": ["Nagakesaramu"],
        "arabic_names": ["Narkaysar"],
        "chinese_names": ["Tie-li-mu"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "tagara": {
        "botanical_name": "Valeriana wallichii",
        "family": "Caprifoliaceae",
        "all_sanskrit_names": ["Tagara", "Kalanusari", "Nard"],
        "hindi_names": ["Tagar", "Mushkbala"],
        "english_names": ["Indian Valerian"],
        "tamil_names": ["Tagarai"],
        "telugu_names": ["Tagara"],
        "arabic_names": ["Asarun"],
        "chinese_names": ["Yindu-baizao"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "vacha": {
        "botanical_name": "Acorus calamus",
        "family": "Acoraceae",
        "all_sanskrit_names": ["Vacha", "Ugragandha", "Shadgrantha"],
        "hindi_names": ["Bach", "Vach"],
        "english_names": ["Sweet Flag", "Calamus"],
        "tamil_names": ["Vasambu"],
        "telugu_names": ["Vasa"],
        "arabic_names": ["Waj"],
        "chinese_names": ["Shui-chang-pu"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "bhringraj": {
        "botanical_name": "Eclipta alba",
        "family": "Asteraceae",
        "all_sanskrit_names": ["Bhringaraja", "Kesharaaja", "Markava"],
        "hindi_names": ["Bhringraj", "Bhangra"],
        "english_names": ["False Daisy"],
        "tamil_names": ["Karisalankanni"],
        "telugu_names": ["Gunta-galagaraku"],
        "arabic_names": ["Bhrangaraj"],
        "chinese_names": ["Mo-han-lian"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Chikitsa Sthana Ch. 26"}]
    },
    "shunthi": {
        "botanical_name": "Zingiber officinale",
        "family": "Zingiberaceae",
        "all_sanskrit_names": ["Shunthi", "Nagara", "Vishvabhesaja"],
        "hindi_names": ["Sonth", "Adrak"],
        "english_names": ["Dry Ginger"],
        "tamil_names": ["Sukku"],
        "telugu_names": ["Sonthi"],
        "arabic_names": ["Zanjabil"],
        "chinese_names": ["Gan-jiang"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "maricha": {
        "botanical_name": "Piper nigrum",
        "family": "Piperaceae",
        "all_sanskrit_names": ["Maricha", "Vellaja", "Kolu"],
        "hindi_names": ["Kali Mirch"],
        "english_names": ["Black Pepper"],
        "tamil_names": ["Milagu"],
        "telugu_names": ["Miriyalu"],
        "arabic_names": ["Filfil Aswad"],
        "chinese_names": ["Hei-hu-jiao"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "ela": {
        "botanical_name": "Elettaria cardamomum",
        "family": "Zingiberaceae",
        "all_sanskrit_names": ["Sukshma Ela", "Truti", "Korangi"],
        "hindi_names": ["Chhoti Elaichi"],
        "english_names": ["Green Cardamom"],
        "tamil_names": ["Elakkai"],
        "telugu_names": ["Yelakulu"],
        "arabic_names": ["Hel"],
        "chinese_names": ["Xiao-dou-kou"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "tvak": {
        "botanical_name": "Cinnamomum zeylanicum",
        "family": "Lauraceae",
        "all_sanskrit_names": ["Tvak", "Darusita", "Chocha"],
        "hindi_names": ["Dalchini"],
        "english_names": ["Ceylon Cinnamon"],
        "tamil_names": ["Lavangam"],
        "telugu_names": ["Dalchina Chekka"],
        "arabic_names": ["Qurfah"],
        "chinese_names": ["Rou-gui"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "tejpatra": {
        "botanical_name": "Cinnamomum tamala",
        "family": "Lauraceae",
        "all_sanskrit_names": ["Tejpatra", "Patra", "Tamalapatra"],
        "hindi_names": ["Tejpatta"],
        "english_names": ["Indian Bay Leaf"],
        "tamil_names": ["Talishapatri"],
        "telugu_names": ["Akupatri"],
        "arabic_names": ["Sazaj"],
        "chinese_names": ["Yindu-gui-ye"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "lavanga": {
        "botanical_name": "Syzygium aromaticum",
        "family": "Myrtaceae",
        "all_sanskrit_names": ["Lavanga", "Devakusuma", "Shrisangya"],
        "hindi_names": ["Laung"],
        "english_names": ["Clove"],
        "tamil_names": ["Krambu"],
        "telugu_names": ["Lavangalu"],
        "arabic_names": ["Qaranful"],
        "chinese_names": ["Ding-xiang"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "jatiphala": {
        "botanical_name": "Myristica fragrans",
        "family": "Myristicaceae",
        "all_sanskrit_names": ["Jatiphala", "Malatiphala", "Jati"],
        "hindi_names": ["Jaiphal"],
        "english_names": ["Nutmeg"],
        "tamil_names": ["Jathikai"],
        "telugu_names": ["Jajikaya"],
        "arabic_names": ["Jauz al- الطيب"],
        "chinese_names": ["Rou-dou-kou"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "dhanyaka": {
        "botanical_name": "Coriandrum sativum",
        "family": "Apiaceae",
        "all_sanskrit_names": ["Dhanyaka", "Dhaniyaka", "Chhatra"],
        "hindi_names": ["Dhaniyaka", "Dhania"],
        "english_names": ["Coriander"],
        "tamil_names": ["Kothamalli"],
        "telugu_names": ["Dhaniyalu"],
        "arabic_names": ["Kuzbarah"],
        "chinese_names": ["Yuan-sui"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "jiraka": {
        "botanical_name": "Cuminum cyminum",
        "family": "Apiaceae",
        "all_sanskrit_names": ["Jiraka", "Gaura-Jiraka", "Ajaji"],
        "hindi_names": ["Jeera"],
        "english_names": ["Cumin"],
        "tamil_names": ["Seeragam"],
        "telugu_names": ["Jilakarra"],
        "arabic_names": ["Kammon"],
        "chinese_names": ["Zi-ran"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "methika": {
        "botanical_name": "Trigonella foenum-graecum",
        "family": "Fabaceae",
        "all_sanskrit_names": ["Methika", "Kunchika", "Bahupatrika"],
        "hindi_names": ["Methi"],
        "english_names": ["Fenugreek"],
        "tamil_names": ["Vendhayam"],
        "telugu_names": ["Mentulu"],
        "arabic_names": ["Hulbah"],
        "chinese_names": ["Hu-lu-ba"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "yavani": {
        "botanical_name": "Trachyspermum ammi",
        "family": "Apiaceae",
        "all_sanskrit_names": ["Yavani", "Dipiyaka", "Ugragandha"],
        "hindi_names": ["Ajwain"],
        "english_names": ["Bishop's Weed", "Carom Seeds"],
        "tamil_names": ["Omam"],
        "telugu_names": ["Vamu"],
        "arabic_names": ["Nanakhwah"],
        "chinese_names": ["Yindu-cang-zhu"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "shatapushpa": {
        "botanical_name": "Anethum sowa",
        "family": "Apiaceae",
        "all_sanskrit_names": ["Shatapushpa", "Shaleya", "Karavi"],
        "hindi_names": ["Soya", "Saunf"],
        "english_names": ["Indian Dill"],
        "tamil_names": ["Sadhakuppi"],
        "telugu_names": ["Shatagopamu"],
        "arabic_names": ["Shibth"],
        "chinese_names": ["Yindu-dill"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "chandana": {
        "botanical_name": "Santalum album",
        "family": "Santalaceae",
        "all_sanskrit_names": ["Shweta Chandana", "Bhadrashriya", "Shrikhanda"],
        "hindi_names": ["Sandalwood", "Chandan"],
        "english_names": ["White Sandalwood"],
        "tamil_names": ["Chandanam"],
        "telugu_names": ["Gandhamu"],
        "arabic_names": ["Sandal Abiyad"],
        "chinese_names": ["Tan-xiang"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "raktachandana": {
        "botanical_name": "Pterocarpus santalinus",
        "family": "Fabaceae",
        "all_sanskrit_names": ["Rakta Chandana", "Raktanga", "Kshudrachandana"],
        "hindi_names": ["Lal Chandan"],
        "english_names": ["Red Sanders", "Red Sandalwood"],
        "tamil_names": ["Santhana maram"],
        "telugu_names": ["Yerra Chandanam"],
        "arabic_names": ["Sandal Ahmar"],
        "chinese_names": ["Zi-tan"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "agaru": {
        "botanical_name": "Aquilaria agallocha",
        "family": "Thymelaeaceae",
        "all_sanskrit_names": ["Agaru", "Loha", "Krimija"],
        "hindi_names": ["Agar"],
        "english_names": ["Agarwood", "Aloeswood"],
        "tamil_names": ["Aggalichandanam"],
        "telugu_names": ["Aguru"],
        "arabic_names": ["Oudh"],
        "chinese_names": ["Chen-xiang"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "usheera": {
        "botanical_name": "Vetiveria zizanioides",
        "family": "Poaceae",
        "all_sanskrit_names": ["Usheera", "Reshira", "Amrinaala"],
        "hindi_names": ["Khas", "Khus"],
        "english_names": ["Vetiver"],
        "tamil_names": ["Vettiver"],
        "telugu_names": ["Vattiveru"],
        "arabic_names": ["Izkhir"],
        "chinese_names": ["Xiang-gen-cao"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "latakasturi": {
        "botanical_name": "Abelmoschus moschatus",
        "family": "Malvaceae",
        "all_sanskrit_names": ["Latakasturi", "Kasturibhendi", "Gandhapura"],
        "hindi_names": ["Kasturi Bhendi"],
        "english_names": ["Musk Mallow"],
        "tamil_names": ["Kasturi Vendai"],
        "telugu_names": ["Kasturi Bhendi"],
        "arabic_names": ["Habb al-Musk"],
        "chinese_names": ["麝香葵"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "nimba": {
        "botanical_name": "Azadirachta indica var",
        "family": "Meliaceae",
        "all_sanskrit_names": ["Nimba", "Pichumarda", "Arishta"],
        "hindi_names": ["Neem"],
        "english_names": ["Margosa Tree"],
        "tamil_names": ["Veppam"],
        "telugu_names": ["Vepa"],
        "arabic_names": ["Azad Dirakht"],
        "chinese_names": ["Yindu-lian"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "bakuchi": {
        "botanical_name": "Psoralea corylifolia",
        "family": "Fabaceae",
        "all_sanskrit_names": ["Bakuchi", "Avalguja", "Somaraji"],
        "hindi_names": ["Bavachi"],
        "english_names": ["Psoralea Seeds"],
        "tamil_names": ["Karpokarisi"],
        "telugu_names": ["Bavanchalu"],
        "arabic_names": ["Bawachi"],
        "chinese_names": ["Bu-gu-zhi"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Chikitsa Sthana Ch. 7"}]
    },
    "karanja": {
        "botanical_name": "Pongamia pinnata",
        "family": "Fabaceae",
        "all_sanskrit_names": ["Karanja", "Naktamala", "Gurcha"],
        "hindi_names": ["Kanji", "Karanj"],
        "english_names": ["Indian Beech"],
        "tamil_names": ["Pungai"],
        "telugu_names": ["Kanuga"],
        "arabic_names": ["Karanj"],
        "chinese_names": ["Yindu-shui-huang-pi"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "gunja": {
        "botanical_name": "Abrus precatorius",
        "family": "Fabaceae",
        "all_sanskrit_names": ["Gunja", "Raktika", "Kakananti"],
        "hindi_names": ["Ratti", "Gunchi"],
        "english_names": ["Rosary Pea", "Jequirity"],
        "tamil_names": ["Gundumani"],
        "telugu_names": ["Gurivinda"],
        "arabic_names": ["Ain al-Afrit"],
        "chinese_names": ["Xiang-si-dou"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Chikitsa Sthana Ch. 26"}]
    },
    "dhataki": {
        "botanical_name": "Woodfordia fruticosa",
        "family": "Lythraceae",
        "all_sanskrit_names": ["Dhataki", "Bahupushpi", "Tamrapushpi"],
        "hindi_names": ["Dhai", "Dhataki"],
        "english_names": ["Fire Flame Bush"],
        "tamil_names": ["Dhataki"],
        "telugu_names": ["Dhataki"],
        "arabic_names": ["Dhataki"],
        "chinese_names": ["Yindu-huo-yan-shu"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "kumari": {
        "botanical_name": "Aloe vera",
        "family": "Asphodelaceae",
        "all_sanskrit_names": ["Kumari", "Ghritakumari", "Kanya"],
        "hindi_names": ["Ghee Kanwar", "Aloe Vera"],
        "english_names": ["Aloe Vera", "Indian Aloe"],
        "tamil_names": ["Katraazhai"],
        "telugu_names": ["Kalabanda"],
        "arabic_names": ["Sabbar"],
        "chinese_names": ["Lu-hui"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Chikitsa Sthana Ch. 15"}]
    },
    "isabgol": {
        "botanical_name": "Plantago ovata",
        "family": "Plantaginaceae",
        "all_sanskrit_names": ["Ishadgola", "Snigdhajira", "Ashwakarna"],
        "hindi_names": ["Isabgol"],
        "english_names": ["Psyllium Husk"],
        "tamil_names": ["Ishappukol"],
        "telugu_names": ["Isabgolu"],
        "arabic_names": ["Baspagul"],
        "chinese_names": ["Yindu-che-qian-zi"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "shallaki": {
        "botanical_name": "Boswellia serrata",
        "family": "Burseraceae",
        "all_sanskrit_names": ["Shallaki", "Gajabhakshya", "Surabhi"],
        "hindi_names": ["Salai Guggul", "Salai"],
        "english_names": ["Indian Frankincense", "Boswellia"],
        "tamil_names": ["Parangipattai"],
        "telugu_names": ["Anduga"],
        "arabic_names": ["Luban"],
        "chinese_names": ["Yindu-ru-xiang"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    },
    "eranda": {
        "botanical_name": "Ricinus communis",
        "family": "Euphorbiaceae",
        "all_sanskrit_names": ["Eranda", "Gandharvahasta", "Rubu"],
        "hindi_names": ["Arandi"],
        "english_names": ["Castor Oil Plant"],
        "tamil_names": ["Amanakku"],
        "telugu_names": ["Aamudamu"],
        "arabic_names": ["Khirwa"],
        "chinese_names": ["Bi-ma"],
        "classical_refs": [{"source": "Charaka Samhita", "chapter": "Sutra Sthana Ch. 4"}]
    }
}

herb_index.update(NEW_30_HERBS)

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    json.dump(herb_index, f, indent=2)

print(f"🎉 Successfully expanded data/herb_index.json to {len(herb_index)} total herbs!")
