import math

def update_score_irt(is_correct: bool, ability_score: float, difficulty: float) -> float:
    """
    This function takes the correct flag, ability_score of the student and difficulty of the question 
    and implements a simplified 1D Item Response Theory (IRT) model.
    """
    prob_correct = 1 / (1 + math.exp(-(ability_score - difficulty))) # this will give a probality between 0-1
    learning_rate = 0.3 # step size for adjusting the ability score
    if is_correct:
        # increase the ability_score
        ability_score += learning_rate * (1 - prob_correct)
    else:
        # decrease the ability score
        ability_score -= learning_rate * prob_correct
    # clamping the score between 0 and 1
    return max(0.0, min(1.0, ability_score))