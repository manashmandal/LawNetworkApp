"""
Instructions:

1. Process input query, tokenize it and prepare bigram for it
2. Run the input query through the database and fine the related laws
3. Prepare a dynamic graph using citation details

"""

# Process using this function when someone enters query
# Process text v2
def process_text_v2(input_text, tokenize=False):
    valid_list = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঅআইঈউঊঋএঐওঔৌোৈেৃূুীিা")
    filter_text = [l for l in input_text if l in valid_list]
    if tokenize == True:
        return filter_text
    else:
        return "".join(filter_text)

    return filter_text



