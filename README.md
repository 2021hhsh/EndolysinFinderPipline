README: EndolysinFinder Pipeline
Introduction
The EndolysinFinder Pipeline is designed to mine bacterial genomes for endolysins within prophages. This tool takes nucleic acid sequence files as input, which should be placed in the input directory. The pipeline processes the input files and produces the final endolysin sequences and an annotation file, final.txt.

Features
The EndolysinFinder Pipeline automates multiple steps in bacterial genomic analysis:

Phage Detection: Uses Vibrant to identify prophages in bacterial genomes.
Phage Screening: Uses CheckV to evaluate the quality of prophages.
Endolysin Prediction: Uses HMMER to predict endolysins and annotate results.
This pipeline supports parallel processing with customizable thread and process options, ensuring efficient execution even with large datasets. Its modular design allows for flexible customization of environments and databases.

Requirements
Dependencies
Operating System: Unix/Linux environment with Bash.
Environment Manager: Conda.
Installed Tools:
Vibrant for phage detection.
CheckV for prophage quality assessment.
HMMER for functional annotation.
Custom Scripts: Located in the scripts/ directory.
Input
The input should be nucleic acid sequence files in .fna format. These files must be placed in the input directory before running the pipeline.

Installation
Environment Setup
Due to potential dependency conflicts between Vibrant and CheckV, you need to install these tools in separate Conda virtual environments. Both environments must reside within the same Conda installation.

Installing Vibrant
Use the provided vibrant.yml file to create a Conda environment:

conda env create -f vibrant.yml
Alternatively, follow the installation guide on the Vibrant GitHub repository.

Vibrant GitHub Repository: https://github.com/AnantharamanLab/VIBRANT
Vibrant Documentation: https://vibrant.readthedocs.io/

Installing CheckV
Use the provided checkv.yml file to create a Conda environment:

conda env create -f checkv.yml
Alternatively, refer to the CheckV installation guide:

CheckV Documentation: https://bitbucket.org/berkeleylab/checkv/src/master/
Database Files
CheckV Database: Use the following command to download the database:


checkv download_database ./checkv-db
Alternatively, download manually:


wget https://portal.nersc.gov/CheckV/checkv-db-v1.0.tar.gz
tar -xzvf checkv-db-v1.0.tar.gz
Pfam-A_v32.HMM: This database is used during the HMMER annotation process. It is included in the Vibrant environment and typically located at:


~/miniconda3/envs/new_vibrant/share/vibrant-1.2.1/db/databases/Pfam-A_v32.HMM
Usage
Run the script using the following syntax:


bash EndolysinFinder.sh [options]
Options
Option	Description	Default
-h	Show help documentation.	
-i	Specify the input directory containing input files.	input
-v	Specify the Vibrant conda environment name.	new_vibrant
-c	Specify the CheckV conda environment name.	checkv
-d	Specify the CheckV database path.	../checkv_db/checkv-db-v1.5
-b	Specify the hmmscan database path.	~/miniconda3/envs/new_vibrant/share/vibrant-1.2.1/db/databases/Pfam-A_v32.HMM
-s	Specify the hmmsearch model input directory.	../hmmer_mod
-t	Specify the number of threads for each process.	10
-n	Specify the number of parallel processes.	1
Workflow Steps
Phage Detection:

Activates the Vibrant environment and runs multi-vibrant.py to process input files.
Extracting .fna Files:

Uses get_fna.py to extract .fna files from Vibrant outputs.
Phage Screening:

Activates the CheckV environment and evaluates the quality of identified phages.
Extracting Protein Sequences:

Runs get_gbk-trans-faa.py to extract protein sequences from phage genomes.
Filtering Sequences:

Filters sequences using CheckV results with checkv-out-faa-copy.py.
Preparing HMMER Input:

Deduplicates sequences into a single .faa file using unique_seq.py.
Running HMMER:

Uses hmmscan and hmmsearch to annotate and identify endolysin-related sequences.
Generating Results:

Extracts, annotates, and ranks HMMER results.
Produces a summary table (final.txt) and other intermediate outputs.
Output Files
Directory/File	Description
vibrant-output/	Output from Vibrant analysis.
fnas/	Extracted .fna files.
checkv_output/	Results from CheckV analysis.
gbk-faa-out/	Extracted protein sequences.
checked_seqs/	Filtered protein sequences.
hmmer-input-uniq/	Deduplicated input sequences for HMMER.
hmm_run/result/	Results from HMMER annotation.
final.txt	Consolidated final results with annotations.
Examples
1. Default Run
bash EndolysinFinder.sh
2. Custom Input and Database
bash EndolysinFinder.sh -i /data/input -d /data/checkv-db -b /data/hmmscan-db/Pfam-A.hmm -t 20 -n 4
Troubleshooting
Input Directory Not Found: Ensure the input directory exists and contains valid .fna files.

CheckV Database Not Found: Verify the database path is correct and accessible. Use the -d option to specify the database path.

No Suitable .faa Files Found: Ensure input files are correctly formatted and the directory is not empty.

HMMER Errors: Confirm the HMMER database and model directories are correctly specified with -b and -s.

Contributors
Author: Ruirui Hu, Fulin Li
Email: 2891345454@qq.com
License
This script is licensed under [Your Preferred License].