## EXERCICIO COM PYTHON AND REG ##
## ---------------------------- ##

import re

def extract_asterisk_words(text):
    # Pattern matches ** followed by one or more uppercase letters (or spaces/hyphens if needed)
    # Adjust the pattern if your words can include numbers or other characters
    pattern = r'\*\*([A-Z\s\-]+)\*\*'
    pattern = r'\*\*([A-ZÀ-ÖØ-ÝĀ-Ž]+)\*\*'      ## better ##
    
    # Find all matches
    matches = re.findall(pattern, text)
    
    return matches

# Example usage
text = """Industry's standard dummy text ever since 1966, when designers at **LETRASET** and James Mosley, the librarian at St Bride Printing **LIBRARY**, took a 1914 Cicero translation (.......)"""

result = extract_asterisk_words(text)
print(result)
# Output: ['LETRASET', 'LIBRARY']

# Using from a list 
result = extract_asterisk_words(" ".join(lst_5_categorias))
print(result)
