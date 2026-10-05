from src.seed import DIAGNOSES, MUNICIPALITIES


def test_diagnosis_set_has_no_duplicates():
    assert len(DIAGNOSES) == 5


def test_municipalities_have_required_fields():
    required = {"ibge", "name", "admissions", "deaths", "risk_score", "lat", "lon"}
    assert all(required.issubset(item) for item in MUNICIPALITIES)
