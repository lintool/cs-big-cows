#!/bin/bash
award_name=$1

python3 award_tokenizer.py --award_name=$award_name --checkpoint=checkpoints/$award_name-tokenizer.txt
python3 category_classifier.py --award_name=$award_name --checkpoint=checkpoints/$award_name-category.txt
python3 word_cloud.py --award_name=$award_name