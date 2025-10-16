import math
import sys

N_GRAM_DATA = {}
UNIGRAM_DATA = {}
BIGRAM_DATA = {}
TRIGRAM_DATA = {}

def print_data(lm_file):
    with open(lm_file, 'a') as file:
        print("\\data\\", file=file)
        for k, v in N_GRAM_DATA.items():
            print(f"{k}: type={v['type']} token={v['token']}", file=file)
        print(file=file)
def find_unigram_probs(lm_file):
    with open(lm_file, 'a') as file:
        total_count = N_GRAM_DATA['ngram 1']['token']
        print("\\1-grams", file=file)
        for key,value in UNIGRAM_DATA.items():
            prob = value / total_count
            log_prob = math.log10(prob)
            print(f'{value} {prob} {log_prob} {key}', file=file)
        print(file=file)

def find_bigram_probs(lm_file):
    with open(lm_file, 'a') as file:
        print("\\2-grams", file=file)
        for item, value in BIGRAM_DATA.items():
            bigram_count = value
            w1 =  item.split()[0]
            unigram_count = UNIGRAM_DATA.get(w1)
            prob = bigram_count / unigram_count
            log_prob = math.log10(prob)
            print(f'{value} {prob} {log_prob} {item}', file=file)
        print(file=file)

def find_trigam_probs(lm_file):
    with open(lm_file, 'a') as file:
        print("\\3-grams", file=file)
        for item, value in TRIGRAM_DATA.items():
            trigam_count = value
            split_bigram = item.split()[0:-1]
            bigram = " ".join(split_bigram)
            bigram_count = BIGRAM_DATA.get(bigram)
            prob = trigam_count / bigram_count
            log_prob = math.log10(prob)
            print(f'{value} {prob} {log_prob} {item}', file=file)
        print(file=file)

def add_data(current_n, n_gram, token_count):
    string_n_gram = " ".join(n_gram)
    if current_n == 1:
        UNIGRAM_DATA[string_n_gram] = token_count
    if current_n == 2:
        BIGRAM_DATA[string_n_gram] = token_count
    if current_n == 3:
        TRIGRAM_DATA[string_n_gram] = token_count

def update_ngram_data():
    uni_values = UNIGRAM_DATA.values()
    uni_total_tokens = sum(uni_values)
    uni_types = len(UNIGRAM_DATA)

    bi_values = BIGRAM_DATA.values()
    bi_total_tokens = sum(bi_values)
    bi_types = len(BIGRAM_DATA)

    tri_values = TRIGRAM_DATA.values()
    tri_total_tokens = sum(tri_values)
    tri_types = len(TRIGRAM_DATA)

    N_GRAM_DATA['ngram 1'] = {'type': uni_types, 'token': uni_total_tokens}
    N_GRAM_DATA['ngram 2'] = {'type': bi_types, 'token': bi_total_tokens}
    N_GRAM_DATA['ngram 3'] = {'type': tri_types, 'token': tri_total_tokens}

def get_probs(count_file):
    with open(count_file, 'r', encoding='utf8') as file:
        tokens = file.readlines()    
        current_n = 1
        n_gram = f'ngram {current_n}'
        n_gram_data = N_GRAM_DATA[n_gram]
        total_n_gram_counts = int(n_gram_data['token'])
        
        print(f"{current_n}-grams:")
        
        for token in tokens:
            split_token = token.split()
            token_count = int(split_token[-1])
            token_data = split_token[0:-1]
            if len(token_data) == current_n:
               calculate_probs(total_n_gram_counts, token_count)
            else:
                current_n +=1
                print(f"{current_n}-grams:")
                calculate_probs(total_n_gram_counts, token_count)

def get_counts(count_file):
    with open(count_file, 'r', encoding='utf8') as file:
        lines = file.readlines()

        current_n = 1
        for line in lines:
            token_data = line.split()
            token_count = int(token_data[-1])
            n_gram = token_data[0:-1]
        
            if len(n_gram) == current_n:
                add_data(current_n, n_gram, token_count)
            else:
                # Increase current-n to next
                current_n +=1
                add_data(current_n, n_gram, token_count)

def get_input_files():
    if len(sys.argv) !=3:
        print("Need to call this with 2 files")
    
    n_gram_count_file = sys.argv[1]
    lm_file = sys.argv[2]
    return n_gram_count_file, lm_file

def main():
    n_gram_count_file, lm_file = get_input_files()
    get_counts(n_gram_count_file)
    update_ngram_data()
    print_data(lm_file)
    find_unigram_probs(lm_file)
    find_bigram_probs(lm_file)
    find_trigam_probs(lm_file)
main()