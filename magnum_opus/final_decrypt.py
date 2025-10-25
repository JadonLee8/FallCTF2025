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

# Based on analysis, position 830 has the best "gigem{" pattern
# Let's build a comprehensive mapping using multiple clues

# Start with position 830
pos830 = 830
base_map = {
    graphemes[pos830]: 'g',      
    graphemes[pos830+1]: 'i',    
    graphemes[pos830+2]: 'g',   # Same as pos830, confirms 'g'
    graphemes[pos830+3]: 'e',    
    graphemes[pos830+4]: 'm',    
    graphemes[pos830+5]: '{',    
}

print("\nBase mapping from position 830:")
for emoji, letter in sorted(base_map.items(), key=lambda x: x[1]):
    print(f"  {repr(emoji)} -> {letter}")

# Now let's use frequency analysis to fill in more letters
freq = Counter(graphemes)
print(f"\nTop 40 most frequent emojis:")
for emoji, count in freq.most_common(40):
    letter = base_map.get(emoji, '?')
    print(f"  {repr(emoji)}: {count} times -> {letter}")

# English letter frequency: e, t, a, o, i, n, s, h, r, d, l, c, u, m, w, f, g, y, p, b
# Map remaining high-frequency emojis
# We already have: g, i, e, m from base_map

# Build extended mapping based on frequency and common words
extended_map = base_map.copy()

# Get unmapped emojis by frequency
unmapped = [(emoji, count) for emoji, count in freq.most_common() if emoji not in extended_map]

# Common English letters (excluding those we have: g,i,e,m)
remaining_letters = list('taonshrdlcuwfypbvkxqjz_')

# Map by frequency
for (emoji, count), letter in zip(unmapped[:len(remaining_letters)], remaining_letters):
    extended_map[emoji] = letter

# Decode the entire text
decoded = ''.join([extended_map.get(g, g) for g in graphemes])

# Search for gigem{...} patterns
print("\n" + "="*80)
print("Searching for flags...")
print("="*80)

# Look for gigem{ followed by lowercase/underscore and }
pattern = r'gigem\{[a-z_]+\}'
matches = re.findall(pattern, decoded)

if matches:
    print(f"Found {len(matches)} potential flag(s):")
    for match in matches:
        print(f"  {match}")
        if len(match) > 15 and len(match) < 80:  # Reasonable flag length
            print(f"    → This could be the flag!")
else:
    print("No complete flags found with only letters/underscores")
    print("\nLooking for gigem{...} with any content:")
    
    # More lenient search
    partial = re.findall(r'gigem\{[^{}]{10,80}\}', decoded)
    if partial:
        print(f"Found {len(partial)} partial matches:")
        for match in partial[:10]:
            print(f"  {match}")
            # Count how many non-letter characters
            inner = match[6:-1]  # Remove 'gigem{' and '}'
            non_alpha = sum(1 for c in inner if not c.isalnum() and c != '_')
            if non_alpha < len(inner) * 0.3:
                print(f"    → {non_alpha}/{len(inner)} non-alpha chars")

# Show decoded sections
print("\n" + "="*80)
print("Decoded text around position 830:")
print("="*80)
start = max(0, 830-50)
end = min(len(decoded), 830+200)
snippet = decoded[start:end]
print(snippet)

# Try to find the closing brace manually
flag_start = snippet.find('gigem{')
if flag_start >= 0:
    # Find the closing brace
    flag_end = snippet.find('}', flag_start + 6)
    if flag_end > flag_start:
        potential_flag = snippet[flag_start:flag_end+1]
        print(f"\nExtracted flag candidate:\n{potential_flag}")
        
        # Check how clean it is
        inner = potential_flag[6:-1]
        clean_chars = sum(1 for c in inner if c.isalpha() or c == '_')
        print(f"Clean characters: {clean_chars}/{len(inner)} ({100*clean_chars/len(inner):.1f}%)")
