import regex
import re

# Read the emoji string from restart_magnum.py
with open('restart_magnum.py', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('"') + 1
    end = content.rfind('"')
    emojis = content[start:end]

# Split into grapheme clusters
graphemes = regex.findall(r'\X', emojis)

# From analyzing position 830 where "gigem{" appears:
# The pattern is: 🤡🐪🐸🤥😶🐰 which should be "gigem{"
# But wait, that's 6 chars and gigem{ is 6 chars:
# Position: 0   1   2   3   4   5
# Pattern:  🤡  🐪  🐸  🤥  😶  🐰
# Should be: g   i   g   e   m   {

# So: 🤡=g, 🐪=i, 🐸=g (confirms 🐸=g), 🤥=e, 😶=m, 🐰={

# But looking at frequencies: 🤥 appears 236 times, 🥰 appears 68 times
# If 🤥 is 'e' that's WAY too frequent. Let me reconsider.

# Actually at position 830, let me check the exact sequence:
print("Emojis at position 830-836:")
for i in range(830, 837):
    print(f"  {i}: {graphemes[i]}")

# Let me try a simple substitution cipher based on keyboard layout
# The "keyboard rebinding" hint suggests the emojis might map to QWERTY keys

# Common approach: map by frequency
from collections import Counter
freq = Counter(graphemes)

# Most common English letters: etaoinshrdlcumwfgypbvkjxqz
english_order = list('etaoinshrdlcumwfgypbvkjxqz ')

# Map most frequent emojis to most frequent letters
sorted_emojis = [emoji for emoji, _ in freq.most_common(30)]

# But we know from gigem pattern:
# Positions where char[0] == char[2] could be 'gigem'
# Let's find those and deduce the mapping

for start in range(len(graphemes) - 5):
    if graphemes[start] == graphemes[start+2]:
        # Could be g_g pattern
        print(f"\nPosition {start}: {graphemes[start:start+6]}")
        
        # Try mapping as gigem{
        test_map = {
            graphemes[start]: 'g',
            graphemes[start+1]: 'i',
            graphemes[start+3]: 'e',
            graphemes[start+4]: 'm',
            graphemes[start+5]: '{',
        }
        
        # Decode next 50 chars
        decoded = []
        for g in graphemes[start:start+50]:
            decoded.append(test_map.get(g, '?'))
        decoded_str = ''.join(decoded)
        
        # Check if it looks like gigem{
        if decoded_str.startswith('gigem{'):
            print(f"  Decoded: {decoded_str}")
            print(f"  Mapping: {test_map}")
            
            # Count how many unknowns
            unknowns = decoded_str.count('?')
            if unknowns < 35:  # Less than 70% unknown
                print(f"  → This looks promising! ({unknowns}/50 unknown)")
