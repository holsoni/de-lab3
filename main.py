import glob
import json
import csv

def main():
    json_files = scan_json_files()

    for json_file in json_files:
        transformed_data = load_and_transform_json(json_file)
        csv_file = json_file.replace('.json', '.csv')
        write_to_csv(transformed_data, csv_file)

def scan_json_files():
    json_files = glob.glob(f'data/**/*.json', recursive=True)
    return json_files

def flatten_json(json_obj, parent_key='', separator='_'):
    flattened = {}
    for key, value in json_obj.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened.update(flatten_json(value, new_key, separator=separator))
        else:
            flattened[new_key] = value
    return flattened

def load_and_transform_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        if 'geolocation' in data and isinstance(data['geolocation'], dict):
            flattened_geolocation = flatten_json(data['geolocation'], parent_key='geolocation', separator='_')
            data.update(flattened_geolocation)
            del data['geolocation']

        if 'geolocation_coordinates' in data and isinstance(data['geolocation_coordinates'], list):
            if len(data['geolocation_coordinates']) == 2:
                data['geolocation_coordinate_0'] = data['geolocation_coordinates'][0]
                data['geolocation_coordinate_1'] = data['geolocation_coordinates'][1]
            del data['geolocation_coordinates']

        return data

def write_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='') as csvf:
        csv_writer = csv.writer(csvf)
        csv_writer.writerow(data.keys())
        csv_writer.writerow(data.values())


if __name__ == "__main__":
    main()
