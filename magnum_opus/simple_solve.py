import regex
import re

# Read
with open('magnum_opus.txt', 'r', encoding='utf-8') as f:
    text = f.read().strip()

graphemes = regex.findall(r'\X', text)
print(f"Total: {len(graphemes)}")

# Try position 10 mapping
p = 10
m = {
    '🤡': 'g', '🐪': 'i', '🐸': 'g', '🤥': 'e', '😶': 'm', '🐰': '{',
    '🐋': '}',  # Last emoji (assumed closing brace)
}

# Add frequency-based guesses for common letters
# Based on the output I saw earlier
m.update({
    '😴': 't',
    '🥰': 'a', 
    '💩': 'o',
    '🦌': 'f',
    '🥂': 'r',
    '🍈': 'h',
    '🍳': 'm',
    '🐆': 'u',
    '🍂': 'l',
    '💎': 'b',
    '😺': 'p',
    '🌸': 's',
    '🍴': '.',
    '🐌': ',',
    '💥': ' ',
    '🍝': 'w',
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
    '🥘': ':',
    '🦎': 'c',
    '🙁': 's',
    '🤠': 'y',
    '🐝': '!',
    '🤣': 'l',
    '🍚': 'o',
    '🥡': ')',
    '🌽': '(',
    '🍞': '[',
    '😆': ']',
    '🌿': ';',
    '🌈': '&',
    '🕸': 'b',
    '🐍': 'q',
    '🆓': 'n',
    '🥨': '{',
    '👹': '!',
    '🥊': '"',
})

# Decode
decoded = ''.join([m.get(g, g) for g in graphemes])

# Find flags
flags = re.findall(r'gigem\{[a-z_]+\}', decoded)
print(f"\nFound {len(flags)} potential flags:")
for flag in flags:
    print(f"  {flag}")

# Show some decoded text
print("\nDecoded text (first 500 chars):")
print(decoded[:500])

print("\nDecoded text (around position 800-1000):")
print(decoded[800:1000])
