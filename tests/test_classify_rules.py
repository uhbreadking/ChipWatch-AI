from src.classify_rules import classify_headline


# ---------- Correct behavior ----------

def test_manufacturing_headline():
    label, terms = classify_headline("TSMC halts production after earthquake")
    assert label == "Manufacturing"
    assert terms == ["halts production", "earthquake"]


def test_geopolitical_matches_plural():
    label, terms = classify_headline("US expands export controls on chip equipment")
    assert label == "Geopolitical"


def test_ordinary_news_has_no_signal():
    label, terms = classify_headline("Micron reports record quarterly revenue")
    assert label == "No signal"
    assert terms == []


def test_mixed_categories_need_review():
    label, terms = classify_headline("Tariffs trigger port closures across Asia")
    assert label == "Needs review"


def test_handles_missing_headline():
    label, terms = classify_headline(None)
    assert label == "No signal"


# ---------- Known limitations of keyword rules ----------
# These document current (imperfect) behavior. If a future change
# fixes one, the test will fail as a reminder to update it on purpose.

def test_known_limitation_negation():
    label, terms = classify_headline("TSMC avoids shutdown as power grid recovers")
    assert label == "Manufacturing"


def test_known_limitation_paraphrase():
    label, terms = classify_headline("Samsung fab halted after blaze")
    assert label == "No signal"


def test_known_limitation_hypothetical():
    label, terms = classify_headline("Will new sanctions hit ASML?")
    assert label == "Geopolitical"


def test_known_limitation_context():
    label, terms = classify_headline("Earthquake drill held at Hsinchu science park")
    assert label == "Manufacturing"