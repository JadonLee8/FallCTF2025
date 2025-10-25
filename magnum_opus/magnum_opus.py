import regex  # pip install regex (supports grapheme clusters)

def find_candidates():
    file = open("magnum_opus.txt", "r", encoding="utf-8")
    text = file.read()
    
    # split into grapheme clusters (visual characters including multi-codepoint emojis)
    graphemes = regex.findall(r'\X', text)
    
    candidates = []
    for i in range(2, len(graphemes)):
        if graphemes[i] == graphemes[i-2]:
            # join 40 graphemes starting from i-2
            candidate = ''.join(graphemes[i-2:i+40])
            candidates.append(candidate)
    
    for candidate in candidates:
        emojis = regex.findall(r'\X', candidate)
        translation = {
            emojis[0]: 'g',
            emojis[1]: 'i',
            emojis[3]: 'e',
            emojis[4]: 'm',
            emojis[5]: '{'
        }
        # if the 6th emoji in the candidate is in the translation dict, remove it from the candidates list
        if emojis[5] in translation:
            candidates.remove(candidate)
        #if the 6th emoji '{' shows up, shorten the candidate to only include up to and including that emoji
        if emojis[5] in translation:
            index = candidate.index(emojis[5]) + len(emojis[5])
            candidate = candidate[:index]
    return candidates

if __name__ == "__main__":
    candidates = find_candidates()
    print(f"Found {len(candidates)} candidates.")

    for candidate in candidates:
        print(candidate)
    # the first emoji represents g, the second i, the fourth e, and the fifth m.
    # everytime one of these emojis appears, replace it with one of these letters. do this for each candidate

