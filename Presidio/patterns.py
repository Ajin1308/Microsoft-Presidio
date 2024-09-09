from presidio_analyzer import PatternRecognizer, Pattern


def add_patterns(name, regex, score):
    pattern = Pattern(name=name, 
                      regex=regex, 
                      score = score)
    pattern_recognizer = PatternRecognizer(
        supported_entity= name,
        patterns= [pattern]
    )

    return pattern_recognizer