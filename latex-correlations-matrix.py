import csv
import argparse


def get_striked_header_pairs(strikethrough):
    if strikethrough is not None:
        return [pair.split('--') for pair in strikethrough]
    else:
        return []


def build_colored_str(v, cancelled):
    if (v < 0.20):
        return '\\textcolor{cor-very-weak}{' + str(cancelled) + "}"
    elif v >= 0.20 and v < 0.40:
        return '\\textcolor{cor-weak}{' + str(cancelled) + "}"
    elif v >= 0.40 and v < 0.60:
        return '\\textcolor{cor-moderate}{' + str(cancelled) + "}"
    elif v >= 0.60 and v < 0.80:
        return '\\textcolor{cor-strong}{' + str(cancelled) + "}"
    elif v >= 0.80 and v <= 1.0:
        return '\\textcolor{cor-very-strong}{' + str(cancelled) + "}"


def build_cancel(v, dim1, dim2, striked_header_pairs):
    if ([dim1, dim2] in striked_header_pairs) or \
       ([dim2, dim1] in striked_header_pairs):
        return "\\hcancel{" + str(v) + "}"
    return v


def build_table_text(csv_header, csv_data, striked_header_pairs):
    i = 0
    j = 0
    table = '& ' + ' & '.join(csv_header) + '\\\\ \\hline \n'

    while i < len(csv_data):
        j = 0
        dim1 = csv_header[i]
        if dim1 == "SS":
            i += 1
            continue

        rowstr = dim1
        while j < len(csv_data[i]):
            dim2 = csv_header[j]
            if dim2 == "SS":
                j += 1
                continue

            if i > j:
                rowstr += " & "
            else:
                v = float("%.2f" % round(float(csv_data[i][j]), 2))
                cancelled = build_cancel(
                    v,
                    dim1,
                    dim2,
                    striked_header_pairs
                )
                v = build_colored_str(v, cancelled)
                rowstr += " & " + v
            j += 1
        table += rowstr + '\\\\ \\hline \n'
        i += 1

    return table


# ---------------
# ARGUMENTS
# ---------------
parser = argparse.ArgumentParser(
    description="This program pretty-prints a CSV correlations matrix for usage in latex",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    'csv_file',
    type=str,
    help='CSV file to load'
)
parser.add_argument(
    '-d',
    '--delimiter',
    type=str,
    default=",",
    help='Column delimiter',
)
parser.add_argument(
    '-s',
    '--strikethrough',
    type=str,
    nargs='+',
    help='Column pair to strike through (e.g. A--B, B--F for headers named A to F)',
)


# ---------------
# MAIN
# ---------------
if __name__ != '__main__':
    raise NotImplementedError("This module should be main")

# Parse arguments
args = parser.parse_args()

# Read CSV file
header = []
data = []

with open(args.csv_file, 'rb') as csvfile:
    all_data = list(csv.reader(csvfile, delimiter=args.delimiter))

    header = all_data[0]
    data = all_data[1:]

striked_header_pairs = get_striked_header_pairs(args.strikethrough)

# Format and print latex commands
table = build_table_text(header, data, striked_header_pairs)

print table
