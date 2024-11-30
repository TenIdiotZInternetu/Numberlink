from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-s", "--solution", default="input.sln", type=str, help="The file with solution.")
parser.add_argument("--cnf", default="input.cnf", type=str, help="The DIMACS CNF file.")
args = parser.parse_args()

Npis = []

with open(args.solution) as file:
    for y, line in enumerate(file):
        for x, num in enumerate(line.split()):
            xstr = str(x).rjust(2, "0")
            ystr = str(y).rjust(2, "0")
            code = "1" + xstr + ystr + num
            Npis.append(code)

print("Problematic clauses:")

with open(args.cnf) as cnf:
    for i, line in enumerate(cnf):
        if i == 0: continue
        line_satisfied = False

        for var in line.split()[:-1]:
            line_satisfied = (var in Npis or
                              var[0] == "-" and var[1:] not in Npis)
            
            if line_satisfied: break

        if not line_satisfied:
            print(f"Line {i}: {line[:-1]}")