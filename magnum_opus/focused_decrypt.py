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

print("Looking for 'gigem{' pattern at position 830...")
print(f"Context around 830: {''.join(graphemes[825:880])}\n")

# Build mapping from position 830 where we see: g🐸🥂🍂🤥🍈🐸g🍈🐸🐌🤥
# This translates to: g i g e m { ...
pos = 830
mapping = {
    graphemes[pos]: 'g',      # 🤡
    graphemes[pos+1]: 'i',    # 🐪
    graphemes[pos+2]: 'g',    # 🐸 (same as 0, so this confirms g)
    graphemes[pos+3]: 'e',    # 🤥
    graphemes[pos+4]: 'm',    # 😶
    graphemes[pos+5]: '{',    # 🐰
}

print("Initial mapping from position 830:")
for emoji, letter in mapping.items():
    print(f"  {emoji} -> {letter}")

# Now decode a large section
test_section = graphemes[820:950]
decoded = ''.join([mapping.get(g, g) for g in test_section])
print(f"\nDecoded section (820-950):\n{decoded}\n")

# The pattern shows 🤥 appears frequently and should be 'i' based on gigem
# Let's refine by looking at common patterns

# Search for closing brace
print("Looking for closing brace...")
for i in range(pos+6, min(pos+200, len(graphemes))):
    if graphemes[i] not in mapping:
        test_map = mapping.copy()
        test_map[graphemes[i]] = '}'
        decoded_test = ''.join([test_map.get(g, g) for g in graphemes[pos:i+1]])
        
        # Check if this looks reasonable
        if '{' in decoded_test and '}' in decoded_test:
            # Check inner content
            inner = re.search(r'\{([^{}]+)\}', decoded_test)
            if inner:
                inner_text = inner.group(1)
                # Check if it's mostly letters/underscores
                unknown_count = sum(1 for c in inner_text if len(c.encode('utf-8')) > 1)
                if unknown_count < len(inner_text) * 0.3:  # Less than 30% unknown
                    print(f"  Position {i}: {decoded_test[:80]}")
                    if len(inner_text) > 10 and len(inner_text) < 60:
                        print(f"    Inner ({len(inner_text)} chars): {inner_text}")
                        print(f"    Brace emoji: {graphemes[i]}")

# Let me try to build a more complete mapping using frequency analysis
# and the gigem{ pattern
print("\n" + "="*80)
print("Building complete mapping...")
print("="*80)

# From position 830, we have:
# 🤡 -> g, 🐪 -> i, 🐸 -> g, 🤥 -> e, 😶 -> m, 🐰 -> {

# Let's look at what follows and build the mapping
extended_map = {
    '🤡': 'g',
    '🐪': 'i', 
    '🐸': 'g',
    '🤥': 'i',  # This emoji is very frequent (236 times), likely 'i' not 'e'
    '😶': 'm',
    '🐰': 'a',  # Frequent, likely a vowel
    '🌸': 's',
    '😴': 't',
    '🥰': 'e',
    '💎': 'b',
    '💩': 'o',
    '🦌': 'f',
    '🥂': 'r',
    '🍈': 'h',
    '🍳': 'm',
    '🐆': 'u',
    '🍂': 'l',
    '🐌': ',',
    '🍴': '.',
    '💥': ' ',  # or delimiter
    '🤠': 'y',
    '😺': 'p',
    '🍝': 'w',
    '🦎': 'c',
    '🥘': ':',
    '😾': 'c',
    '😁': 'n',
    '😏': 'k',
    '🤯': 'w',
    '❌': 'x',
    '🐷': 'p',
    '⛳': 'i',
    '☘': '_',
    '😧': 'a',
    '🦂': '{',
    '🍣': 'j',
    '🐝': '!',
    '🤣': 'l',
    '🍚': 'o',
    '🐋': '}',
}

# Decode with extended mapping
full_decode = ''.join([extended_map.get(g, g) for g in graphemes])

# Find gigem{...}
print("\nSearching for gigem{...} in decoded text...")
matches = list(re.finditer(r'gigem\{[a-z_]{10,60}\}', full_decode))
if matches:
    print(f"Found {len(matches)} potential flags:")
    for match in matches:
        print(f"  {match.group(0)}")
else:
    # Show partial matches
    print("No complete flag found. Showing partial matches:")
    partial = list(re.finditer(r'gigem\{[^}]{5,80}\}', full_decode))
    for match in partial[:5]:
        print(f"  {match.group(0)}")

# Show decoded text around position 830
print("\n" + "="*80)
print("Decoded text around flag position (chars 400-600):")
print("="*80)
print(full_decode[400:600])

print("\n" + "="*80)
print("Decoded text (chars 800-1000):")
print("="*80)
print(full_decode[800:1000])
