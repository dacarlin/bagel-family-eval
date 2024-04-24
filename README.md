# Evaluating protein language models on designed enzymes  


The design and discovery of enzymes to perform catalysis on an unnatural substrate is a fascinating set of challenges. The design of novel enzymes and the discovery of useful ones are related problems. In the past, it has been difficult to identify computational approaches that can efficiently use fine-grained data, such as the effects of mutations, in harmonious integration with coarse grained data, such as the results of a synthetic metagenomics pipeline where we codon-optimize and synthesize genes for a diverse array of homologous proteins from different organisms. 

In this post, we'll explore the use of generative ML to tackle the tough and related problems of discovering and designing enzymes. To do this, well use a model system where we can experimentally measure kinetic constants for hundreds of mutants of a glucosidase enzyme coupled with screening data on hundreds of enzyme homologs. We'll use a generative ML approach to designing new enzymes for the desired function, and we'll use the experimental data to benchmark. 

We'll then use this to construct a difficult evaluation procedure for generative ML approaches to protein design, the Bagel Family Eval, that we can use to evaluate generative ML approaches for protein engineering in a way that is largely complementary to existing benchmarks based on low dynamic range phenotypic measurements. 

Data
- P22505, gram positive nitrogen fixer, we have about 100 kcat and km for pNP
- Q7MG41, vibrio, gram negative, marine bacterium, (medium similar)
- Q59976 from strep, gram positive (most similar!)
- Q97AX4, thermoplasma volcanium, thermophile! (most distant)



# Experiments 

## Process the mutant dataset 

Use the notebook `process.ipynb` to preprocess the mutational dataset. 

## Predict functional effects of single variants using ESM-2 

Use the provided script `predict.py` to predict the effects of mutations using ESM-2. 

```shell
python predict/predict.py \
	--model-location esm2_t6_8M_UR50D \
	--sequence MSENT (...snip...) KNGF \
	--dms-input data/bglb_for_labeling.csv \
	--offset-idx 1 \
	--dms-output data/bglb_labeled.csv \
	--scoring-strategy masked-marginals
```

This will provide zero-shot predictions from ESM-2 for the BglB dataset. 

## Searching for homologs 

Using the [Bioinformatics Toolkit from the Max Planck Institute](https://toolkit.tuebingen.mpg.de/), we can rapidly perform a homolog search for close homologs of BglB. To do this, my favorite tool is HMMER, an HMM-based method that is very popular for classifying proteins. We'll input the BglB sequence and use the `phmmer` tool (which allows searching with a single sequence) to search the UniProt database. We'll use an E-value of 1e-10 to get only highly significant hits in the result. 

Using this procedure, we obtain 3,211 homologous sequences. We won't do any further filtering or clustering at this step. 

## Embedding with ESM-2 

Instead of working with raw sequence data, we'll use embeddings from ESM-2 as the representation of our proteins. 

```bash
python extract.py \
	esm2_t6_8M_UR50D \
	../search/output.fa \
	embeddings \
	--repr_layers 6 \
	--include mean
```

## Visualizing the embedding space 

Using the notebook `embed.ipynb`, we'll visualize the embeddings. 
