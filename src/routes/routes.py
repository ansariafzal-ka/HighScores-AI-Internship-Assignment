from fastapi import APIRouter
from src.configurations.mongodb_connection import db
from src.models.session_model import UserSession
from src.utils.exception import CustomException
from src.utils.irt import update_score_irt
import sys
import os
from bson import ObjectId
from openai import OpenAI

router = APIRouter()

@router.post('/start-test')
def start_test() -> dict:
    try:
        # get the UserSession model
        session = UserSession()
        # make it into a dictionary
        session_dict = session.model_dump()

        # insert the UserSession in the database
        result = db['UserSession'].insert_one(session_dict)
        # make the id into a string
        session_id = result.inserted_id

        # get a question with the difficulty in range 0.45 - 0.55
        question = db['Questions'].find_one({
            'difficulty': {
                '$gte': 0.45,
                '$lte': 0.55
            }
        })

        # checks for None response
        if question is None:
            return {'message': 'No starting question found.'}

        # preventing repeating questions
        db['UserSession'].update_one(
            {'_id': session_id},
            {
                '$push': {
                    'asked_questions': str(question['_id'])
                }
            }
        )

        # make the id into a string
        question['_id'] = str(question['_id'])

        # return the session_id and question
        return {
            'session_id': str(session_id),
            'question': question
        }

    except Exception as e:
        raise CustomException(e, sys)
    
@router.post('/submit-answer')
def submit_answer(data: dict) -> dict:
    try:
        # get the data from the client
        session_id = data['session_id']
        question_id = data['question_id']
        selected_answer = data['selected_answer']

        # convert the ids
        question_id = ObjectId(question_id)
        session_id = ObjectId(session_id)

        # get the question for checking if correct
        question = db['Questions'].find_one({
            '_id': question_id
        })
        
        # checks for None response
        if question is None:
            return {'message': 'Question not found.'}
        
        # check if answer is correct
        is_correct = selected_answer == question['correct_answer']

        # find the session
        session = db['UserSession'].find_one({
            '_id': session_id
        })

        # checks for None response
        if session is None:
            return {'message': 'Session not found.'}
        
        # get the ability_score, num_questions and difficulty
        ability_score = session['ability_score']
        num_questions = session['num_questions']
        difficulty = question['difficulty']

        # update the score based on the answer
        updated_ability_score = update_score_irt(is_correct, ability_score, difficulty)
        # increment the number of questions
        num_questions += 1

        # update the user session
        db['UserSession'].update_one(
            {'_id': session_id},
            {
                '$set': {
                    'ability_score': updated_ability_score,
                    'num_questions': num_questions
                },
                # storing the user response for LLM study plan
                '$push': {
                    'responses': {
                    'question_id': str(question_id),
                    'topic': question['topic'],
                    'correct': is_correct,
                    'difficulty': difficulty
                    }
                }
            }
        )

        # return the correct flag, updated score and number of questions
        return {
            'correct': is_correct,
            'ability_score': updated_ability_score,
            'num_questions': num_questions
        }

    except Exception as e:
        raise CustomException(e)
    
@router.get('/next-question/{session_id}')
def next_question(session_id: str) -> dict:
    try:
        # convert the is
        session_id = ObjectId(session_id)

        # find the session
        session = db['UserSession'].find_one({
            '_id': session_id
        })

        # checks for None response
        if session is None:
            return {'message': 'Session not found.'}
        
        # get the number of questions done by the user
        num_questions = session['num_questions']

        # stop the test after 10 questions
        if num_questions >= 10:
            return {
                'message': 'Test completed.',
                'final ability score': session['ability_score']
            }
        # get the current ability score
        ability_score = session['ability_score']
        # filter asked questions
        asked_questions = [ObjectId(q) for q in session.get('asked_questions', [])]

        # get a question with the difficulty in range of current ability score
        question = db['Questions'].find_one({
            '_id': {'$nin': asked_questions},
            'difficulty': {
                '$gte': ability_score - 0.1,
                '$lte': ability_score + 0.1
            }
        })

        # If no match, find any unanswered question
        if question is None:
            question = db['Questions'].find_one({
                '_id': {'$nin': asked_questions}
        })
            
        # checks for None response
        if question is None:
            return {'message': 'Question not found.'}

        # store asked question
        db['UserSession'].update_one(
            {'_id': session_id},
            {
                '$push': {
                    'asked_questions': str(question['_id'])
                }
            }
        )
        
        # convert id to string
        question['_id'] = str(question['_id'])

        # return the question
        return {
            'question': question
        }
    except Exception as e:
        raise CustomException(e, sys)

@router.post('/end-session')
def end_session(data: dict):
    try:
        session_id = ObjectId(data['session_id'])
        # find the session
        session = db['UserSession'].find_one({
            '_id': session_id
        })

        # checks for None response
        if session is None:
            return {'message': 'Session not found'}
        
        responses = session.get('responses', [])
        final_ability = session['ability_score']
        incorrect_topics = [r['topic'] for r in responses if not r['correct']]

        topics_summary = ', '.join(set(incorrect_topics)) if incorrect_topics else 'No major weaknesses'

        # prompt for LLM
        prompt = f"""
            A student completed an adaptive GRE test with the following results:
            - Final ability score: {final_ability:.2f} (scale 0-1)
            - Topics missed: {topics_summary}
            - Total questions answered: {len(responses)}

            Generate a personalized 3-step study plan to help them improve. Be specific and actionable.
        """

        # calling the OpenAI API
        OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')
        client = OpenAI(api_key=OPEN_AI_API_KEY)
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=500
        )

        # get the study plan from the LLM
        study_plan = response.choices[0].message.content

        return {
            'final_ability': final_ability,
            'topics_missed': list(set(incorrect_topics)),
            'study_plan': study_plan
        }
    except Exception as e:
        raise CustomException(e, sys)