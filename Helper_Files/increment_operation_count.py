import csv

def increment_operation_count():
    file_path = 'Input_Files/actions.csv'
    # Read the existing data
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        actions = list(reader)

    # Increment the operationCount for each action
    for action in actions:
        action['operationCount'] = int(action['operationCount']) + 1

    # Write the updated data back to the file
    with open(file_path, mode='w', newline='') as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(actions)

    print(f"Updated operationCount values in {file_path}")

# # Example usage

# increment_operation_count(file_path)
