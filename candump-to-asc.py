import re
from datetime import datetime
import sys
def parse_line(line):
    pattern = r"\((\d+\.\d+)\)\s+can\d+\s+(\w+)##([\w]+)"
    match = re.match(pattern, line.strip())
    if match:
        timestamp, can_id, payload = float(match.group(1)), match.group(2), match.group(3)
        return timestamp, can_id, payload
    else:
        return None, None, None

def format_arb_id(arb_id):
    arb_id = arb_id.lstrip('0')
    
    if len(arb_id) > 3:
        arb_id += 'x'
    
    return arb_id.rjust(8)

def main(input_file, output_file):
    now = datetime.now()
    now_str = now.strftime("%a %b %d %I:%M:%S.%f %p %Y")
    start_time = None

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        outfile.write(f"{now_str}\n")
        outfile.write("base hex  timestamps absolute\n")
        outfile.write("internal events logged\n")
        outfile.write(f"Begin Triggerblock {now_str}\n")
        outfile.write("0.000000 Start of measurement\n")
        
        for line in infile:
            timestamp, can_id, payload = parse_line(line)
            
            if timestamp is None:
                print(f"Skipping line: {line.strip()}")
                continue
            
            if start_time is None:
                start_time = timestamp

            relative_timestamp = timestamp - start_time
            formatted_payload = ' '.join([payload[i:i+2] for i in range(0, len(payload), 2)])
            dlc = len(formatted_payload.split())-1

            formatted_can_id = format_arb_id(can_id)

            outfile.write(f"{relative_timestamp:9.6f} CANFD   1 Rx   {formatted_can_id}   1 0 8  {dlc:1} {formatted_payload.ljust(28)}       0    0     3000        0        0        0        0        0\n")

        outfile.write("End TriggerBlock\n")

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
