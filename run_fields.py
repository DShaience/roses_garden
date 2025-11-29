import json
from pathlib import Path

from roses_field import RosesField


def parse_location_dict(location_dict):
    return {tuple(map(int, k.split(','))): v for k, v in location_dict.items()}


def run_test_case(test_case):
    name = test_case['name']
    description = test_case['description']
    
    location_roses = parse_location_dict(test_case['location_roses'])
    location_costs = parse_location_dict(test_case['location_costs'])
    
    purchased_squares = [tuple(sq) for sq in test_case['purchased_squares']]
    
    # initializing
    roses_field = RosesField(
        field_width=test_case['field_width'],
        field_height=test_case['field_height'],
        purchased_squares=purchased_squares,
        location_roses=location_roses,
        location_costs=location_costs,
        garden_width=test_case['garden_width'],
        garden_height=test_case['garden_height']
    )
    
    # finding the best garden
    result = roses_field.find_best_garden(budget=test_case['budget'])
       
    return {
        'name': name,
        'description': description,
        'result': result
    }


def run_examples():
    test_file = Path('test_fields_to_run.json')
    with open(test_file, 'r') as f:
        data = json.load(f)
    
    test_cases = data['test_cases']
    
    print(f"Running {len(test_cases)} test cases:\n")   
    results = []    
    for test_case in test_cases:
        result = run_test_case(test_case)
        results.append(result)
        print(f"   {result['description']}")
        print(f"   Result: {result['result']}")
        print("")
    print("")


if __name__ == "__main__":
    run_examples()
