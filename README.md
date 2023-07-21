# CS Big Cows List
List of people with great achievements in Computer Science.

## Docker Setup
Build docker image and run the container:
```
chmod u+x docker_run.sh
./docker_run.sh
```
To stop the docker container:
```
exit
```

## ACM awards WordCloud
The second part of this repository includes how to create a wordcloud regarding the ACM turing and fellow winners based on which category of computer science field they did that won the award. The category field was classified based on the award citation from the ACM website. The code utilized ChatGpt to generate the top CS fields which was contributed by the winners and perform the classification for each of the winners to the CS fields. Finally, we present the result as a word cloud which can be found in `gpt-classification/word_cloud`.

The code to generate this wordcloud can be run as follows:
```
pip install -r requirements.txt
cd gpt-classification
./run.sh {award_name}
```
where `award_name` covered right now are acm_turings and acm_fellows.

### GPT-Classification Codes Summary
Read this if you want to reuse this code for generalizing for more awards.

The script consists of 3 different codes:
1. `python3 award_tokenizer.py --award_name --checkpoint` which retrieved the csv file consists of list of the award winner which include their `citation` fields and the checkpoint file (as described below). The code generated prompt which includes citations and sent it to openai api to retrieve the classification of the citations into CS categories, producing `{award_name}_categories.json`. 
2. `python3 category_list.py --award_name --checkpoint` which retrieved the csv file consists of list of the CS categories produced by the `award_tokenizer.py` and the checkpoint file (as described below). The code will generate CS categories based on the award name and then distribute the category list `{award_name}_categories.txt` to these CS categories and write the output to `{award_name}_categories.json`.
3. `python3 category_list.py --award_name --checkpoint` which retrieved `{award_name}_categories.json` and create a word cloud based on the distribution.

Remarks: All checkpoints argument shared the same use cases in case the script crash due to certain issues (insufficient gpt tokens, exceptions, etc). The checkpoint consists of the next line of the csv file that should be processed.
  
