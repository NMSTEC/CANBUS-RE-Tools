import csv

unique_addresses = set()
with open('input.csv', 'r') as in_file, open('output.csv', 'w', newline='') as out_file:

    csv_reader = csv.DictReader(in_file)
    csv_writer = csv.writer(out_file)
    csv_writer.writerow(['Time Stamp', 'ID', 'Extended', 'Dir', 'Bus', 'LEN', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'])
    for row in csv_reader:
        d_values = [int(row[f"D{i}"], 16) for i in range(2, 9)]
   
        gaysome = sum(d_values) + int(row['ID'], 16)
        gaysome = (gaysome & 0xFF) + (gaysome >> 8)

        if gaysome == int(row['D1'], 16):
            address = row['ID']
            if address not in unique_addresses:
                csv_writer.writerow([row['Time Stamp'], row['ID'], row['Extended'], row['Dir'], row['Bus'], row['LEN'], row['D1'], row['D2'], row['D3'], row['D4'], row['D5'], row['D6'], row['D7'], row['D8']])
                unique_addresses.add(address)
