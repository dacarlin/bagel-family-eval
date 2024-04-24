from biotite.sequence import ProteinSequence 
from biotite.sequence.io.fasta import FastaFile, set_sequence 


input_file = "family.fa"
output_file = "output.fa"

file = FastaFile.read(input_file)
out_file = FastaFile() 

for header, sequence in file.items():
    print(header)

    accession = header.split("-F1")[0]  # just the accession 
    out_file[accession] = sequence 

with open(output_file, "w") as fn:
    out_file.write(fn)

