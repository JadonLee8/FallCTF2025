import regex
from collections import Counter
import re

# Read the emoji string from restart_magnum.py
with open('restart_magnum.py', 'r', encoding='utf-8') as f:
    content = f.read()
    # Extract the emojis string
    start = content.find('"') + 1
    end = content.rfind('"')
    emojis = content[start:end]

# Split into grapheme clusters
graphemes = regex.findall(r'\X', emojis)
print(f"Total graphemes: {len(graphemes)}")
print(f"Unique graphemes: {len(set(graphemes))}")

# Frequency analysis
freq = Counter(graphemes)
print("\nTop 30 most frequent emojis:")
for emoji, count in freq.most_common(30):
    print(f"{emoji}: {count} times")

print("\n" + "="*80)
print("TECHNIQUE 1: Looking for 'gigem{' pattern (positions 0=2 for 'g')")
print("="*80)

# Find patterns where position 0 and 2 are the same (for 'g' in 'gigem')
candidates = []
for i in range(len(graphemes) - 50):
    if graphemes[i] == graphemes[i+2]:
        # This could be "g_g" pattern
        candidates.append(i)

print(f"Found {len(candidates)} positions where graphemes[i] == graphemes[i+2]")

# Try each candidate
for start in candidates[:10]:  # Check first 10
    print(f"\n--- Candidate at position {start} ---")
    pattern = graphemes[start:start+42]
    print(f"Pattern (first 42 chars): {''.join(pattern)}")
    
    # Map based on gigem{
    if len(pattern) >= 6:
        mapping = {
            pattern[0]: 'g',
            pattern[1]: 'i', 
            pattern[2]: 'g',
            pattern[3]: 'e',
            pattern[4]: 'm',
            pattern[5]: '{',
        }
        
        # Decode just this section
        decoded_section = ''.join([mapping.get(g, '?') for g in pattern[:20]])
        print(f"Decoded start: {decoded_section}")

print("\n" + "="*80)
print("TECHNIQUE 2: Substitution cipher frequency analysis")
print("="*80)

# Most common English letters in order
english_freq = 'etaoinshrdlcumwfgypbvkjxqz'

# Try mapping most frequent emojis to most frequent letters
mapping = {}
sorted_emojis = [e for e, _ in freq.most_common()]

# First, look for the gigem{ pattern
# In the restart file, we need to find where gigem{ starts
for i in range(len(graphemes) - 5):
    if graphemes[i] == graphemes[i+2]:  # g pattern
        # Try this as gigem{
        test_map = {
            graphemes[i]: 'g',
            graphemes[i+1]: 'i',
            graphemes[i+3]: 'e',
            graphemes[i+4]: 'm',
            graphemes[i+5]: '{',
        }
        
        # Decode entire text with this mapping
        decoded = ''.join([test_map.get(g, g) for g in graphemes])
        
        if decoded.count('gigem{') >= 1:
            print(f"\nFound potential gigem{{ at position {i}")
            print(f"Partial decode: {decoded[i:i+50]}")
            
            # Look for closing brace
            for j in range(i+6, min(i+200, len(graphemes))):
                test_map_with_close = test_map.copy()
                test_map_with_close[graphemes[j]] = '}'
                decoded_with_close = ''.join([test_map_with_close.get(g, g) for g in graphemes])
                
                if 'gigem{' in decoded_with_close and '}' in decoded_with_close[i:j+1]:
                    # Extract potential flag
                    flag_match = re.search(r'gigem\{[^{}]+\}', decoded_with_close[i:j+20])
                    if flag_match:
                        print(f"Potential flag fragment: {flag_match.group(0)}")

print("\n" + "="*80)
print("TECHNIQUE 3: Looking at specific markers")
print("="*80)

# Look for 💥 at start and end (could be delimiters)
print(f"💥 appears at positions: {[i for i, g in enumerate(graphemes[:50]) if g == '💥']}")
print(f"💥 appears at positions (last 50): {[i for i, g in enumerate(graphemes[-50:], start=len(graphemes)-50) if g == '💥']}")

# The pattern 💥💥 might be a delimiter
double_boom = []
for i in range(len(graphemes)-1):
    if graphemes[i] == '💥' and graphemes[i+1] == '💥':
        double_boom.append(i)
print(f"\n💥💥 (double) appears at positions: {double_boom}")

# Split by double boom and analyze segments
if len(double_boom) > 0:
    segments = []
    prev = 0
    for pos in double_boom:
        segments.append(graphemes[prev:pos])
        prev = pos + 2
    segments.append(graphemes[prev:])
    
    print(f"\nFound {len(segments)} segments between 💥💥")
    for idx, seg in enumerate(segments[:5]):  # Show first 5
        print(f"Segment {idx}: length {len(seg)}, starts with: {''.join(seg[:10])}")

print("\n" + "="*80)
print("TECHNIQUE 4: Check if emojis map to keyboard keys")
print("="*80)

# Maybe the "keyboard rebinding" is literal - each emoji represents a key
# Let's check the first segment more carefully
print("\nFirst 100 graphemes:")
print(''.join(graphemes[:100]))

# Check for repeating patterns
print("\n" + "="*80)
print("TECHNIQUE 5: Pattern analysis for flag format")
print("="*80)

# gigem{ is 6 characters, look for this pattern everywhere
for i in range(len(graphemes) - 6):
    if (graphemes[i] == graphemes[i+2] and  # g matches g
        graphemes[i] != graphemes[i+1] and   # g != i
        graphemes[i+3] != graphemes[i] and   # e != g
        graphemes[i+4] != graphemes[i] and   # m != g
        graphemes[i+1] != graphemes[i+3]):   # i != e
        
        # This could be gigem{
        potential_start = i
        print(f"\nPotential gigem{{ at position {i}")
        
        # Build mapping
        map_test = {
            graphemes[i]: 'g',
            graphemes[i+1]: 'i',
            graphemes[i+3]: 'e', 
            graphemes[i+4]: 'm',
            graphemes[i+5]: '{',
        }
        
        # Look ahead to find }
        # The flag format suggests it should be within 50-100 chars
        for end_pos in range(i+7, min(i+150, len(graphemes))):
            map_with_end = map_test.copy()
            map_with_end[graphemes[end_pos]] = '}'
            
            # Decode the flag section
            flag_section = graphemes[i:end_pos+1]
            decoded_flag = ''.join([map_with_end.get(g, g) for g in flag_section])
            
            # Check if it looks like a valid flag
            if decoded_flag.count('{') == 1 and decoded_flag.count('}') == 1:
                print(f"  Trying }} at position {end_pos}: {decoded_flag}")
                
                # Check if all characters between {{}} are unmapped emojis (could be flag content)
                inner = decoded_flag[6:-1]  # Between {{ and }}
                if len(inner) > 5:  # Reasonable flag length
                    print(f"    Inner content: {inner} (length: {len(inner)})")
