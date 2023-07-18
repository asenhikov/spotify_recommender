# Spotify Music Recommender README

This is a music recommender system that given an input song extracts similar songs by extracting songs of the same genre, performing clustering on the audio attributes for each song, and recommends  utilizes OpenAI's GPT-3.5 model to write descriptions for the recommended songs.
## Features

- Generates recommendations for similar songs based on user input.
- Provides short descriptions for all recommended songs and explains why they are similar.

## Setup

1. Clone the repository:
2. Install the required dependencies:

pip install requirements.txt

3. Set up your authentication:
- Rename the `.env_example` to `.env`
- Inside the `.env` file, fill the OPENAI_APIKEY
- You can get the spotify credentials from here: https://developer.spotify.com/dashboard by creating a new app.

4. Run the recommender from the SpotifySongRecommender.ipynb



## Usage

1. Enter the input song:
- Provide the input song in the format: `Songname`.
- For example: `The less i know the better`

2. View the recommendations:
- The system will generate similar song recommendations along with short descriptions explaining their similarities.


## NOTE
Please note that the song features extraction is currently unavailable due to rate limits imposed by Spotify's API. As a workaround, the recommender uses a spotify dataset, `data.csv`, obtained from Kaggle, which is used for clustering and generating recommendations. Consequently, the recommender can only accept songs that are present in the dataset.