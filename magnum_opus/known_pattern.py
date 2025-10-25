emojis = "🌸🐰🌸🐸🍝🥨🐸🍝💩🍣🐰🍚😾🍂🤯😺😴💩🌸🍂🥂🍝🍚💩😺🐆🍈🐋💥"

# i know that this flag starts with gigem{
# i can replace the first 6 emojis with gigem{ and create a mapping from those 5 to gigem{
# i need an algorithm to figure out the mapping for the rest of the emojis
import regex

def find_flag():
    graphemes = regex.findall(r'\X', emojis)
    
    # Known mapping from flag prefix "gigem{"
    translations = {
        graphemes[0]: 'g',
        graphemes[1]: 'i',
        graphemes[2]: 'g',
        graphemes[3]: 'e',
        graphemes[4]: 'm',
        graphemes[5]: '{',
    }

    # also the poop emoji maps to o and the sushi emoji maps to j
    translations[graphemes[8]] = 'o'  # 💩
    translations[graphemes[9]] = 'j'  # 🍣
    translations[graphemes[11]] = '_'
    
    # Apply translations to build the flag
    result = ''.join(translations.get(g, g) for g in graphemes)
    print(result)


if __name__ == "__main__":
    find_flag()

