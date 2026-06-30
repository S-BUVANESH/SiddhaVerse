import json
import os

def generate():
    benchmark_data = {
        "version": "3B-R",
        "queries": []
    }
    
    queries = []
    
    # === 1. Tamil Verse Queries (20) ===
    tamil_verses = [
        ("நினைப்பதொன்று கண்டிலேன்", ["sivavakkiyar_pm_0616"], "Tamil Verse"),
        ("ஓடிஓடி ஓடிஓடி உட்கலந்த", ["sivavakkiyar_pm_0612"], "Tamil Verse"),
        ("ஞான நிலை என்னிலே இருந்த", ["sivavakkiyar_pm_0615"], "Tamil Verse"),
        ("மண்ணும்நீ அவ்விண்ணும்நீ", ["sivavakkiyar_pm_0617"], "Tamil Verse"),
        ("நாலுவேதம் ஓதுவீர் ஞானபாதம்", ["sivavakkiyar_pm_0623"], "Tamil Verse"),
        ("சங்கிரண்டு தாரை ஒன்று", ["sivavakkiyar_pm_0628"], "Tamil Verse"),
        ("நீளவீடு கட்டுறீர் நெடுங்கதவு", ["sivavakkiyar_pm_0631"], "Tamil Verse"),
        ("வித்தில்லாத சம்பிரதாயம்", ["sivavakkiyar_pm_0624"], "Tamil Verse"),
        ("ஓடம்உள்ள போதெல்லாம் நீர்", ["sivavakkiyar_pm_0632"], "Tamil Verse"),
        ("தங்கம்ஒன்று ரூபம்வேறு தன்மையான", ["sivavakkiyar_pm_0638"], "Tamil Verse"),
        ("உருத்தரித்த நாடியில்", ["sivavakkiyar_pm_0613"], "Tamil Verse"),
        ("அஞ்செழுத்திலே பிறந்து", ["sivavakkiyar_pm_0629"], "Tamil Verse"),
        ("அதிசயம் பலபலவுமாய்", ["classic_agasthiyar_vaidya_kaviyam"], "Tamil Verse"),
        ("அனாதிமுன் அனாதியாய்", ["sivavakkiyar_pm_0616"], "Tamil Verse"),
        ("அஞ்சும்மூணும் எட்டாதாய்", ["sivavakkiyar_pm_0625"], "Tamil Verse"),
        ("பண்டுநான் பறித்தெறிந்த", ["sivavakkiyar_pm_0635"], "Tamil Verse"),
        ("அண்டவாசல் ஆயிரம்", ["sivavakkiyar_pm_0626"], "Tamil Verse"),
        ("சரியை கிரியை யோக", ["sivavakkiyar_pm_0612"], "Tamil Verse"),
        ("காப்பு அரியதோர் நமச்சிவாயம்", ["sivavakkiyar_pm_0609"], "Tamil Verse"),
        ("கரியதோர் முகத்தையொத்த", ["sivavakkiyar_pm_0610"], "Tamil Verse")
    ]
    for q_text, expected, cat in tamil_verses:
        queries.append({
            "query_id": f"q{len(queries) + 1:03d}",
            "category": cat,
            "query_text": q_text,
            "expected_documents": expected,
            "relevance_scores": {doc: 1.0 for doc in expected}
        })
        
    # === 2. Romanized Queries (20) ===
    romanized = [
        ("pranayamam", ["classic_thirumandiram", "sivavakkiyar_pm_0616"], "Romanized Suffix"),
        ("kumbhakam", ["sivavakkiyar_pm_0616"], "Romanized Suffix"),
        ("namasivaya", ["sivavakkiyar_pm_0609"], "Romanized Suffix"),
        ("odi odi odi odi", ["sivavakkiyar_pm_0612"], "Romanized Suffix"),
        ("vaasi yogam", ["classic_thirumandiram", "sivavakkiyar_pm_0613"], "Romanized Suffix"),
        ("kayakalpa rejuvenation", ["classic_agasthiyar_soumya_sagaram", "formulation_brahma_rasayanam"], "Romanized Suffix"),
        ("pancha boothas", ["sivavakkiyar_pm_0617"], "Romanized Suffix"),
        ("siddhar yoga", ["classic_thirumandiram"], "Romanized Suffix"),
        ("anathi mun anathiyay", ["sivavakkiyar_pm_0616"], "Romanized Suffix"),
        ("thangam ondru roobam veru", ["sivavakkiyar_pm_0638"], "Romanized Suffix"),
        ("vetrilai mooligai", ["plant_karisalankanni"], "Romanized Suffix"), # karisalankanni is a herb
        ("kabasura kudineer", ["formulation_kabasura_kudineer"], "Romanized Suffix"),
        ("nilavembu decoction", ["formulation_nilavembu_kudineer", "plant_nilavembu"], "Romanized Suffix"),
        ("amukkara choornam", ["formulation_amukkara_choornam"], "Romanized Suffix"),
        ("siddhar bogar", ["siddhar_bogar", "classic_bogar_7000"], "Romanized Suffix"),
        ("agasthiyar kuzhambu", ["formulation_agasthiyar_kuzhambu", "siddhar_agasthiyar"], "Romanized Suffix"),
        ("thirumoolar thirumandiram", ["classic_thirumandiram"], "Romanized Suffix"),
        ("karuvoorar pooja", ["classic_karuvoorar_pooja_vidhi", "siddhar_karuvoorar"], "Romanized Suffix"),
        ("seenthil chooranam", ["formulation_seenthil_chooranam", "plant_seenthil"], "Romanized Suffix"),
        ("sivavakkiyam complete", ["classic_sivavakkiyar_padalgal"], "Romanized Suffix")
    ]
    for q_text, expected, cat in romanized:
        queries.append({
            "query_id": f"q{len(queries) + 1:03d}",
            "category": cat,
            "query_text": q_text,
            "expected_documents": expected,
            "relevance_scores": {doc: 1.0 for doc in expected}
        })
        
    # === 3. English Synonym Queries (20) ===
    english_synonyms = [
        ("breath retention", ["classic_thirumandiram", "sivavakkiyar_pm_0616"], "English Synonym"),
        ("holy basil", ["plant_tulsi", "plant_karunthulasi"], "English Synonym"),
        ("indian gooseberry", ["plant_nelli"], "English Synonym"),
        ("ginger decoction", ["plant_inji___sukku"], "English Synonym"),
        ("green chiretta", ["plant_nilavembu", "formulation_nilavembu_kudineer"], "English Synonym"),
        ("black pepper", ["plant_milagu"], "English Synonym"),
        ("garlic cloves", ["plant_poondu"], "English Synonym"),
        ("cardamom spice", ["plant_elakkai"], "English Synonym"),
        ("malabar nut", ["plant_adathodai"], "English Synonym"),
        ("stonebreaker herb", ["plant_keelanelli", "plant_keezhanelli"], "English Synonym"),
        ("alchemical mercury", ["classic_agasthiyar_soumya_sagaram", "formulation_siddha_makaradhwaja"], "English Synonym"),
        ("respiratory herbal drink", ["formulation_kabasura_kudineer"], "English Synonym"),
        ("joint pain remedy", ["plant_mudakathan"], "English Synonym"),
        ("winter cherry", ["plant_ashwagandha", "formulation_amukkara_choornam"], "English Synonym"),
        ("licorice root", ["plant_athimathuram"], "English Synonym"),
        ("rejuvenating herbal paste", ["formulation_brahma_rasayanam"], "English Synonym"),
        ("cosmic illusion", ["sivavakkiyar_pm_0616"], "English Synonym"),
        ("rejuvenation therapy kayakalpa", ["classic_agasthiyar_soumya_sagaram", "formulation_brahma_rasayanam"], "English Synonym"),
        ("breath control exercises", ["classic_thirumandiram", "sivavakkiyar_pm_0613"], "English Synonym"),
        ("indian pennywort", ["plant_brahmi___neerbrahmi"], "English Synonym")
    ]
    for q_text, expected, cat in english_synonyms:
        queries.append({
            "query_id": f"q{len(queries) + 1:03d}",
            "category": cat,
            "query_text": q_text,
            "expected_documents": expected,
            "relevance_scores": {doc: 1.0 for doc in expected}
        })
        
    # === 4. Entity Queries (20) ===
    entities = [
        ("Agasthiyar", ["siddhar_agasthiyar", "classic_agasthiyar_soumya_sagaram"], "Entity Search"),
        ("Thirumoolar", ["classic_thirumandiram"], "Entity Search"),
        ("Bogar", ["siddhar_bogar", "classic_bogar_7000"], "Entity Search"),
        ("Sivavakkiyar", ["classic_sivavakkiyar_padalgal"], "Entity Search"),
        ("Theriyar", ["classic_theriyar_sekarappa", "classic_theriyar_yamaga_venba"], "Entity Search"),
        ("Karuvoorar", ["siddhar_karuvoorar", "classic_karuvoorar_pooja_vidhi"], "Entity Search"),
        ("Korakkar", ["siddhar_korakkar_bio", "siddhar_korakkar"], "Entity Search"),
        ("Pambatti Siddhar", ["siddhar_pambatti_siddhar"], "Entity Search"),
        ("Thirumandiram book", ["classic_thirumandiram"], "Entity Search"),
        ("Sivavakkiyam book", ["classic_sivavakkiyar_padalgal"], "Entity Search"),
        ("Green Chiretta plant", ["plant_nilavembu"], "Entity Search"),
        ("Malabar Nut plant", ["plant_adathodai"], "Entity Search"),
        ("Ashwagandha plant", ["plant_ashwagandha"], "Entity Search"),
        ("Brahmi plant", ["plant_brahmi___neerbrahmi"], "Entity Search"),
        ("Karisalankanni plant", ["plant_karisalankanni"], "Entity Search"),
        ("Kabasura Kudineer recipe", ["formulation_kabasura_kudineer"], "Entity Search"),
        ("Nilavembu Kudineer formulation", ["formulation_nilavembu_kudineer"], "Entity Search"),
        ("Amukkara Choornam recipe", ["formulation_amukkara_choornam"], "Entity Search"),
        ("Brahma Rasayanam formulation", ["formulation_brahma_rasayanam"], "Entity Search"),
        ("Siddha Makaradhwaja recipe", ["formulation_siddha_makaradhwaja"], "Entity Search")
    ]
    for q_text, expected, cat in entities:
        queries.append({
            "query_id": f"q{len(queries) + 1:03d}",
            "category": cat,
            "query_text": q_text,
            "expected_documents": expected,
            "relevance_scores": {doc: 1.0 for doc in expected}
        })
        
    # === 5. Concept / Formulation / Biography Queries (20) ===
    concepts = [
        ("alchemical mercury purification", ["classic_agasthiyar_soumya_sagaram", "formulation_siddha_makaradhwaja"], "Concept/Formulation/Biography"),
        ("siddha formulation for respiratory fever", ["formulation_kabasura_kudineer"], "Concept/Formulation/Biography"),
        ("Agasthiyar alchemical cosmology and Kayakalpa", ["siddhar_agasthiyar", "classic_agasthiyar_soumya_sagaram"], "Concept/Formulation/Biography"),
        ("Thirumoolar yogic breath control philosophy", ["classic_thirumandiram"], "Concept/Formulation/Biography"),
        ("treatment for joint pain mudakathan", ["plant_mudakathan"], "Concept/Formulation/Biography"),
        ("brahma rasayanam preparation and dosage", ["formulation_brahma_rasayanam"], "Concept/Formulation/Biography"),
        ("Siddhar Bogar travels and medical findings", ["siddhar_bogar", "classic_bogar_7000"], "Concept/Formulation/Biography"),
        ("amukkara choornam indications and use", ["formulation_amukkara_choornam"], "Concept/Formulation/Biography"),
        ("Siddha herb for liver protection and jaundice", ["plant_keelanelli", "plant_keezhanelli"], "Concept/Formulation/Biography"),
        ("preparation of kalyana ghritham", ["formulation_kalyana_ghritham"], "Concept/Formulation/Biography"),
        ("Agasthiyar Kuzhambu composition and purgative uses", ["formulation_agasthiyar_kuzhambu"], "Concept/Formulation/Biography"),
        ("Pathartha Guna Chinthamani dietary guidelines", ["classic_pathartha_guna_chinthamani"], "Concept/Formulation/Biography"),
        ("rejuvenation through mercury and sulfur", ["formulation_siddha_makaradhwaja"], "Concept/Formulation/Biography"),
        ("nilavembu kudineer preparation and dengue fever", ["formulation_nilavembu_kudineer", "plant_nilavembu"], "Concept/Formulation/Biography"),
        ("Yugi Chinthamani classification of diseases", ["classic_yugi_chinthamani_800"], "Concept/Formulation/Biography"),
        ("Pambatti Siddhar spiritual and kundalini philosophy", ["siddhar_pambatti_siddhar"], "Concept/Formulation/Biography"),
        ("Korakkar biography and use of cannabis", ["siddhar_korakkar_bio", "siddhar_korakkar"], "Concept/Formulation/Biography"),
        ("Karuvoorar puja protocols and copper work", ["siddhar_karuvoorar", "classic_karuvoorar_pooja_vidhi"], "Concept/Formulation/Biography"),
        ("Sivavakkiyar critique of rituals and temple structures", ["classic_sivavakkiyar_padalgal", "sivavakkiyar_pm_0612"], "Concept/Formulation/Biography"),
        ("Siddha Materia Medica plant classification", ["plant_seenthil", "plant_adathodai"], "Concept/Formulation/Biography")
    ]
    for q_text, expected, cat in concepts:
        queries.append({
            "query_id": f"q{len(queries) + 1:03d}",
            "category": cat,
            "query_text": q_text,
            "expected_documents": expected,
            "relevance_scores": {doc: 1.0 for doc in expected}
        })
        
    # === 6. Adversarial Queries (20) ===
    adversarial = [
        # Misspellings (5)
        ("pranyama breathing", ["classic_thirumandiram", "sivavakkiyar_pm_0616"], "Adversarial"),
        ("algastiar medicine", ["siddhar_agasthiyar", "classic_agasthiyar_soumya_sagaram"], "Adversarial"),
        ("thulasi plant", ["plant_tulsi", "plant_karunthulasi"], "Adversarial"),
        ("kabasura kudiner recipe", ["formulation_kabasura_kudineer"], "Adversarial"),
        ("tiromular yoga", ["classic_thirumandiram"], "Adversarial"),
        # Ambiguous terms (5)
        ("oil", ["formulation_chandanadi_thailam", "formulation_chirattai_thailam", "formulation_pinda_thailam"], "Adversarial"),
        ("breath", ["classic_thirumandiram", "sivavakkiyar_pm_0616", "sivavakkiyar_pm_0613"], "Adversarial"),
        ("root", ["plant_ashwagandha", "plant_athimathuram", "plant_inji___sukku"], "Adversarial"),
        ("rejuvenation", ["classic_agasthiyar_soumya_sagaram", "formulation_brahma_rasayanam"], "Adversarial"),
        ("fever", ["formulation_kabasura_kudineer", "formulation_nilavembu_kudineer"], "Adversarial"),
        # Multi-intent queries (3)
        ("kayakalpa rejuvenation in agasthiyar and thirumandiram", ["classic_agasthiyar_soumya_sagaram", "classic_thirumandiram"], "Adversarial"),
        ("tulsi plant and nilavembu kudineer", ["plant_tulsi", "plant_karunthulasi", "formulation_nilavembu_kudineer"], "Adversarial"),
        ("agasthiyar kuzhambu and amukkara choornam", ["formulation_agasthiyar_kuzhambu", "formulation_amukkara_choornam"], "Adversarial"),
        # Unrelated/Out-of-Scope questions (4)
        ("what is the capital of France?", [], "Adversarial"),
        ("how to cook pasta?", [], "Adversarial"),
        ("latest iPhone price", [], "Adversarial"),
        ("how does python build lists?", [], "Adversarial"),
        # Very short queries (3)
        ("va", [], "Adversarial"),
        ("o", [], "Adversarial"),
        ("si", [], "Adversarial")
    ]
    for q_text, expected, cat in adversarial:
        queries.append({
            "query_id": f"q{len(queries) + 1:03d}",
            "category": cat,
            "query_text": q_text,
            "expected_documents": expected,
            "relevance_scores": {doc: 1.0 for doc in expected}
        })
        
    benchmark_data["queries"] = queries
    
    output_path = r"d:\Siddha_Wisdom\expanded_benchmark_ground_truth.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=2, ensure_ascii=False)
        
    print(f"Generated 120-query ground-truth benchmark suite at: {output_path}")

if __name__ == "__main__":
    generate()
