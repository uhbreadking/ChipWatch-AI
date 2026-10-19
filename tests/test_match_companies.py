from src.match_companies import load_aliases, match_companies

ALIASES = load_aliases()


def test_load_aliases_has_all_six_companies():
    assert len(ALIASES) == 6


def test_aliases_have_no_extra_spaces():
    for names in ALIASES.values():
        for name in names:
            assert name == name.strip()


def test_matches_single_company():
    assert match_companies("Micron halts production at Hiroshima plant", ALIASES) == ["micron"]


def test_matches_two_companies():
    assert match_companies("TSMC and Samsung Foundry race for 2nm customers", ALIASES) == ["tsmc", "samsung"]


def test_ignores_capitalization():
    assert match_companies("SK HYNIX shares jump on HBM demand", ALIASES) == ["sk_hynix"]


def test_ignores_partial_words():
    assert match_companies("New study links micronutrients to better sleep", ALIASES) == []


def test_plain_samsung_is_not_matched():
    assert match_companies("Samsung unveils new Galaxy phone", ALIASES) == []


def test_no_company_returns_empty_list():
    assert match_companies("Stock market closes higher on Friday", ALIASES) == []


def test_handles_missing_headline():
    assert match_companies(None, ALIASES) == []


def test_known_limitation_micron_unit_matches():
    # Known false positive: "micron" the unit matches Micron Technology.
    # Kept as a test so any future fix shows up as a deliberate change.
    assert match_companies("Researchers build a 5-micron optical sensor", ALIASES) == ["micron"]