import itertools
import sys

def hamming(str1, str2):
	return sum(itertools.imap(str.__ne__, str1, str2))

def get_mutations(nt):
    # return the other letters?
    return ['G','C','U','A'].remove(nt) # ??

def create_mutation(seq, pos, mut):
    result = []
    for i in len(seq):
        if i == pos:
            result.append(mut)
        else:
            result.append(seq[i])
    return "".join(result)


def run_rna_fold(sequence):
    # return shape
    # to do
    return ".(((....)))."

wild_fasta_file = sys.argv[1]

wild_seq = get_sequence(wild_fasta_file)

l = len(wild_seq)

wild_shape = get_shape(wild_fasta_file)

score_map = {}


for pos in range(l):
    nt = wild_seq[pos]
    hamming_dists = []
    for mut in get_mutations(nt):
        mutation_seq = create_mutation(wild_seq, pos, mut)
        mutation_shape = run_rna_fold(mutation_seq)
        hamming_dist = hamming(wild_shape, mutation_shape)
        hamming_dists.append(hamming_dist)
    average_hamming = sum(hamming_dists) / len(hamming_dists)
    score_map[pos] = average_hamming


# we should now process the scores somehow, e.g. create a fingerprint
# based on the score?
# dump scores to a file for now

# ideas for features would be simple stats, or percentage over threshold
# skewness


score_file_name = fasta_file_name.replace(".fasta", ".score")

with open(score_file), "w") as sf:
    for pos in score_map:
        sf.write("%s " % score_map[pos])

