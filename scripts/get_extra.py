import sys
from Bio.Blast import NCBIXML

query_file = sys.argv[1]
output_file = sys.argv[2]

with open(output_file, 'w') as f:
	blast_records = NCBIXML.parse(blast_handle)
	for i, blast_record in enumerate(blast_records):
      	for alignment in blast_record.alignments:
        	for hsp in alignment.hsps:
            	f.write('>%s\n' % (hsp.query))
