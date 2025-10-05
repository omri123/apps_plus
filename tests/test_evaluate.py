from apps_plus import get_apps_data, evaluate_apps_solution

def test_get_and_eval():
    data = get_apps_data()
    sample = data[0]
    assert "passed" == evaluate_apps_solution(sample['starter_code'], sample['inputs'], sample['outputs'], sample['canonical_solution'])