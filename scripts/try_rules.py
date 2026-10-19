from src.classify_rules import classify_headline

headlines = [
    "TSMC halts production after earthquake",
    "US expands export controls on chip equipment",
    "Micron reports record quarterly revenue",
    "Tariffs trigger port closures across Asia",
    "TSMC avoids shutdown as power grid recovers",
    "Samsung fab halted after blaze",
    "Will new sanctions hit ASML?",
    "Earthquake drill held at Hsinchu science park",
]

for headline in headlines:
    label, terms = classify_headline(headline)
    print(f"{label:<14} {terms}  <-  {headline}")