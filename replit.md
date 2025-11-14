# きもちのいろ (Colors of Feelings)

## Overview
A child-friendly emotion tracking web application that helps children identify and express their feelings through colors. The app uses AI to provide empathetic, supportive messages based on the emotion they select.

## Purpose
To help children:
- Recognize and name their emotions in a safe, non-judgmental way
- Receive validating, supportive responses from AI
- Build emotional awareness through simple, color-based interactions

## Current Features
- **7 Emotion Categories**: Each represented by a color
  - Red: Angry/Frustrated (怒ってる時・イライラしてる時)
  - Blue: Lonely/Sad (寂しい時・しょんぼりしてる時)
  - Yellow: Anxious/Surprised (落ち着かない時・びっくりした時)
  - Green: Calm/Relieved (落ち着いてる時・ホッとしてる時)
  - Pink: Happy/Joyful (嬉しい時・楽しい時)
  - Purple: Confused/Uncertain (モヤモヤしてる時・よく分からない気持ちの時)
  - Black: Tired/Overwhelmed (疲れてる時・何も考えたくない時)

- **AI-Generated Empathetic Messages**: Uses OpenAI GPT-4o-mini to generate warm, supportive responses
- **Child-Friendly Design**: Soft pastel colors, rounded shapes, smooth animations
- **Interactive Color Selection**: Hover effects that make circles grow and glow
- **Japanese Language Support**: Full interface in Japanese for accessibility

## Recent Changes
- **November 14, 2025**: Initial project setup and improvements
  - Created Flask web application structure
  - Set up templates (index.html, result.html) and static CSS
  - Configured OpenAI API integration with modern client syntax
  - Added workflow configuration to run on port 5000
  - Implemented graceful handling for missing API key
  - Added comprehensive logging (startup, API key status, API call failures)
  - Implemented try/except error handling for OpenAI API calls
  - Added user-friendly error messages in Japanese for API failures

## Technical Stack
- **Backend**: Flask (Python)
- **AI**: OpenAI GPT-4o-mini
- **Frontend**: HTML5, Jinja2 templates, CSS3
- **Hosting**: Replit with environment variable management

## Project Structure
```
.
├── main.py                 # Flask application and routes
├── templates/
│   ├── index.html         # Color selection page
│   └── result.html        # AI message display page
├── static/
│   └── style.css          # Styling with child-friendly design
└── replit.md              # This file
```

## Setup Requirements
- **Python 3.11+**
- **Flask** (installed via uv)
- **OpenAI API Key**: Required for AI message generation
  - Set as `OPENAI_API_KEY` environment variable
  - Get your key at https://platform.openai.com/api-keys

## How It Works
1. Child selects a colored circle representing their current emotion
2. App sends the emotion label to OpenAI GPT-4o-mini
3. AI generates a supportive, validating message (approx. 80 characters)
4. Message is displayed in a soft, rounded box with warm styling
5. Child can return to select another emotion

## Future Enhancements (Not Yet Implemented)
- Persistent emotion logging with database
- Mood history visualization
- Optional memo/journal feature
- Parent/teacher dashboard
- Printable emotion check-in sheets

## User Preferences
None documented yet.

## Notes
- The app is designed for children, so all messaging is warm, non-judgmental, and supportive
- AI is instructed to never deny or dismiss feelings, only validate and comfort
- The design uses soft colors and playful elements to feel safe and inviting
