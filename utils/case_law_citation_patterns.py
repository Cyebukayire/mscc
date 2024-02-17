
# Patterns of case law citations
simplified_format = r'\b[A-Za-z]+\s+v\.\s+[A-Za-z]+\b' # Case law containing parties with single names
# pattern_2 = r'\b[A-Za-z]+\s+v\.\s+[A-Za-z\s]+\b', # Case law containing parties two names
# pattern_3 = r'\b[A-Za-z]+\s+v\.\s+[A-Za-z]+\s+[A-Z]+\s+[A-Z]+\b', # Case law containing parties two names
# pattern_4 = r'\b[A-Z]+\s+[A-Za-z]+\s+v\.\s+[A-Za-z]\b', # Case law containing parties two names
# pattern_5 = r'\b[A-Z]+\s+[A-Za-z]+\s+v\.\s+[A-Za-z]+\s+[A-Z]+\b', # Case law containing parties two names
# pattern_6 = r'\b[A-Z]+\s+[A-Za-z]+\s+v\.\s+[A-Za-z]+\s+[A-Z]+\s+[A-Z]+\b', # Case law containing parties multiple names
# pattern_7 = r'\b[A-Z]+\s+[A-Za-z]+\s+[A-Za-z]+\s+v\.\s+[A-Za-z]+\b', # Case law containing parties multiple names
# pattern_8 = r'\b[A-Z]+\s+[A-Za-z]+\s+[A-Za-z]+\s+v\.\s+[A-Za-z]+\s+[A-Z]+\b', # Case law containing parties multiple names
# pattern_9 = r'\b[A-Z]+\s+[A-Za-z]+\s+[A-Za-z]+\s+v\.\s+[A-Za-z]+\s+[A-Za-z]+\s+[A-Za-z]+\b', # Case law containing parties multiple names
# Standard format
standard_format = r'([A-Za-z .]+ v\. [A-Za-z .]+), (\d+) US (\d+) \((\d{4})\)'

# With periods
with_periods = r'([A-Za-z .]+ v\. [A-Za-z .]+), (\d+) U\.S\. (\d+) \((\d{4})\)'

# With spaces
with_spaces = r'([A-Za-z .]+ v\. [A-Za-z .]+), (\d+) U\. S\. (\d+) \((\d{4})\)'

# S.Ct. format
sct_format = r'([A-Za-z .]+ v\. [A-Za-z .]+), (\d+) S\.Ct\. (\d+) \((\d{4})\)'

# S.Ct. with space
sct_with_space = r'([A-Za-z .]+ v\. [A-Za-z .]+), (\d+) S\. Ct\. (\d+) \((\d{4})\)'

# Federal Court of Appeals Cases
federal_appeals_cases = r'([A-Za-z .]+ v\. [A-Za-z .]+), (\d+) F\.(2d|3d|4th) (\d+) \((\d{4})\)'

# District Court Cases
district_court_cases = r'([A-Za-z .]+ v\. [A-Za-z .]+), (\d+) F\. Supp\. (2d)? (\d+) \(([A-Z\. ]+) (\d{4})\)'

patterns =  [simplified_format, standard_format, with_periods, with_spaces, sct_format, sct_with_space, federal_appeals_cases, district_court_cases]
