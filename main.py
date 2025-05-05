import json
import os
import re
import sys
from collections import Counter


def count_word_frequencies(text):
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    word_counts = Counter(words)
    return dict(word_counts)


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {str(e)}", file=sys.stderr)
        sys.exit(1)


def write_json_output(frequencies, output_file=None):
    """
    Write frequencies to JSON, either to a file or stdout
    Sort by frequency (descending) and alphabetically for equal frequencies
    """
    # Sort the dictionary by value (descending) and then by key (alphabetically)
    sorted_frequencies = dict(
        sorted(
            frequencies.items(),
            key=lambda x: (
                -x[1],
                x[0],
            ),  # Negative frequency for descending order, then word alphabetically
        )
    )
    if output_file:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(sorted_frequencies, f, indent=2)
        except Exception as e:
            print(f"Error writing to file: {str(e)}", file=sys.stderr)
            sys.exit(1)
    else:
        # Print to stdout
        print(json.dumps(sorted_frequencies, indent=2))


def main():
    print("word-frequency v1.0.0")
    import argparse

    parser = argparse.ArgumentParser(
        description="Count word frequencies and output as JSON"
    )
    parser.add_argument("input_file", help="Path to the input text file")
    parser.add_argument("-o", "--output", help="Output JSON file path (optional)")
    args = parser.parse_args()
    if not os.path.exists(args.input_file):

        print(f"Error: File '{args.input_file}' does not exist.", file=sys.stderr)
        sys.exit(1)
    input_text = read_file(args.input_file)
    frequencies = count_word_frequencies(input_text)
    write_json_output(frequencies, args.output)


if __name__ == "__main__":
    main()
