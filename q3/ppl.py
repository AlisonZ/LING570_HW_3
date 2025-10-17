import sys
import math

DATA = {}
UNIGRAMS = {}
BIGRAMS = {}
TRIGRAMS = {}


SENTENCE_NUM = 0
WORD_COUNT = 0
OOV_NUM = 0
LOG_PROB_SUM = 0

def print_results():
    with open('results', 'a') as file:
        print("DATA!", file=file)
        print(DATA, file=file)
        print(file=file)
        
        print("1-grams", file=file)
        print(UNIGRAMS, file=file)
        print(file=file)
        print("2-grams", file=file)
        print(BIGRAMS, file=file)
        print(file=file)

        print("3-grams", file=file)
        print(TRIGRAMS, file=file)

def get_word_probs(lamdba_1, lambda_2, lambda_3, token, sent_oov):
    split_token = token.split(" ")
    word = split_token[0]
    bigram = f"{split_token[-1]} {word}"
    trigram = f"{split_token[-2]} {split_token[-1]} {word}" if len(split_token) == 4 else ''
    total_prob = 0
    if word in UNIGRAMS:
        uni_prob = UNIGRAMS[word].get('prob')
        bi_prob = BIGRAMS[bigram].get('prob') if bigram in BIGRAMS else 0
        tri_prob = TRIGRAMS[trigram].get('prob') if trigram in TRIGRAMS else 0
        l1 = float(uni_prob) * float(lamdba_1)
        l2 = float(bi_prob) * float(lambda_2)
        l3 = float(tri_prob) * float(lambda_3)
        total_prob = l1 + l2 + l3
    
        if total_prob > 0:
            return math.log10(total_prob), 0
        else:
            # unseen gram
            return float('-inf'), 0
    else: 
        # unknown word
        return float('-inf'), 1

def get_tokens(sent_with_tags, lamdba_1, lambda_2, lambda_3, output_file):
    sentence_log = 0.0
    sent_oov = 0
    sentence = sent_with_tags.split(" ")
    for i, word in enumerate(sentence):            
        if i == 1:
            token = f"{word} | {sentence[0]}"
        if i > 1:
            token = f"{word} | {sentence[i-2]} {sentence[i-1]}"
        if i > 0:
            word_prob, oov_status = get_word_probs(lamdba_1, lambda_2, lambda_3, token, sent_oov)
            sent_oov +=oov_status
            word_status = ''
            if word_prob == float('-inf'):
                if oov_status == 0:
                    word_status = '(unseen gram)'
                if oov_status == 1:
                    word_status = '(unknown word)'

            print(f"{i}: lg P({token}) = {word_prob} {word_status}", file=output_file)
            if  word_prob != float('-inf'):
                sentence_log += word_prob
    return sentence_log, sent_oov

def get_sentence_stats(test_data, lamdba_1, lambda_2, lambda_3, output_file):
    global SENTENCE_NUM, WORD_COUNT, OOV_NUM, LOG_PROB_SUM
    with open(test_data, 'r', encoding='utf8') as file:
        with open(output_file, 'a') as output_file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                sent_with_tags = f"<s> {line} </s>"
                print(f"Sent #{i+1}: {sent_with_tags}", file=output_file)
                split_line = line.split()
            
                sentence_log, sent_oov = get_tokens(sent_with_tags, lamdba_1, lambda_2, lambda_3, output_file)
                word_count = len(split_line)
                SENTENCE_NUM +=1
                WORD_COUNT += word_count
                OOV_NUM += sent_oov
                LOG_PROB_SUM += sentence_log

                valid_words = word_count - sent_oov
                if valid_words > 0:
                    sentence_avg_log = -(sentence_log / valid_words)
                    ppl = 10 ** (sentence_avg_log)

                print(f"1 sentence, {word_count} words, {sent_oov} OOVs",file=output_file)
                print(f"lgprob={sentence_log}, ppl={ppl}", file=output_file)
                print(file=output_file)

def get_overall_stats():
    count = WORD_COUNT + SENTENCE_NUM - OOV_NUM
    avg_lgprob = - LOG_PROB_SUM / count
    ppl = 10 ** avg_lgprob
    return f"lgprob={LOG_PROB_SUM} ave_lgprob={avg_lgprob} ppl={ppl}"

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
    get_sentence_stats(test_data, lamdba_1, lambda_2, lambda_3, output_file)
    
    with open(output_file, 'a') as output_file:
        print(f"sent_num={SENTENCE_NUM} word_num={WORD_COUNT} oov_num={OOV_NUM}", file=output_file)
        overall_stats = get_overall_stats()
        print(overall_stats, file=output_file)
main()
    