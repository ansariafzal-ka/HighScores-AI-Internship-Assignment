# AI-Driven Adaptive Diagnostic Engine

This project implements a 1D adaptive diagnostic testing engine using FastAPI and MongoDB.
The system dynamically selects questions based on the student's ability score and updates
their proficiency using an Item Response Theory (IRT) model.

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- MongoDB Atlas account (or local MongoDB)
- OpenAI API Key

### 2 Installation

```
# Clone repository
git clone https://github.com/ansariafzal-ka/HighScores-AI-Internship-Assignment.git
cd HighScores-AI-Internship-Assignment

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **3. Environment Variables**

Create a `.env` file in the root directory:

```
MONGODB_URI=your_mongodb_connection_string
MONGODB_DATABASE=adaptive_testing
OPENAI_API_KEY=your_openai_api_key
```

### 4. Seed Database

```
python src/utils/seed.py
```

### 5. Run Application

```
uvicorn app:app --reload
```

You can test the app using `http://localhost:8000/docs`

## Adaptive Testing Logic

The system implements a simplified 1D Item Response Theory (IRT) model.

```python
def update_score_irt(is_correct: bool, ability_score: float, difficulty: float) -> float:
    """
    This function takes the correct flag, ability_score of the student and difficulty of the question
    and implements a simplified 1D Item Response Theory (IRT) model.
    """
    prob_correct = 1 / (1 + math.exp(-(ability_score - difficulty))) # this will give a probability between 0-1
    learning_rate = 0.3 # step size for adjusting the ability score

    if is_correct:
        # increase the ability_score
        ability_score += learning_rate * (1 - prob_correct)
    else:
        # decrease the ability score
        ability_score -= learning_rate * prob_correct

    # clamping the score between 0 and 1
    return max(0.0, min(1.0, ability_score))
```

1. Each student starts with an initial ability score of **0.5**.
2. Each question has a **difficulty parameter** between 0 and 1.
3. The system computes the **probability of answering correctly** using a logistic function:

   P(correct) = 1 / (1 + e^-(ability - difficulty))

4. If the student answers correctly, their ability score increases slightly.
5. If the answer is incorrect, the ability score decreases slightly.
6. The adjustment magnitude is controlled by a **learning rate (0.3)**.
7. After updating, the ability score is **clamped between 0.0 and 1.0** to keep it within valid bounds.
8. The next question selected is the one whose **difficulty is closest to the student's updated ability score**.

This allows the test to dynamically adapt to the student's skill level.

## AI Usage Log

AI tools (ChatGPT) were used during development to assist with:

- Designing FastAPI API routes
- Structuring MongoDB data models
- Debugging adaptive question selection logic
- Implementing ability score updates using IRT concepts
- Writing documentation

All final implementation, testing, and integration were reviewed and verified manually.

## API Endpoints

### 1. Start Test

POST /start-test

Creates a new adaptive test session.

Response:

- session_id
- first question

### 2. Submit Answer

POST /submit-answer

Submit answer for the current question.

Request Body:
{
"session_id": "string",
"question_id": "string",
"selected_option": "string"
}

### 3. Get Next Question

GET /next-question/{session_id}

Returns the next question based on the student's updated ability score.

### 4. End Test

POST /end-session

Ends the session and generates a personalized study plan using gpt-3.5-turbo.
