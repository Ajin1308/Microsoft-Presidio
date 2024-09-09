from presidio_analyzer import AnalyzerEngine

def analyze(text,entities):
    # Set up the engine, loads the NLP module (spaCy model by default) 
    # and other PII recognizers
    analyzer = AnalyzerEngine()

    # Call analyzer to get results
    results = analyzer.analyze(text=text,
                               entities=entities,
                            language='en')
    print(results)
    return results