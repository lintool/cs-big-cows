from gpt_tokenizer import GPTTokenizer
import time
from collections import defaultdict
import json
import argparse

BATCH_SIZE = 100

# batch list of items into list of batch of size batch_size
def batch(iterable, batch_size):
    l = len(iterable)
    res = []
    for ndx in range(0, l, batch_size):
        res.append(iterable[ndx:min(ndx + batch_size, l)])
    return res


# receive categories txt file produced from category tokenizer 
# and classify the categories based on category_list.txt
class CategoryClassifier:

    def __init__(self, award_name, batch_size = BATCH_SIZE):
        self.award_name = award_name
        self.batch_size = batch_size
        self.batch_index = 0

        categories_list_file = f'category_list/{award_name}_category_list.txt'
        categories_file = f'categories/{award_name}_categories.txt'
        self.categories = []
        self.category_list = []

        with open(categories_list_file, 'r') as file:
            self.category_list = [c[:-1] if c[-1] == '\n' else c for c in file.readlines()]

        with open(categories_file, 'r') as file:
            self.categories = [c[:-1] if (len(c) > 0 and c[-1] == '\n') else c for c in file.readlines()]
    
    def __preprocess(self):
        tokenizer_prompt = f"""
            Given list of group name [{", ".join(self.category_list)}], 
            categorize each lines into one or more group in the list that's most relevant,
            the return output is subset of the group list and return "Others" if nothing is relevant 
            or return "Missing" if line is empty string:
        """
        self.tokenizer = GPTTokenizer(tokenizer_prompt)
        self.category_batches = batch(self.categories, self.batch_size)

    def run_classifier(self, checkpoint_txt = None):
        if checkpoint_txt:
            with open (checkpoint_txt, 'w+') as f:  
                line = f.readline()
                if line:
                    self.batch_index= int(line.split(':')[-1])

        category_dict = defaultdict(int)
        self.__preprocess()

        # run prompt on the given list
        for i, category_batch in enumerate(self.category_batches[self.batch_index:]):
            try:
                cat_list = self.tokenizer.generate_response(category_batch)
                print(f'finished batch {self.batch_index + i}')

                 # check if parsed category is inside category_list
                for line in cat_list:
                    if line != '' and line[-1] == '.':
                        line = line[:-1]

                    for cat in line.split(', '):
                        if cat in self.category_list or cat == 'Others' or cat == 'Missing':
                            category_dict[cat] += 1
                
                self.batch_index += 1
                time.sleep(30)
            
            # exception handler, updating checkpoint to the current batch checkpoint
            except KeyboardInterrupt:
                print("Program forced to stop")
                with open (checkpoint_txt, 'w+') as f:  
                    f.write(f'last batch: {self.batch_index}')  
                break       
            except Exception as e:
                print(f"Exception occured causing program to stop: {e}")
                with open (checkpoint_txt, 'w+') as f:  
                    f.write(f'last batch: {self.batch_index}')  
                break

        json_object = json.dumps(category_dict, indent=4)
        with open(f"categories/{self.award_name}_categories.json", "w+") as outfile:
            outfile.write(json_object)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parse award csv input award_name')
    parser.add_argument('award_name', type=str,
                        help='categories name')
    parser.add_argument('checkpoint', type=str,
                        help='checkpoint file')
    args = parser.parse_args()
    award_name = args.award_name
    checkpoint_txt = args.checkpoint

    # tokenize citations csv into cs fields related to each citation
    award_tokenizer = CategoryClassifier(award_name)
    award_tokenizer.run_classifier(checkpoint_txt)
