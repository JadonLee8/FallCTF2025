import regex
import re
from collections import Counter

# Read the emoji string from restart_magnum.py
with open('restart_magnum.py', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('"') + 1
    end = content.rfind('"')
    emojis = content[start:end]

# Split into grapheme clusters
graphemes = regex.findall(r'\X', emojis)

print("Total graphemes:", len(graphemes))

# Let me try position 10 which looked promising
pos = 10
print(f"\nAnalyzing position {pos}: {graphemes[pos:pos+6]}")

base_map = {
    graphemes[pos]: 'g',      # First 'g'
    graphemes[pos+1]: 'i',    # 'i'
    graphemes[pos+2]: 'g',    # Second 'g' (should be same emoji as pos)
    graphemes[pos+3]: 'e',    # 'e'
    graphemes[pos+4]: 'm',    # 'm'
    graphemes[pos+5]: '{',    # '{'
}

# Verify pos and pos+2 are the same
if graphemes[pos] != graphemes[pos+2]:
    print("WARNING: Position 0 and 2 don't match!")
    print(f"  pos: {graphemes[pos]}")
    print(f"  pos+2: {graphemes[pos+2]}")
    # Use the correct pattern
    base_map[graphemes[pos]] = 'g'
    base_map[graphemes[pos+2]] = 'g'

print("\nBase mapping:")
for emoji, letter in sorted(set(base_map.items()), key=lambda x: x[1]):
    print(f"  {repr(emoji)} -> {letter}")

# Get frequency
freq = Counter(graphemes)

# Map remaining by frequency
# English: e,t,a,o,i,n,s,h,r,d,l,c,u,m,w,f,g,y,p,b,v,k,x,q,j,z
english_order = list('etaoinshrdlcuwfgypbvkxqjz_., ')

extended_map = base_map.copy()
unmapped_emojis = [e for e, _ in freq.most_common() if e not in extended_map]
unmapped_letters = [l for l in english_order if l not in extended_map.values()]

for emoji, letter in zip(unmapped_emojis, unmapped_letters):
    extended_map[emoji] = letter

# Decode
decoded = ''.join([extended_map.get(g, g) for g in graphemes])

# Find flags
print("\n" + "="*80)
print("Searching for flags...")
print("="*80)

# Look around the original position
start_search = max(0, pos - 20)
end_search = min(len(decoded), pos + 300)
snippet = decoded[start_search:end_search]

print(f"Decoded text around position {pos}:")
print(snippet)
print()

# Find gigem{ in the snippet
matches = list(re.finditer(r'gigem\{[^}]{10,100}\}', decoded))
if matches:
    print(f"Found {len(matches)} potential flag candidates:")
    for i, match in enumerate(matches[:5]):
        flag = match.group(0)
        inner = flag[6:-1]
        
        # Count different character types
        alpha = sum(1 for c in inner if c.isalpha())
        underscore = inner.count('_')
        other = len(inner) - alpha - underscore
        
        print(f"\n{i+1}. {flag}")
        print(f"   Length: {len(inner)}, Alpha: {alpha}, Underscores: {underscore}, Other: {other}")
        
        # Check if it's mostly clean
        if other < len(inner) * 0.2:  # Less than 20% non-standard chars
            print(f"   → GOOD CANDIDATE!")

# Try all positions that have g_g pattern
print("\n" + "="*80)
print("Trying all g_g pattern positions...")
print("="*80)

candidates = []
for start in range(len(graphemes) - 5):
    if graphemes[start] == graphemes[start+2]:
        test_map = {
            graphemes[start]: 'g',
            graphemes[start+1]: 'i',
            graphemes[start+3]: 'e',
            graphemes[start+4]: 'm',
            graphemes[start+5]: '{',
        }
        
        # Try to find closing brace within 100 chars
        for end_pos in range(start+7, min(start+100, len(graphemes))):
            if graphemes[end_pos] not in test_map:
                test_map2 = test_map.copy()
                test_map2[graphemes[end_pos]] = '}'
                
                # Decode this section
                section = graphemes[start:end_pos+1]
                decoded_section = ''.join([test_map2.get(g, '?') for g in section])
                
                # Check if it matches gigem{...}
                if decoded_section.startswith('gigem{') and decoded_section.endswith('}'):
                    inner = decoded_section[6:-1]
                    unknowns = inner.count('?')
                    
                    # If less than 30% unknown, this might be good
                    if unknowns < len(inner) * 0.3:
                        candidates.append((start, end_pos, decoded_section, unknowns, len(inner)))

# Sort by least unknowns
candidates.sort(key=lambda x: x[3] / x[4])

print(f"\nFound {len(candidates)} candidates with <30% unknowns")
print("Top 10 candidates:")
for i, (start, end, decoded_section, unknowns, length) in enumerate(candidates[:10]):
    pct = 100 * unknowns / length if length > 0 else 100
    print(f"\n{i+1}. Position {start}-{end} ({length} chars, {unknowns} unknown = {pct:.1f}%)")
    print(f"   {decoded_section}")
