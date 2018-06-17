import itertools
import sys
import subprocess
from Bio import SeqIO

def hamming(str1, str2):
	return sum(itertools.imap(str.__ne__, str1, str2))

def get_mutations(nt):
    # return the other letters?
    l = ['G','C','U','A','T']
    l.remove(nt)
    return l

def create_mutation(seq, pos, mut):
    result = []
    l = len(seq)
    for i in range(l):
        if i == pos:
            result.append(mut)
        else:
            result.append(seq[i])
    return "".join(result)

def get_sequence(fasta_file):
    fasta = SeqIO.read(fasta_file, "fasta")
    return "%s" % fasta.seq

def parse_shape(rna_fold_output):
    lines = rna_fold_output.split("\n")
    shape_lines = lines[2:]   # starts third line
    s = "".join(shape_lines)
    shape = []
    pos = 0
    l = len(s)
    space = ' '
    shape_chars = ['.','(',')']
    char = ''

    while char != space and pos < l:
        char = s[pos]
        if char in shape_chars:
            shape.append(char)
        else:
            break
        pos += 1
    r = "".join(shape)
    return r

def run_rna_fold(sequence):
    # return shape
    # to do
    tmp_file = "/tmp/seq.fa"
    with open(tmp_file, "w") as f:
        f.write("> tmp seq\n")
        f.write(sequence)
    return rna_fold(tmp_file)
    
    
def rna_fold(fasta_file):
    cmd = ["RNAfold", "-p", "-d2", "--noLP", "--noPS", "-i", fasta_file]
    result = subprocess.check_output(cmd)
    shape_part = parse_shape(result)
    return shape_part
    

def get_shape(fasta_file):
    return rna_fold(fasta_file)
    
    
wild_fasta_file = sys.argv[1]

wild_seq = get_sequence(wild_fasta_file)

l = len(wild_seq)

wild_shape = get_shape(wild_fasta_file)

score_map = {}

best_pos = -1
best_score = -1

for pos in range(l):
    print "pos = %s" % pos
    nt = wild_seq[pos]
    print "nt = %s" % nt
    hamming_dists = []
    for mut in get_mutations(nt):
        print "mutation at pos %s = %s" % (pos, mut)
        
        mutation_seq = create_mutation(wild_seq, pos, mut)
        mutation_shape = run_rna_fold(mutation_seq)
        hamming_dist = hamming(wild_shape, mutation_shape)
        hamming_percentage = float(hamming_dist) / float(len(mutation_shape))
        
        hamming_dists.append(hamming_percentage)
    average_hamming = float(sum(hamming_dists)) / float(len(hamming_dists))
    score = round(average_hamming, 4)
    print "score = %s" % score
    if score > best_score:
        best_score = score
        best_pos = pos

    score_map[pos] = score


# we should now process the scores somehow, e.g. create a fingerprint
# based on the score?
# dump scores to a file for now

# ideas for features would be simple stats, or percentage over threshold
# skewness


score_file = wild_fasta_file + ".score"

with open(score_file, "w") as sf:
    for pos in score_map:
        sf.write("%s " % score_map[pos])

print "most effective mutation pos = %s score = %s" % (best_pos, best_score)

