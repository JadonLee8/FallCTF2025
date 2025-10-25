import regex
import re
from collections import Counter

# Read emoji text
with open('magnum_opus.txt', 'r', encoding='utf-8') as f:
    emojis = f.read().strip()

# Split into graphemes
graphemes = regex.findall(r'\X', emojis)

print(f"Total: {len(graphemes)} graphemes")
print(f"First: {graphemes[0]}, Last: {graphemes[-1]}")

# The VERY last emoji before the final 💥 should be the closing }
# Let's find patterns: 🌸🐰🌸🐸🍝🥨🐸🍝💩🍣🐰🍚😾🍂🤯😺😴💩🌸🍂🥂🍝🍚💩😺🐆🍈🐋💥
# This looks like: gigem{...}
# So 🐋 might be }

# Let me find the first 💥💥 which seems to be a delimiter
double_boom = []
for i in range(len(graphemes)-1):
    if graphemes[i] == '💥' and graphemes[i+1] == '💥':
        double_boom.append(i)

print(f"\n💥💥 positions: {double_boom}")

# The flag is likely in the first segment before first 💥💥
# Start is after the first 💥
flag_segment = graphemes[1:double_boom[0]] if double_boom else graphemes[1:]
print(f"\nFlag segment length: {len(flag_segment)}")
print(f"First 20: {flag_segment[:20]}")

# Look for "gigem{" pattern: g_g_m{ where char[0]==char[2]
for i in range(len(flag_segment)-5):
    if flag_segment[i] == flag_segment[i+2]:
        print(f"\nPosition {i}: {flag_segment[i:i+6]}")
        
        # Map as gigem{
        mapping = {
            flag_segment[i]: 'g',
            flag_segment[i+1]: 'i',
            flag_segment[i+3]: 'e',
            flag_segment[i+4]: 'm',
            flag_segment[i+5]: '{',
        }
        
        # The closing } should be 🐋 at the very end (position -2, before final 💥)
        if len(graphemes) >= 2:
            mapping[graphemes[-2]] = '}'
        
        # Decode everything
        decoded_all = ''.join([mapping.get(g, '?') for g in graphemes])
        
        # Find gigem{...}
        match = re.search(r'gigem\{[^{}]{5,100}\}', decoded_all)
        if match:
            flag = match.group(0)
            inner = flag[6:-1]
            unknowns = inner.count('?')
            pct = 100 * unknowns / len(inner) if len(inner) > 0 else 0
            
            print(f"  Found flag: {flag}")
            print(f"  Unknowns: {unknowns}/{len(inner)} ({pct:.1f}%)")
            
            if unknowns < len(inner) * 0.4:  # Less than 40% unknown
                print(f"  → PROMISING!")

# Now let's use comprehensive frequency analysis
print("\n" + "="*80)
print("Comprehensive frequency-based decryption")
print("="*80)

freq = Counter(graphemes)
print("Top 30 emojis:")
for e, c in freq.most_common(30):
    print(f"  {e}: {c}")

# Given the flag format, let me map intelligently
# Start with gigem{...} at position 10 (most likely)
pos = 10
full_map = {
    graphemes[pos]: 'g',      # 🤡
    graphemes[pos+1]: 'i',    # 🐪
    graphemes[pos+3]: 'e',    # 🤥
    graphemes[pos+4]: 'm',    # 😶
    graphemes[pos+5]: '{',    # 🐰
    graphemes[-2]: '}',       # 🐋 (last char before final 💥)
}

# Most frequent should be common letters
# 🤥 appears 236 times - very high, probably space or very common letter
# But we mapped it to 'e'... let me reconsider

# English letter frequency: space, e, t, a, o, i, n, s, h, r
# The most frequent emoji (🤥: 236) is likely space or a very common letter

# Remap based on better frequency analysis
english_freq = list(' etaoinshrdlcumwfgypbvkjxqz_.,')
sorted_emojis = [e for e, _ in freq.most_common()]

# But keep our known mappings from gigem{
known_emojis = {graphemes[pos], graphemes[pos+1], graphemes[pos+3], 
                graphemes[pos+4], graphemes[pos+5], graphemes[-2]}
unknown_emojis = [e for e in sorted_emojis if e not in known_emojis]
unknown_letters = [l for l in english_freq if l not in full_map.values()]

for e, l in zip(unknown_emojis, unknown_letters):
    full_map[e] = l

# Decode
full_decoded = ''.join([full_map.get(g, g) for g in graphemes])

# Find flags
matches = re.findall(r'gigem\{[a-z_]{10,80}\}', full_decoded)
print(f"\nFound {len(matches)} clean flags:")
for m in matches:
    print(f"  {m}")

# If no clean ones, show partial
if not matches:
    partial = re.findall(r'gigem\{[^{}]{10,100}\}', full_decoded)
    print(f"\nFound {len(partial)} partial matches:")
    for m in partial[:3]:
        inner = m[6:-1]
        alpha = sum(1 for c in inner if c.isalpha() or c == '_')
        print(f"  {m}")
        print(f"    Clean: {alpha}/{len(inner)} ({100*alpha/len(inner):.1f}%)")
