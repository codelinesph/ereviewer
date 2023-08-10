

def checkAnswers(answers, corrected):
    overall_points = 0

    answer_index = 0
    # loop my answers
    for answer in answers:

        # validate if it has id
        if ('id' in answer.keys()): 
            correct_index = 0
            # loop corrected answers
            for correct in corrected:

                # check if there is a match
                if(answer.get('id') == correct.get('id')):

                    # reset point counter and indexes
                    answer_points = 0
                    answer_choice_index = 0

                    # loop my choices from my own data
                    for answer_choice in answer.get('choices'):

                        # then loop corrected
                        position = 0
                        for correct_choice in correct.get('choices'):
                            # check if everything is correct and mark it if it is
                            if answer_choice.get('id') == correct_choice.get('id'):
                              
                                if (
                                    correct_choice.get('is_correct_answer') == False and 
                                    answer_choice.get('my_answer')
                                ):
                                    answers[answer_index]['choices'][position]['correct'] = False
                                elif (
                                    correct_choice.get('is_correct_answer') == True and 
                                    answer_choice.get('my_answer') == True
                                ):
                                    answers[answer_index]['choices'][position]['correct'] = True
                                    answer_points += 1
                            pass
                            position += 1
                        pass   


                    # gained points is points divided by expected answers
                    answer_points = 0
                    if correct.get('expected_answers') > 0:
                        answer_points/correct.get('expected_answers')
                    # then add it to overalls
                    overall_points += answer_points
                    answers[answer_index]['points'] = answer_points
                    # increment indexes
                    answer_choice_index += 1

                    
                    pass
                pass
                correct_index += 1
            pass
        pass
        answer_index += 1
    pass

    return {
        'points_earned':overall_points,
        'data':answers
    }
