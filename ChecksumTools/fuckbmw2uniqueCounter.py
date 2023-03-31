import csv
failed_rows = []
unique_addresses = {}

with open('input.csv', 'r') as in_file, open('output.csv', 'w', newline='') as out_file, open('failedoutputs.csv', 'w', newline='') as fail_file:


    csv_reader = csv.DictReader(in_file)
    csv_writer = csv.writer(out_file)
    fail_writer = csv.writer(fail_file)


    csv_writer.writerow(['Time Stamp', 'ID', 'Extended', 'Dir', 'Bus', 'LEN', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'])
    fail_writer.writerow(['Time Stamp', 'ID', 'Extended', 'Dir', 'Bus', 'LEN', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'])

    for row in csv_reader:
        d_values = [int(row[f"D{i}"], 16) for i in range(2, 9)]
        checksum = sum(d_values) + int(row['ID'], 16)
        checksum = (checksum & 0xFF) + (checksum >> 8)
        d1 = int(row['D1'], 16)
        if d1 <= checksum or (d1 > checksum and d1 - checksum == 256):
            address = row['ID']
            if address not in unique_addresses:

                csv_writer.writerow([row['Time Stamp'], row['ID'], row['Extended'], row['Dir'], row['Bus'], row['LEN'], row['D1'], row['D2'], row['D3'], row['D4'], row['D5'], row['D6'], row['D7'], row['D8']])
                unique_addresses[address] = [1, 0]
            else:
                unique_addresses[address][0] += 1
        else:
            failed_rows.append(row)
            fail_writer.writerow([row['Time Stamp'], row['ID'], row['Extended'], row['Dir'], row['Bus'], row['LEN'], row['D1'], row['D2'], row['D3'], row['D4'], row['D5'], row['D6'], row['D7'], row['D8']])

            address = row['ID']
            if address not in unique_addresses:
                unique_addresses[address] = [0, 1]
            else:
                unique_addresses[address][1] += 1
    for row in failed_rows:
        address = row['ID']
        d1 = int(row['D1'], 16)
        d8 = int(row['D8'], 16)
        if address not in unique_addresses:
            unique_addresses[address] = [0, 1, 0, 0]  # Initialize with D1 and D8 matched counts set to 0
        if is_d1_checksum:
            unique_addresses[address][2] += 1
        if is_d8_checksum:
            unique_addresses[address][3] += 1

    sorted_addresses = sorted(unique_addresses.items(), key=lambda x: x[1][0], reverse=True)
    print("Address  Successes  Failures  Total  D1_Matched  D8_Matched")
    for address, counts in sorted_addresses:
        total = counts[0] + counts[1]
        if total > 0:
            print(f"{address}  {counts[0]}  {counts[1]}  {total}  {counts[2]}  {counts[3]}")
