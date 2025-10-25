
def find_possibilities(chars):
    # given a list of chars, with $ representing a unique unknown, and # representing a char that is the same as other # chars, and known characters represented by their letters, find the possible words
    import string
    
    possibilities = []
    word_length = len(chars)
    
    # Try to load a word list from various sources
    words = []
    
    # Try NLTK words corpus
    try:
        import nltk
        try:
            from nltk.corpus import words as nltk_words
            words = [w.lower() for w in nltk_words.words() if len(w) == word_length]
            print(f"Loaded {len(words)} words from NLTK")
        except LookupError:
            print("NLTK words corpus not downloaded. Downloading...")
            nltk.download('words', quiet=True)
            from nltk.corpus import words as nltk_words
            words = [w.lower() for w in nltk_words.words() if len(w) == word_length]
            print(f"Loaded {len(words)} words from NLTK")
    except ImportError:
        print("NLTK not installed. Install with: pip install nltk")
        print("Using empty word list for now.")
        words = []
    
    # Find positions of each symbol type
    hash_positions = [i for i, c in enumerate(chars) if c == '#']
    dollar_positions = [i for i, c in enumerate(chars) if c == '$']
    known_positions = {i: c.lower() for i, c in enumerate(chars) if c not in ['$', '#']}
    
    for word in words:
        word = word.lower()
        if len(word) != word_length:
            continue
            
        # Check known positions match
        if not all(word[i] == known_positions[i] for i in known_positions):
            continue
        
        # Check all # positions have the same character
        if hash_positions:
            hash_char = word[hash_positions[0]]
            if not all(word[i] == hash_char for i in hash_positions):
                continue
        
        # Check all $ positions have unique characters (different from each other)
        if dollar_positions:
            dollar_chars = [word[i] for i in dollar_positions]
            if len(dollar_chars) != len(set(dollar_chars)):
                continue
        
        # Check that $ chars don't overlap with # chars
        if hash_positions and dollar_positions:
            hash_char = word[hash_positions[0]]
            dollar_chars = [word[i] for i in dollar_positions]
            if hash_char in dollar_chars:
                continue
        
        possibilities.append(word)
    
    return possibilities

if __name__ == "__main__":
    chars = ['$', '#', '$', '$', '$', 'o', 'g', '#', '$', 'm']
    results = find_possibilities(chars)
    print(f"Found {len(results)} possibilities:")
    for word in results[:20]:  # Show first 20
        print(f"  {word}")
    if len(results) > 20:
        print(f"  ... and {len(results) - 20} more")