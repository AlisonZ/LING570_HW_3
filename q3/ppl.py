import sys

WORD_NUM = 0
OOV_NUM = 0
SENTENCE_COUNT = 0
DATA = {}
UNIGRAMS = {}
BIGRAMS = {}
TRIGRAMS = {}

def calculate_perplexity(test_data, lm_file):
    with open(test_data, 'r', encoding='utf8') as file:
        global SENTENCE_COUNT, WORD_NUM, OOV_NUM
        lines = file.readlines()
        SENTENCE_COUNT = len(lines)
        for line in lines:
            split_line = line.split()
            BOS = split_line.pop(0)
            EOS = split_line.pop(-1)
            WORD_NUM += len(split_line)
            split_line.append(EOS)
            for word in split_line:
                if word in UNIGRAMS:
                    # TODO: compute interpolated probability here
                    print("WWWORD", word)
                else:
                    OOV_NUM +=1

                # if word in lm_file --> compute probabilities

def get_final_perplexity():
    count = WORD_NUM + SENTENCE_COUNT - OOV_NUM
    # TODO: calculate per slide

def load_lm(lm_file):
    with open(lm_file, 'r', encoding='utf8') as file:
        lines = file.readlines()
        current_section = ''
        for line in lines:
            if line.startswith('\\data\\'):
                current_section = 'data'
            if line.startswith('\\1-grams'):
                current_section = 'unigram'
            if line.startswith('\\2-grams'):
                current_section = 'bigram'
            if line.startswith('\\3-grams'):
                current_section = 'trigram'

            if current_section == 'data':    
                split = line.split()
                if len(split) > 1:
                    split.pop(0)
                    n_gram = split[0]
                    type = split[1]
                    type_val = type.split("=")[1]
                    token = split[2]
                    token_val = token.split("=")[1]
                    data_object = {n_gram: {'type': type_val, 'token': token_val}}
                    DATA.update(data_object)
            if current_section == 'unigram':
                split = line.split()
                if len(split) > 1:
                    count = split[0]
                    prob = split[1]
                    logProb = split[2]
                    token = split[3]
                    data_object = {token: {'count': count, 'prob': prob, 'logProb': logProb}}
        
                    UNIGRAMS.update(data_object)

            if current_section == 'bigram':
                split = line.split()
                if len(split) > 1:
                    count = split[0]
                    prob = split[1]
                    logProb = split[2]
                    token = " ".join(split[3:5])
                    data_object = {token: {'count': count, 'prob': prob, 'logProb': logProb}}
                        
                    BIGRAMS.update(data_object)
            if current_section == 'trigram':
                split = line.split()
                if len(split) > 1:
                    count = split[0]
                    prob = split[1]
                    logProb = split[2]
                    token = " ".join(split[3:6])
                    data_object = {token: {'count': count, 'prob': prob, 'logProb': logProb}}
                    TRIGRAMS.update(data_object)
                        
def read_inputs():
    if len(sys.argv) !=7:
        print("Need to call this with 6 files")

    lm_file = sys.argv[1]
    lamdba_1 = sys.argv[2]
    lambda_2 = sys.argv[3]
    lambda_3 = sys.argv[4]
    test_data = sys.argv[5]
    output_file = sys.argv[6]
    return lm_file, lamdba_1, lambda_2, lambda_3, test_data, output_file

def main():
    lm_file, lamdba_1, lambda_2, lambda_3, test_data, output_file = read_inputs()
    load_lm(lm_file)
    # print("DATA", DATA)
    # print("UNI", UNIGRAMS)
    # print("BI", BIGRAMS)
    # print("TRI", TRIGRAMS)

    calculate_perplexity(test_data, lm_file)
main()
    