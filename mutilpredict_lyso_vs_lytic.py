import os
import sys
import numpy as np
import argparse
import pandas as pd
from typing import List, Tuple
from pathlib import Path

class DNASequenceAnalyzer:
    """Analyzes DNA sequences to predict if they are lysogenic or lytic."""

    VALID_NUCLEOTIDES = set("ACTG")
    KMER_SIZE = 6
    STEP_SIZE = 1
    SEQUENCE_LENGTH = 100 + KMER_SIZE - 1
    THRESHOLD1 = 0.9
    THRESHOLD2 = 0.016

    def __init__(self, model_path: str, fasta_folder: str, output_csv: str):
        self.model_path = model_path
        self.fasta_folder = Path(fasta_folder)
        self.output_csv = output_csv

        # Ensure output file exists
        if not Path(self.output_csv).exists():
            pd.DataFrame(columns=["FASTA File", "Probability", "Prediction"]).to_csv(self.output_csv, index=False)

    def validate_sequence(self, seq: str) -> None:
        """Validates that sequence contains only ACTG."""
        invalid_chars = set(seq) - self.VALID_NUCLEOTIDES
        if invalid_chars:
            raise ValueError(f"Error: Sequence contains invalid letters {invalid_chars}, expecting only ACTG.")

    def seq2kmer(self, seq: str, k: int) -> str:
        """Converts sequence to k-mer representation."""
        return " ".join(seq[x:x + k] for x in range(len(seq) + 1 - k))

    def read_fasta(self, fasta_file: Path) -> str:
        """Reads and validates a FASTA file."""
        with open(fasta_file) as f:
            lines = [line.strip() for line in f.readlines()]

        if len(lines) != 2:
            raise ValueError(f"Error in {fasta_file.name}: FASTA file must contain exactly 2 lines.")

        dna_sequence = lines[1]
        self.validate_sequence(dna_sequence)
        return dna_sequence

    def prepare_tmp_directory(self, tmp_dir: Path) -> None:
        """Sets up a temporary directory for processing."""
        if tmp_dir.exists():
            os.system(f"rm -r {tmp_dir}")
        print(f"Creating tmp directory: {tmp_dir}")
        tmp_dir.mkdir()

    def generate_sequences(self, dna: str, tmp_dir: Path) -> None:
        """Generates overlapping sequences for prediction."""
        with open(tmp_dir / "dev.tsv", "w") as f:
            f.write("sequence\tlabel\n")
            n = 0
            c = 0
            while n + self.SEQUENCE_LENGTH < len(dna):
                kmers = self.seq2kmer(dna[n:n + self.SEQUENCE_LENGTH], self.KMER_SIZE)
                f.write(f"{kmers}\t{int(c == 0)}\n")
                n += self.STEP_SIZE
                c += 1

    def run_prediction(self, fasta_file: Path, tmp_dir: Path) -> Tuple[str, float, str]:
        """Runs the prediction model and interprets results."""
        command = (
            f"python ./run_finetune.py "
            f"--model_type dna "
            f"--tokenizer_name=dna6 "
            f"--model_name_or_path {self.model_path} "
            f"--task_name dnaprom "
            f"--do_predict "
            f"--data_dir {tmp_dir} "
            f"--max_seq_length 100 "
            f"--per_gpu_pred_batch_size=32 "
            f"--output_dir {self.model_path} "
            f"--predict_dir {tmp_dir} "
            f"--n_process 48"
        )
        print(f"\n{command}")
        os.system(command)

        # Load and interpret results
        results = np.load(tmp_dir / "pred_results.npy")
        probability = np.mean(results > self.THRESHOLD1)
        prediction = "Lysogenic" if probability >= self.THRESHOLD2 else "Lytic"

        return fasta_file.name, probability, prediction

    def save_result(self, result: Tuple[str, float, str]) -> None:
        """Appends a single prediction result to the CSV file."""
        df = pd.DataFrame([result], columns=["FASTA File", "Probability", "Prediction"])
        df.to_csv(self.output_csv, mode='a', header=False, index=False)
        print(f"Saved result for {result[0]}")

    def delete_tmp_directory(self, tmp_dir: Path) -> None:
        """Deletes the temporary directory."""
        if tmp_dir.exists():
            os.system(f"rm -r {tmp_dir}")
            print(f"Deleted tmp directory: {tmp_dir}")

    def analyze_folder(self) -> None:
        """Processes all FASTA files in the specified folder."""
        for fasta_file in self.fasta_folder.glob("*.fasta"):
            try:
                dna = self.read_fasta(fasta_file)
                tmp_dir = Path(f"./{fasta_file.stem}.tmp")
                self.prepare_tmp_directory(tmp_dir)
                self.generate_sequences(dna, tmp_dir)
                result = self.run_prediction(fasta_file, tmp_dir)
                self.save_result(result)
                self.delete_tmp_directory(tmp_dir)
            except Exception as e:
                print(f"Error processing {fasta_file.name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Predict whether DNA sequences are lysogenic or lytic")
    parser.add_argument('--model_path', type=str, required=True, help="Path to the model")
    parser.add_argument('--fasta_folder', type=str, required=True, help="Path to folder containing FASTA files")
    parser.add_argument('--output_csv', type=str, required=True, help="CSV file to store predictions")

    args = parser.parse_args()

    analyzer = DNASequenceAnalyzer(args.model_path, args.fasta_folder, args.output_csv)
    analyzer.analyze_folder()

if __name__ == "__main__":
    main()
