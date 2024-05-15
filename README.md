# Art App
The Art App is designed to provide an unbiased platform for artists to share their in sight art to spectators.
In sight art refers to art that is either physical, or performative art taking place in the physical environment.
The application is built with Python and Flask. It allows artists and spectators to create user accounts. 
User status will be granted based on their roles (artist/spectator), with the possibility of verified status for artists.
One of the key components of this app is a map feature to find artists' works. Additionally, the app will have a rating system, 
a search function for users and art type, and a schegule/timetable for the art.

## Features

- **User Accounts**: Users can register and log in.
- **User Roles**: Accounts for artists and spectators.
- **Verified Artists**: Artists can apply for verified status.
- **Schedule**: For upcoming shows nearby/artist schegule.
- **Map View**: See artists' works on a map, including schegule times.
- **Art Types**: Type of art, (ex. physical or performative).
- **Rating System**: Users can rate artworks.
- **Search Function**: Search for art by type and use filters.

## Installation
Instructions for setting up the project locally.

1. Clone this repository:
```sh
git clone
```
2. Navigate to the project directory:
```sh
cd art-app
```
3. Create and activate virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
```
4. Install required dependencies:
```sh
pip install -r requirements.txt
```
5. Run application:
```sh
flask run
```

## User usage: Spectator
- Register user account type "Spectator".
- Complete user profile.
- Find art through map, schedule, search or filter.
- Rate artworks upon viewing.

## User usage: Artist
- Register user account type "Artist".
- Complete artist profile.
- Set up upcoming artshows.
- Artist accounts include all spectator functionalities.

## Contact
For any inquiries please contact niki.pouladi@helsinki.fi.
