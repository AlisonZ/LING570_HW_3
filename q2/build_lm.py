N_GRAM_DATA = {}
def print_data():
    print("data: ")
    print(N_GRAM_DATA)

def handle_processed_counts(current_n, count):
    processed_n_gram = f"ngram {current_n}"
    N_GRAM_DATA[processed_n_gram] = {'type': current_n}
    N_GRAM_DATA[processed_n_gram] = {'token': count}

def get_counts():
    count_file = '../q1/ngram_count_file'
    with open(count_file, 'r', encoding='utf8') as file:
        lines = file.readlines()

        current_n = 1
        count = 0
        for line in lines:
            token_data = line.split()
            token_count = int(token_data[-1])
            n_gram = token_data[0:-1]
        
            if len(n_gram) == current_n:
                print("====", n_gram)
                count +=token_count
            else:
                # Add data for the n-gram that just finished processing
                # TODO: what is type supposed to be?
                handle_processed_counts(current_n, count)

               
                # Reset count for new n-gram
                # Increase current-n to next
                current_n +=1
                count = 0

                # Add count for new n-gram
                count += token_count
            handle_processed_counts(current_n, count)
        
def main():
    get_counts()
    print_data()


main()