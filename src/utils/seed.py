from src.configurations.mongodb_connection import MongoDBConnection
from src.utils.exception import CustomException
import sys

# 57 questions for uploading to mongodb Atlas
questions = [
    {
        "question": "If x + 3 = 7, what is x?",
        "options": ["2", "3", "4", "5"],
        "correct_answer": "4",
        "difficulty": 0.1,
        "topic": "Algebra",
        "tags": ["basic", "equations"]
    },
    {
        "question": "If 2x - 5 = 9, what is x?",
        "options": ["5", "6", "7", "8"],
        "correct_answer": "7",
        "difficulty": 0.2,
        "topic": "Algebra",
        "tags": ["linear", "equations"]
    },
    {
        "question": "What is the value of 3^4?",
        "options": ["27", "64", "81", "243"],
        "correct_answer": "81",
        "difficulty": 0.2,
        "topic": "Arithmetic",
        "tags": ["exponents"]
    },
    {
        "question": "If a rectangle has length 8 and width 5, what is its area?",
        "options": ["13", "30", "40", "45"],
        "correct_answer": "40",
        "difficulty": 0.2,
        "topic": "Geometry",
        "tags": ["area", "rectangle"]
    },
    {
        "question": "The average of five numbers is 12. What is their total sum?",
        "options": ["48", "60", "72", "84"],
        "correct_answer": "60",
        "difficulty": 0.3,
        "topic": "Arithmetic",
        "tags": ["average", "statistics"]
    },
    {
        "question": "If 40% of a number is 20, what is the number?",
        "options": ["40", "45", "50", "55"],
        "correct_answer": "50",
        "difficulty": 0.4,
        "topic": "Arithmetic",
        "tags": ["percentage"]
    },
    {
        "question": "What is the next number in the sequence: 2, 6, 18, 54, ?",
        "options": ["72", "108", "162", "216"],
        "correct_answer": "162",
        "difficulty": 0.4,
        "topic": "Sequences",
        "tags": ["pattern", "geometric"]
    },
    {
        "question": "If x^2 = 49 and x is positive, what is x?",
        "options": ["5", "6", "7", "8"],
        "correct_answer": "7",
        "difficulty": 0.3,
        "topic": "Algebra",
        "tags": ["quadratic", "roots"]
    },
    {
        "question": "A train travels 120 miles in 2 hours. What is its average speed in miles per hour?",
        "options": ["50", "55", "60", "65"],
        "correct_answer": "60",
        "difficulty": 0.2,
        "topic": "Word Problems",
        "tags": ["speed", "rate"]
    },
    {
        "question": "If the probability of an event occurring is 0.25, what is the probability it does not occur?",
        "options": ["0.25", "0.5", "0.75", "1"],
        "correct_answer": "0.75",
        "difficulty": 0.3,
        "topic": "Probability",
        "tags": ["basic"]
    },
    {
        "question": "The word 'aberration' most nearly means:",
        "options": ["Deviation", "Agreement", "Harmony", "Consistency"],
        "correct_answer": "Deviation",
        "difficulty": 0.5,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'benevolent' most nearly means:",
        "options": ["Kind", "Cruel", "Indifferent", "Hostile"],
        "correct_answer": "Kind",
        "difficulty": 0.3,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'candid' most nearly means:",
        "options": ["Honest", "Secretive", "Careless", "Confusing"],
        "correct_answer": "Honest",
        "difficulty": 0.3,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'ephemeral' most nearly means:",
        "options": ["Lasting", "Temporary", "Important", "Common"],
        "correct_answer": "Temporary",
        "difficulty": 0.6,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'pragmatic' most nearly means:",
        "options": ["Practical", "Idealistic", "Emotional", "Theoretical"],
        "correct_answer": "Practical",
        "difficulty": 0.5,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'meticulous' most nearly means:",
        "options": ["Careless", "Precise", "Lazy", "Rough"],
        "correct_answer": "Precise",
        "difficulty": 0.5,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'ambiguous' most nearly means:",
        "options": ["Clear", "Uncertain", "Certain", "Direct"],
        "correct_answer": "Uncertain",
        "difficulty": 0.4,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'resilient' most nearly means:",
        "options": ["Weak", "Fragile", "Quick to recover", "Slow"],
        "correct_answer": "Quick to recover",
        "difficulty": 0.4,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'obsolete' most nearly means:",
        "options": ["Outdated", "Modern", "Useful", "Popular"],
        "correct_answer": "Outdated",
        "difficulty": 0.3,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'lucid' most nearly means:",
        "options": ["Clear", "Confusing", "Dark", "Complex"],
        "correct_answer": "Clear",
        "difficulty": 0.4,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "Solve for x: 5x + 7 = 2x + 16",
        "options": ["3", "2", "1", "5"],
        "correct_answer": "3",
        "difficulty": 0.2,
        "topic": "Algebra",
        "tags": ["linear", "equations"]
    },
    {
        "question": "If y/4 = 6, what is y?",
        "options": ["12", "18", "24", "30"],
        "correct_answer": "24",
        "difficulty": 0.2,
        "topic": "Algebra",
        "tags": ["linear", "equations"]
    },
    {
        "question": "What is the sum of the first 20 positive integers?",
        "options": ["190", "200", "210", "220"],
        "correct_answer": "210",
        "difficulty": 0.3,
        "topic": "Arithmetic",
        "tags": ["series", "sum"]
    },
    {
        "question": "If a circle has radius 7, what is its area? (Use π = 3.14)",
        "options": ["153.86", "144.5", "154", "150"],
        "correct_answer": "153.86",
        "difficulty": 0.4,
        "topic": "Geometry",
        "tags": ["area", "circle"]
    },
    {
        "question": "If 7x - 4 = 24, what is x?",
        "options": ["2", "4", "6", "8"],
        "correct_answer": "4",
        "difficulty": 0.3,
        "topic": "Algebra",
        "tags": ["linear"]
    },
    {
        "question": "What is 15% of 200?",
        "options": ["25", "30", "35", "40"],
        "correct_answer": "30",
        "difficulty": 0.2,
        "topic": "Arithmetic",
        "tags": ["percentage"]
    },
    {
        "question": "Find the median of the numbers: 3, 7, 9, 12, 15",
        "options": ["7", "9", "12", "10"],
        "correct_answer": "9",
        "difficulty": 0.3,
        "topic": "Statistics",
        "tags": ["median"]
    },
    {
        "question": "The word 'alacrity' most nearly means:",
        "options": ["Laziness", "Eagerness", "Indifference", "Slowness"],
        "correct_answer": "Eagerness",
        "difficulty": 0.5,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'capricious' most nearly means:",
        "options": ["Predictable", "Fickle", "Reliable", "Stable"],
        "correct_answer": "Fickle",
        "difficulty": 0.6,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'diffident' most nearly means:",
        "options": ["Confident", "Shy", "Bold", "Aggressive"],
        "correct_answer": "Shy",
        "difficulty": 0.5,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'enervate' most nearly means:",
        "options": ["Energize", "Weaken", "Strengthen", "Refresh"],
        "correct_answer": "Weaken",
        "difficulty": 0.6,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'fervent' most nearly means:",
        "options": ["Apathetic", "Passionate", "Cold", "Weak"],
        "correct_answer": "Passionate",
        "difficulty": 0.4,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'garrulous' most nearly means:",
        "options": ["Talkative", "Quiet", "Serious", "Reserved"],
        "correct_answer": "Talkative",
        "difficulty": 0.5,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'harangue' most nearly means:",
        "options": ["Lecture", "Whisper", "Praise", "Applaud"],
        "correct_answer": "Lecture",
        "difficulty": 0.6,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'impecunious' most nearly means:",
        "options": ["Wealthy", "Poor", "Generous", "Famous"],
        "correct_answer": "Poor",
        "difficulty": 0.7,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'juxtapose' most nearly means:",
        "options": ["Separate", "Place side by side", "Compare carefully", "Ignore"],
        "correct_answer": "Place side by side",
        "difficulty": 0.6,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "If x^2 + 5x + 6 = 0, what are the values of x?",
        "options": ["-2 and -3", "2 and 3", "-1 and -6", "1 and 6"],
        "correct_answer": "-2 and -3",
        "difficulty": 0.5,
        "topic": "Algebra",
        "tags": ["quadratic"]
    },
    {
        "question": "If 3x + 4y = 12 and x = 2, what is y?",
        "options": ["1", "2", "3", "4"],
        "correct_answer": "1",
        "difficulty": 0.4,
        "topic": "Algebra",
        "tags": ["linear"]
    },
    {
        "question": "A rectangle has perimeter 30 and width 5. What is the length?",
        "options": ["10", "15", "20", "25"],
        "correct_answer": "10",
        "difficulty": 0.4,
        "topic": "Geometry",
        "tags": ["perimeter"]
    },
    {
        "question": "The sum of interior angles of a polygon with 8 sides is:",
        "options": ["1080", "1260", "1440", "1620"],
        "correct_answer": "1080",
        "difficulty": 0.5,
        "topic": "Geometry",
        "tags": ["angles", "polygon"]
    },
    {
        "question": "If the probability of A is 0.6 and B is 0.5, and A and B are independent, what is P(A and B)?",
        "options": ["0.1", "0.3", "0.5", "0.6"],
        "correct_answer": "0.3",
        "difficulty": 0.6,
        "topic": "Probability",
        "tags": ["independence"]
    },
    {
        "question": "The word 'laconic' most nearly means:",
        "options": ["Talkative", "Using few words", "Verbose", "Expressive"],
        "correct_answer": "Using few words",
        "difficulty": 0.6,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'mendacious' most nearly means:",
        "options": ["Truthful", "Dishonest", "Brave", "Careless"],
        "correct_answer": "Dishonest",
        "difficulty": 0.7,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'nefarious' most nearly means:",
        "options": ["Evil", "Good", "Kind", "Honorable"],
        "correct_answer": "Evil",
        "difficulty": 0.7,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'obdurate' most nearly means:",
        "options": ["Stubborn", "Flexible", "Soft", "Kind"],
        "correct_answer": "Stubborn",
        "difficulty": 0.7,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'paragon' most nearly means:",
        "options": ["Model of excellence", "Flaw", "Error", "Weakness"],
        "correct_answer": "Model of excellence",
        "difficulty": 0.6,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'quixotic' most nearly means:",
        "options": ["Practical", "Idealistic but impractical", "Realistic", "Ordinary"],
        "correct_answer": "Idealistic but impractical",
        "difficulty": 0.8,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'recalcitrant' most nearly means:",
        "options": ["Obedient", "Resistant to authority", "Flexible", "Agreeable"],
        "correct_answer": "Resistant to authority",
        "difficulty": 0.8,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'sagacious' most nearly means:",
        "options": ["Wise", "Foolish", "Ignorant", "Naive"],
        "correct_answer": "Wise",
        "difficulty": 0.6,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'taciturn' most nearly means:",
        "options": ["Talkative", "Reserved", "Loud", "Aggressive"],
        "correct_answer": "Reserved",
        "difficulty": 0.5,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'ubiquitous' most nearly means:",
        "options": ["Rare", "Everywhere", "Uncommon", "Hidden"],
        "correct_answer": "Everywhere",
        "difficulty": 0.5,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'venerable' most nearly means:",
        "options": ["Respected", "Disrespectful", "Unimportant", "Common"],
        "correct_answer": "Respected",
        "difficulty": 0.6,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'wanton' most nearly means:",
        "options": ["Deliberate and unprovoked", "Necessary", "Justified", "Controlled"],
        "correct_answer": "Deliberate and unprovoked",
        "difficulty": 0.7,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'zealous' most nearly means:",
        "options": ["Enthusiastic", "Apathetic", "Lazy", "Indifferent"],
        "correct_answer": "Enthusiastic",
        "difficulty": 0.5,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'abstruse' most nearly means:",
        "options": ["Obvious", "Difficult to understand", "Clear", "Simple"],
        "correct_answer": "Difficult to understand",
        "difficulty": 0.8,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    },
    {
        "question": "The word 'bombastic' most nearly means:",
        "options": ["Simple", "Pretentious", "Clear", "Subtle"],
        "correct_answer": "Pretentious",
        "difficulty": 0.8,
        "topic": "Vocabulary",
        "tags": ["meaning"]
    }
]

def seed_collections() -> None:
    try:
        connection = MongoDBConnection()
        db = connection.database

        questions_collection = db['Questions']
        questions_collection.insert_many(questions)
        print(f'Inserted {len(questions)} questions.')
        print(db.list_collection_names())
    except Exception as e:
        raise CustomException(e, sys)

if __name__ == '__main__':
    seed_collections()
