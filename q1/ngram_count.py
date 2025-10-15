import sys

UNIGRAM_DICT = {}
BIGRAM_DICT = {}
TRIGRAM_DICT = {}

def print_results(token_dict, output_file):
    sorted_dict = {
        k: v for k, v in sorted(
        token_dict.items(),
        key=lambda item: (-item[1], item[0])  # negative for descending value
    )
    }
    for key, value in sorted_dict.items():
        with open(output_file, 'a') as file:
            print(f"{key}   {value}", file=file)    

def create_trigram(split_line):
    length = len(split_line)
    for i in range(length):
        if i+2 < length:
            trigram = f'{split_line[i]} {split_line[i+1]} {split_line[i+2]}'
            if trigram in BIGRAM_DICT:
                TRIGRAM_DICT[trigram] +=1
            else:
                TRIGRAM_DICT[trigram] =1

def create_unigram(split_line):
    for token in split_line:
        if token in UNIGRAM_DICT:
            UNIGRAM_DICT[token] +=1
        else:
            UNIGRAM_DICT[token] = 1

def create_bigram(split_line):
    length = len(split_line)
    for i in range(length):
        if i+1 < length:
            bigram = f'{split_line[i]} {split_line[i+1]}'
            if bigram in BIGRAM_DICT:
                BIGRAM_DICT[bigram] +=1
            else:
                BIGRAM_DICT[bigram] =1

def read_file(data_file):
    with open(data_file, 'r', encoding='utf8') as file:
        lines = file.readlines()
        for line in lines:
            split_line = line.split()
            split_line.insert(0, '<s>')
            split_line.append('</s>')

            create_unigram(split_line)
            create_bigram(split_line)
            create_trigram(split_line)

def get_input_files():
    if len(sys.argv) !=3:
        print("Need to call this with 2 files")
    
    training_data = sys.argv[1]
    ngram_count_file = sys.argv[2]
    return training_data, ngram_count_file

def main():
    training_data, ngram_count_file = get_input_files()    

    read_file(training_data)
    print_results(UNIGRAM_DICT, ngram_count_file)
    print_results(BIGRAM_DICT, ngram_count_file)
    print_results(TRIGRAM_DICT, ngram_count_file)

main()