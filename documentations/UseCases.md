# Use Cases
I have defined 3 use cases for this project
## Scraping news
Taking news data from online website. For simplicity, I will use HuggingFace's  [multi_news](https://huggingface.co/datasets/multi_news) dataset.

Input: news text

Output: None

## Content NER Extraction
From those news data, I will extract the Named Entities (NE) with [stanza](https://stanfordnlp.github.io/stanza/) and store the NE categories into a database.

Input: `["Barrack", "Obama"]`

Output: `["B-PERSON", "E-PERSON"]`

## Named entity search
1. First, users will be able to search the NE categories available in the database

    Input: `per`

    Output: `["Person", "Percent"]`

2. Then after users type, autocomplete showed up, they will be able to select one of the NE categories
3. Users will be able to see news related to the NE categories.
    
    Input: `Person`
    
    Output: `["Today news 1, a girl...", "Today news 2, a man found..."]`