import re

text = "00014123樱の风语"
match = re.search(r'\d+', text).group()
