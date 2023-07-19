import argparse
import json
from wordcloud import WordCloud


def generate_word_cloud(json_file, output_file):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Create a word cloud object
    wordcloud = WordCloud(width=1600, height=800, max_font_size=120, max_words=100, background_color='white')
    
    # Generate the word cloud from the data
    wordcloud.generate_from_frequencies(data)
    
    # Save the word cloud as a JPEG image
    wordcloud.to_file(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parse word cloud input award_name')
    parser.add_argument('award_name', type=str,
                        help='categories name')
    args = parser.parse_args()
    award_name = args.award_name

    # convert to categories json to word cloud
    json_file = f'categories/{award_name}_categories.json' 
    output_file = f'word_cloud/{award_name}_word_cloud.jpg'  
    generate_word_cloud(json_file, output_file)
