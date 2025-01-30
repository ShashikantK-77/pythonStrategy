import csv
def update_execution_count(strategy_data_list, strategy_file):
    # Read the CSV file into a list of dictionaries
    with open(strategy_file, mode='r', newline='') as file:
        reader = list(csv.DictReader(file))

    # Update the execution count in the CSV data
    for strategy_data in strategy_data_list:
        for action in strategy_data['actions']:
            for row in reader:
                if row['strategy_id'] == strategy_data['strategy']['strategy_id']:
                    row['executionCount'] = str(action['executionCount'])

    # Write the updated data back to the CSV file
    with open(strategy_file, mode='w', newline='') as file:
        fieldnames = reader[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reader)
