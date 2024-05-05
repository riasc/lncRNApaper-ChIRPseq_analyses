import sys
import intervaltree

"""
    Usage:
        python3 bed2bedgraph.py <bed1> <bed2> <output>
"""

def main():
    data = dict()
    bed1 = open(sys.argv[1], 'r')
    for line1 in bed1:
        line = line1.strip().split()
        treekey = (line[0], line[5]) # create a key (chromosome, strand)
        if treekey not in data:
            data[treekey] = intervaltree.IntervalTree()
        data[treekey][int(line[1]):int(line[2])] = float(line[6])
    bed1.close()

    bed2 = open(sys.argv[2], 'r')
    out = open(sys.argv[3], 'w')
    out.write("track type=bedGraph name=\"BedGraph Format\" description=\"BedGraph format\" priority=20\n")
    for line2 in bed2:
        line = line2.strip().split()
        treekey = (line[0], line[5])
        if treekey in data:
            if len(data[treekey][int(line[1]):int(line[2])]) > 0:
                for interval in data[treekey][int(line[1]):int(line[2])]:
                    # determine new start and end positions
                    if interval.begin <= int(line[1]):
                        start = int(line[1])
                    else:
                        start = interval.begin

                    if interval.end >= int(line[2]):
                        end = int(line[2])
                    else:
                        end = interval.end

                    length = end - start

                    bed1_signal_per_unit = interval.data / (interval.end - interval.begin)
                    bed2_signal_per_unit = float(line[6]) / (int(line[2]) - int(line[1]))
                    final_signal = (bed1_signal_per_unit * length + bed2_signal_per_unit * length) / 2

                    out.write(f"{line[0]}\t{start}\t{end}\t{final_signal}\n")

    bed2.close()
    out.close()

main()
