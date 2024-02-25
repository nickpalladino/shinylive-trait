from shiny.express import input, render, ui
from shiny import reactive
import requests
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

ui.h1('BrAPI Trait Entity Word Cloud')
ui.input_text("base_url", "BrAPI Base URL")
ui.input_text("token", "Authorization Token")
ui.input_task_button("generate_btn", "Generate")

@render.plot(alt="Word Cloud")
@reactive.event(input.generate_btn, ignore_none=True)
def word_cloud():
    # BrAPI GET /variables
    url = input.base_url()+"/brapi/v2/variables?pageSize=100"
    
    # Include the token in the Authorization header
    headers = {"Authorization": f"Bearer {input.token()}"}
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()['result']['data']
        df = pd.json_normalize(data, meta=[['trait', 'entity'],])
        df.rename(columns={'trait.entity':'traitEntity',}, inplace=True)
        names = df['traitEntity']

        # create string for word cloud
        names_str = " ".join(traitEntity for traitEntity in df.traitEntity)
        wordcloud = WordCloud(width=800, height=400, max_font_size=200, min_font_size=10).generate(names_str)
    
        # Display the generated image:
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')  # Don't show axes for a cleaner look
    
    else:
        # Handle request errors
        print(f"Error: {response.status_code}")
