import sys

rna_fold_file = sys.argv[1]

with open(rna_fold_file) as rff:
    lines = rff.readlines()

holes = []
hole_size = 0
hole_start = 0
in_hole = False


for line in lines:
    line = line.strip()
    if line.startswith(">"):
        continue
    if any(["A" in line,
            "C" in line,
            "U" in line,
            "G" in line]):
        continue

    words = line.split(" ")
    structure = words[0]
    for index, char in enumerate(structure):
        if in_hole:
            if char == ".":
                hole_size += 1
            else:
                in_hole = False
                holes.append((hole_start, hole_size))
        else:
            if char == ".":
                in_hole = True
                hole_start = index
                hole_size = 1
            else:
                pass


hole_map = {"vsmall": 0,
            "small": 0,
            "medium": 0,
            "large": 0,
            "huge": 0}


for pos, size in holes:
    if size > 0 and size <= 2:
        hole_map["vsmall"] += 1
    elif size > 2 and size <= 4:
        hole_map["small"] += 1
    elif size > 4 and size <= 7:
        hole_map["medium"] += 1
    elif size > 7 and size <= 10:
        hole_map["large"] += 1
    else:
        hole_map["huge"] += 1


finger_print = "%s %s %s %s %s" % (hole_map["vsmall"],
                                   hole_map["small"],
                                   hole_map["medium"],
                                   hole_map["large"],
                                   hole_map["huge"])


print finger_print
