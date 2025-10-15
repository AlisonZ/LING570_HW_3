import math

N_GRAM_DATA = {}
UNIGRAM_DATA = {}
BIGRAM_DATA = {}
TRIGRAM_DATA = {}

# TODO: update the type once determine what it is
def print_data():
    print("\\data\\")
    for k, v in N_GRAM_DATA.items():
        print(f"{k}: type={v['type']} token={v['token']}")
    print()

# TODO -check that probs are not 0
# TODO: add the first column value for all prob reporting
def find_unigram_probs():
    total_count = N_GRAM_DATA['ngram 1']['token']
    print("\\1-grams")
    for key,value in UNIGRAM_DATA.items():
        prob = value / total_count
        log_prob = math.log10(prob)
        print(f'{prob} {log_prob} {key}')

    print()

def find_bigram_probs():
    print("\\2-grams")
    for item, value in BIGRAM_DATA.items():
        bigram_count = value
        w1 =  item.split()[0]
        unigram_count = UNIGRAM_DATA.get(w1)
        prob = bigram_count / unigram_count
        log_prob = math.log10(prob)
        print(f'{prob} {log_prob} {item}')
    print()

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

    bi_values = BIGRAM_DATA.values()
    bi_total_tokens = sum(bi_values)

    tri_values = TRIGRAM_DATA.values()
    tri_total_tokens = sum(tri_values)

    # TODO! What are the types???
    N_GRAM_DATA['ngram 1'] = {'type': 1, 'token': uni_total_tokens}
    N_GRAM_DATA['ngram 2'] = {'type': 2, 'token': bi_total_tokens}
    N_GRAM_DATA['ngram 3'] = {'type': 3, 'token': tri_total_tokens}

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
        
def main():
    count_file = '../q1/ngram_count_file'
    get_counts(count_file)
    update_ngram_data()
    print_data()
    find_unigram_probs()
    find_bigram_probs()
    # TODO implement find_trigram_probs()
main()