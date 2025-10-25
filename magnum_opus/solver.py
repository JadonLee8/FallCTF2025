import regex  # pip install regex (supports grapheme clusters)
from collections import Counter

def solve_magnum_opus():
    # Read the emoji text
    with open("magnum_opus.txt", "r", encoding="utf-8") as file:
        text = file.read()
    
    # Split into grapheme clusters (visual characters including multi-codepoint emojis)
    graphemes = regex.findall(r'\X', text)
    
    print(f"Total graphemes: {len(graphemes)}")
    print(f"Unique graphemes: {len(set(graphemes))}")
    
    # Find the flag format "gigem{" 
    # Look for a pattern where positions match: g-i-g-e-m-{
    # positions 0,2 should be the same (g)
    # positions 1 is i
    # position 3 is e  
    # position 4 is m
    # position 5 is {
    
    candidates = []
    for i in range(len(graphemes) - 5):
        if graphemes[i] == graphemes[i+2]:  # g matches g
            candidate_start = i
            # Extract potential "gigem{"
            pattern = graphemes[i:i+6]
            candidates.append((candidate_start, pattern))
    
    print(f"\nFound {len(candidates)} potential 'gigem{{' patterns")
    
    # Build initial mapping from the most likely candidate
    # We'll use frequency analysis and context to find the right one
    best_mapping = None
    best_decoded = None
    
    for start_pos, pattern in candidates:
        # Create initial mapping based on "gigem{"
        mapping = {
            pattern[0]: 'g',  # g
            pattern[1]: 'i',  # i
            pattern[3]: 'e',  # e
            pattern[4]: 'm',  # m
            pattern[5]: '{',  # {
        }
        
        # Check if this makes sense - the opening brace shouldn't appear elsewhere in common words
        # Let's do a partial decode and see if it looks reasonable
        partial_decode = decode_with_mapping(graphemes, mapping)
        
        # Look for the closing brace
        if '}' in [mapping.get(g, g) for g in graphemes]:
            # Already has }, this might be good
            candidates_with_brace = [(start_pos, pattern, mapping)]
        else:
            # Try to find closing brace - it should be near the end
            for j in range(len(graphemes) - 1, max(start_pos, len(graphemes) - 100), -1):
                test_mapping = mapping.copy()
                test_mapping[graphemes[j]] = '}'
                test_decode = decode_with_mapping(graphemes, test_mapping)
                
                # Check if this creates a reasonable flag
                if 'gigem{' in test_decode and '}' in test_decode:
                    flag_match = extract_flag(test_decode)
                    if flag_match and is_valid_flag(flag_match):
                        mapping = test_mapping
                        break
        
        decoded = decode_with_mapping(graphemes, mapping)
        
        # Score this candidate
        score = score_decode(decoded, mapping)
        
        if best_mapping is None or score > score_decode(best_decoded, best_mapping):
            best_mapping = mapping
            best_decoded = decoded
            print(f"\nNew best candidate at position {start_pos}:")
            print(f"Pattern: {pattern}")
            print(f"Score: {score}")
    
    print("\n" + "="*80)
    print("INITIAL MAPPING (from 'gigem{' pattern):")
    print("="*80)
    for emoji, letter in sorted(best_mapping.items(), key=lambda x: x[1]):
        print(f"{emoji} -> {letter}")
    
    # Now use frequency analysis to extend the mapping
    print("\n" + "="*80)
    print("FREQUENCY ANALYSIS:")
    print("="*80)
    
    emoji_freq = Counter(graphemes)
    print("\nTop 20 most frequent emojis:")
    for emoji, count in emoji_freq.most_common(20):
        mapped = best_mapping.get(emoji, '?')
        print(f"{emoji}: {count} times -> {mapped}")
    
    # Common English letter frequencies (approximate)
    # e, t, a, o, i, n, s, h, r are most common
    english_freq = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b']
    
    # Map remaining frequent emojis to common letters
    unmapped_emojis = [emoji for emoji, _ in emoji_freq.most_common() if emoji not in best_mapping]
    unmapped_letters = [letter for letter in english_freq if letter not in best_mapping.values()]
    
    # Extend mapping using frequency
    extended_mapping = best_mapping.copy()
    for emoji, letter in zip(unmapped_emojis[:len(unmapped_letters)], unmapped_letters):
        extended_mapping[emoji] = letter
    
    # Decode with extended mapping
    decoded_text = decode_with_mapping(graphemes, extended_mapping)
    
    print("\n" + "="*80)
    print("DECODED TEXT (partial):")
    print("="*80)
    print(decoded_text[:500])
    
    # Extract flag
    flag = extract_flag(decoded_text)
    if flag:
        print("\n" + "="*80)
        print("FOUND FLAG:")
        print("="*80)
        print(flag)
    else:
        print("\n" + "="*80)
        print("No complete flag found. Let's try a smarter approach...")
        print("="*80)
        
        # Try to find flag by looking for gigem{ ... } pattern
        decoded_text = decode_with_mapping(graphemes, best_mapping)
        print(f"\nPartially decoded text:\n{decoded_text[:1000]}")
        
        # Find all occurrences of gigem{
        import re
        gigem_positions = [m.start() for m in re.finditer(r'gigem\{', decoded_text)]
        print(f"\nFound 'gigem{{' at positions: {gigem_positions}")
        
        for pos in gigem_positions:
            # Look for closing brace within reasonable distance
            end_search = min(pos + 200, len(decoded_text))
            for i in range(pos + 6, end_search):
                if decoded_text[i] == '}':
                    potential_flag = decoded_text[pos:i+1]
                    print(f"\nPotential flag: {potential_flag}")
                    if is_valid_flag(potential_flag):
                        return potential_flag
    
    return flag

def decode_with_mapping(graphemes, mapping):
    """Decode graphemes using the given mapping"""
    decoded = []
    for g in graphemes:
        decoded.append(mapping.get(g, g))
    return ''.join(decoded)

def extract_flag(text):
    """Extract flag from decoded text"""
    import re
    match = re.search(r'gigem\{[a-z_]+\}', text)
    if match:
        return match.group(0)
    return None

def is_valid_flag(flag):
    """Check if flag looks valid (only lowercase and underscores)"""
    import re
    return bool(re.match(r'gigem\{[a-z_]+\}$', flag))

def score_decode(decoded, mapping):
    """Score a decoded text based on how reasonable it looks"""
    if not decoded:
        return 0
    
    score = 0
    
    # Check if we have gigem{
    if 'gigem{' in decoded:
        score += 100
    
    # Check if we have closing brace
    if '}' in decoded:
        score += 50
    
    # Check for common English words
    common_words = ['the', 'and', 'was', 'for', 'that', 'with', 'have', 'this']
    for word in common_words:
        score += decoded.lower().count(word) * 10
    
    # Penalize if too many unknown emojis remain
    unknown_count = sum(1 for c in decoded if len(c) > 1)  # emojis are multi-byte
    score -= unknown_count * 0.1
    
    return score

if __name__ == "__main__":
    flag = solve_magnum_opus()
    if flag:
        print("\n" + "="*80)
        print("FINAL ANSWER:")
        print("="*80)
        print(flag)
