from gpt_tokenizer import GPTTokenizer
import pandas as pd
import time
import argparse

BATCH_SIZE = 60

# batch list of items into list of batch of size batch_size
def batch(iterable, batch_size):
    l = len(iterable)
    res = []
    for ndx in range(0, l, batch_size):
        res.append(iterable[ndx:min(ndx + batch_size, l)])
    return res


# receive award csv file and tokenize cs fields related to the citations
class AwardTokenizer:

    def __init__(self, csv_award_name, batch_size = BATCH_SIZE):
        self.award_name = csv_award_name
        self.batch_size = batch_size
        self.batch_index = 0

        award_df = pd.read_csv(f"acm_csv/{csv_award_name}.csv")
        self.citations = award_df['Citation'].values.tolist()
    
    def __preprocess(self):
        tokenizer_prompt = f"""
            Please tokenize the citations from the following list. 
            The output is list of tokens consisting ONLY computer science topics covered in the citations. 
            Perform this for each citations and for each line, split the tokens with comma, 
            and return just index number if citation is an empty string
        """
        self.tokenizer = GPTTokenizer(tokenizer_prompt)
        self.citation_batches = batch(self.citations, self.batch_size)

    def run_classifier(self, checkpoint_txt = None):
        if checkpoint_txt:
            with open (checkpoint_txt, 'w+') as f:  
                line = f.readline()
                if line:
                    self.batch_index= int(line.split(':')[-1])
                
        self.__preprocess()

        txt_award_name = f'categories/{self.award_name}_categories.txt'
        # run prompt on the given list
        with open(txt_award_name, 'r', newline='') as file:
            line_index = len(file.readlines())

        with open(txt_award_name, 'a', newline='') as file:
            for i, cit_batch in enumerate(self.citation_batches[self.batch_index:]):
                try:
                    # match the batch with the current line of the citations that will be processed
                    if (self.batch_index+i+1) * self.batch_size <= line_index:
                        continue
                    elif line_index < (self.batch_index+i+1) * self.batch_size \
                        and (self.batch_index+i) * self.batch_size < line_index:
                        cit_batch = cit_batch[line_index- (self.batch_index+i) * self.batch_size:]

                    # tokenize the citation batch
                    token_list = self.tokenizer.generate_response(cit_batch)
                    print(f'finished batch {self.batch_index + i}')
                    for token in token_list:
                        file.write(token + '\n')
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
    award_tokenizer = AwardTokenizer(award_name)
    award_tokenizer.run_classifier(checkpoint_txt)
    

    