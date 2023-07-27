# SpotPlay - Music Recommendation Web App

SpotPlay is a music recommendation web application that provides personalized song recommendations based on an input song. It uses the Spotify Web API to fetch audio features of songs and applies content-based filtering to suggest similar tracks.

## Features

- Content-based music recommendation: Given a song link, SpotPlay suggests similar tracks based on audio features like danceability, valence, liveness, and energy.
- User-friendly interface: SpotPlay has a simple and intuitive user interface for easy navigation and input.
- Create Spotify playlist: The web app creates a new Spotify playlist with the recommended songs, allowing users to listen to the suggested tracks conveniently.

## Installation

1. Clone the repository to your local machine.

git clone https://github.com/your-username/SpotPlay.git
cd SpotPlay

2. Create a virtual environment and activate it.

python3 -m venv venv
source venv/bin/activate #for mac os
venv\Scripts\activate #for windows

3. Install the required dependencies.

pip install -r requirements.txt


## Usage

1. Set up Spotify API credentials:
   - Create a Spotify developer account and create a new app to get your client ID and client secret.
   - Update the `keys.py` file with your Spotify API credentials.

2. Run the Flask web application:

python app.py

markdown
Copy code

3. Access the web app:
   - Open your web browser and go to `http://127.0.0.1:5000/`.
   - Enter the link to your favorite song in the input field and click the "Get Recommendations" button.
   - The web app will provide a list of recommended songs based on the input track and create a new Spotify playlist with these recommendations.

## Troubleshooting

- If you encounter any issues related to the Spotify API or authorization, make sure you have provided valid Spotify API credentials in the `keys.py` file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.