import regex

# Read
with open('magnum_opus.txt', 'r', encoding='utf-8') as f:
    text = f.read().strip()

graphemes = regex.findall(r'\X', text)

# Print first 100 with positions
print("First 100 graphemes:")
for i in range(min(100, len(graphemes))):
    print(f"{i:3d}: {graphemes[i]}")

# Check which positions have g_g pattern (pos 0 == pos 2)
print("\n\nPositions where grapheme[i] == grapheme[i+2] (potential 'gigem' start):")
for i in range(len(graphemes)-5):
    if graphemes[i] == graphemes[i+2]:
        print(f"{i:4d}: {graphemes[i:i+6]}")
        if i < 20 or (i > 65 and i < 75) or (i > 100 and i < 115):
            print(f"       This could be 'g{i}gemy' for gigem{{")
