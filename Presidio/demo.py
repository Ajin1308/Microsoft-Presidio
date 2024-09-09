import re
from faker import Faker
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern


fake = Faker()
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

document = """Date: October 19, 2021
 Witness: John Doe
 Subject: Testimony Regarding the Loss of Wallet
 Testimony Content:
 Hello Officer,
 My name is John Doe and on October 19, 2021, my wallet was stolen in the vicinity of Kilmarnock during a bike trip. This wallet contains some very important things to me.
 Firstly, the wallet contains my credit card with number 4111 1111 1111 1111, which is registered under my name and linked to my bank account, PL61109010140000071219812874.
 Additionally, the wallet had a driver's license - DL No: 999000680 issued to my name. It also houses my Social Security Number, 602-76-4532.
 What's more, I had my polish identity card there, with the number ABC123456.
 I would like this data to be secured and protected in all possible ways. I believe It was stolen at 9:30 AM.
 In case any information arises regarding my wallet, please reach out to me on my phone number, 999-888-7777, or through my personal email, johndoe@example.com.
 Please consider this information to be highly confidential and respect my privacy.
 The bank has been informed about the stolen credit card and necessary actions have been taken from their end. They will be reachable at their official email, support@bankname.com.
 My representative there is Victoria Cherry (her business phone: 987-654-3210).
 Thank you for your assistance,
 John Doe"""


def analyze(text):
    analyzer_results = analyzer.analyze(text=text, language="en")
    results = []
    for res in analyzer_results:
        # Append the entire result object to the results list
        results.append(res)
        
    return results

analyzer_results = analyze(document)



def anonymize(text, analyzer_results):
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=analyzer_results)
    print(anonymized_text)


anonymize(document, analyzer_results)




def anonymize_polish_id(text):
    # Define the pattern for Polish ID
    polish_id_pattern = Pattern(
        name="polish_id_pattern",
        regex="[A-Z]{3}\d{6}",
        score=1.0,
    )
    
    # Create a recognizer using the defined pattern
    polish_id_recognizer = PatternRecognizer(
        supported_entity="POLISH_ID", patterns=[polish_id_pattern]
    )
    
    # Initialize the AnalyzerEngine and AnonymizerEngine
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    
    # Add the custom recognizer to the analyzer's registryS
    analyzer.registry.add_recognizer(polish_id_recognizer)
    
    # Analyze the text to detect entities
    analyzer_results = analyzer.analyze(text=text, language="en")
    
    # Anonymize the detected entities in the text
    anonymized_results = anonymizer.anonymize(
        text=text,
        analyzer_results=analyzer_results,
    )

    print(anonymized_results.text)


anonymize_polish_id(document)