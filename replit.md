# きもちのいろ (Colors of Feelings)

## Overview
A child-friendly emotion tracking web application that helps children identify and express their feelings through colors. The app uses AI to provide empathetic, supportive messages based on what they write about their emotions.

## Purpose
To help children:
- Recognize and name their emotions in a safe, non-judgmental way
- Express their feelings freely through writing
- Receive validating, supportive responses from AI
- Build emotional awareness through simple, color-based interactions
- Track their emotional journey over time

## Current Features
- **7 Emotion Categories**: Each represented by a color
  - Red: Angry/Frustrated (怒ってる時・イライラしてる時)
  - Blue: Lonely/Sad (寂しい時・しょんぼりしてる時)
  - Yellow: Anxious/Surprised (落ち着かない時・びっくりした時)
  - Green: Calm/Relieved (落ち着いてる時・ホッとしてる時)
  - Pink: Happy/Joyful (嬉しい時・楽しい時)
  - Purple: Confused/Uncertain (モヤモヤしてる時・よく分からない気持ちの時)
  - Black: Tired/Overwhelmed (疲れてる時・何も考えたくない時)

- **Interactive User Flow**:
  1. Child selects a color representing their emotion
  2. Optional text input to freely express their thoughts and feelings
  3. AI generates a personalized, short, empathetic message based on their input
  4. All interactions are saved to database for future reference

- **AI-Generated Empathetic Messages**: Uses OpenAI GPT-4o-mini to generate warm, supportive responses based on user input
- **Emotion Logging**: PostgreSQL database stores all emotion check-ins with timestamps
- **History View**: Children can review their past emotions and AI messages (last 50 entries)
- **Child-Friendly Design**: Soft pastel colors, rounded shapes, smooth animations
- **Japanese Language Support**: Full interface in Japanese for accessibility

## Recent Changes
- **November 14, 2025**: Major feature update
  - **New user flow**: Color selection → Text input → AI message generation
  - **Database integration**: Added PostgreSQL for persistent emotion logging
  - **Input form**: Children can write about their feelings (optional)
  - **AI prompt enhancement**: Messages now personalized based on user input, shorter (50 chars)
  - **Logs page**: View history of emotions with timestamps
  - **Navigation**: Added links between all pages (Home, Input, Result, Logs)
  - **Error handling**: Comprehensive logging and graceful error messages
  - **Styling updates**: New CSS for input forms and log display

- **November 14, 2025**: Initial project setup
  - Created Flask web application structure
  - Set up templates and static CSS
  - Configured OpenAI API integration with modern client syntax
  - Added workflow configuration to run on port 5000
  - Implemented graceful handling for missing API key

## Technical Stack
- **Backend**: Flask (Python)
- **Database**: PostgreSQL (Replit-managed)
- **AI**: OpenAI GPT-4o-mini
- **Frontend**: HTML5, Jinja2 templates, CSS3
- **Hosting**: Replit with environment variable management

## Project Structure
```
.
├── main.py                 # Flask application, routes, and database logic
├── templates/
│   ├── index.html         # Color selection page with navigation
│   ├── input.html         # Text input form for expressing feelings
│   ├── result.html        # AI message display page
│   └── logs.html          # Emotion history display page
├── static/
│   └── style.css          # Comprehensive styling with child-friendly design
└── replit.md              # This file
```

## Database Schema
```sql
CREATE TABLE emotion_logs (
    id SERIAL PRIMARY KEY,
    color VARCHAR(20) NOT NULL,
    emotion_label VARCHAR(100) NOT NULL,
    user_input TEXT,
    ai_message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Setup Requirements
- **Python 3.11+**
- **Dependencies**: Flask, psycopg2-binary, openai (managed via uv)
- **PostgreSQL Database**: Automatically provided by Replit
- **OpenAI API Key**: Required for AI message generation
  - Set as `OPENAI_API_KEY` environment variable
  - Get your key at https://platform.openai.com/api-keys

## How It Works
1. Child selects a colored circle representing their current emotion
2. App displays an input form where they can write about their feelings (optional)
3. Child clicks "メッセージをもらう" to submit
4. AI analyzes both the emotion color and user input to generate a personalized message
5. Message is displayed in a soft, rounded box with warm styling
6. Emotion, input, and AI message are saved to the database
7. Child can view their emotion history in the "記録を見る" page
8. All pages have navigation links for easy movement between screens

## Future Enhancements (Not Yet Implemented)
- Mood visualization with charts and graphs
- Parent/teacher dashboard with privacy controls
- Export logs as PDF or printable format
- Emotion patterns analysis
- Multi-language support (English, etc.)

## User Preferences
None documented yet.

## Notes
- The app is designed for children, so all messaging is warm, non-judgmental, and supportive
- AI is instructed to never deny or dismiss feelings, only validate and comfort
- The design uses soft colors and playful elements to feel safe and inviting
- User input is optional - children can submit without writing anything
- Database logs help track emotional patterns over time
