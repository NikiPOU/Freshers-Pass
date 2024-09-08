# Freshers Pass
The Freshers Pass is designed for BSc freshers starting in 2024 as a fun way to encourage them to attend more events and engage actively.
The pass supports two types of users: tutors and freshers. Tutors can create challenges and award points based on these challenges. They can mark challenges as completed only for freshers within their group.
For freshers, the goal is to accumulate as many points as possible, and the pass is designed to track their progress.

## Features

- **User Accounts**: Users can register and log in.
- **User Roles**: Accounts for freshers and spectators.
- **Challenges**: Tutors can post challenges for freshers.
- **Point system**: Freshers can gather points based on completed challenges.
- **Profiles**: Users can view their own profiles, and only see their own points.
- **Feed**: Feed consisting of challenges.

## Installation
Instructions for setting up the project locally.

1. Clone this repository:
```sh
git clone https://github.com/NikiPOU/Freshers-Pass.git
```
2. Navigate to the project directory:
```sh
cd Freshers-Pass
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

## User usage: Fresher
- Register fresher account via "Sign Up", and receive email confirmation.
- Complete fresher profile.
- View available challenges through feed.
- View your own profile/points.

## User usage: Tutor
- Register tutor account via /tutorsignup.
- Complete tutor profile.
- View & create challanges through feed.
- View your own profile.
- Authorization to mark challenges as completed for freshers in own (tutor) group.

## Note:
For full feature exploration, please create a tutor account and at least one fresher account assigned to the same (tutor) group. Then create challenges via tutor profile and mark completion for freshers accordingly.
  
## Contact
For any inquiries please contact niki.pouladi@helsinki.fi.
