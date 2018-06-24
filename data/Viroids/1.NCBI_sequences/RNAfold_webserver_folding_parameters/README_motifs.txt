#get matches to CCR (CC plus purine base)
grep CCCCGGGG viroid_genomes_ncbi.fasta  -B1 | sed '/^--$/d' | grep ">" | sed 's/>//' | sed 's/ /_/g' | sed 's/.1_/.1 /' | sed 's/,_complete/ complete/' > CCR_hits_CCCCGGGG_motif.txt

