from presidio_anonymizer import AnonymizerEngine


def anonymize(text, analyzer_results):
    anonymizer = AnonymizerEngine()

    anonymized_text = anonymizer.anonymize(text=text,analyzer_results=analyzer_results)
    print(anonymized_text)

    return anonymized_text