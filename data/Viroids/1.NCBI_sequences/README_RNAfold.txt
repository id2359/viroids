#Predicting RNA secondary folding structure using RNAfold (Vienna package)
#Output both RNAfold structures and RNA folding images
cat sequences.fasta | RNAfold -noLP > sequences_structures.out

#Output only the RNAfolding structures with no images
cat sequences.fasta | RNAfold -noPS > sequences_structures.out

