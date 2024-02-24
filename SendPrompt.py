from CaesarSQLDB.caesarcrud import CaesarCRUD
from AnthropicAPI.Anthropic import AnthropicAPI
from CaesarAICronEmail.CaesarAIEmail import CaesarAIEmail
class SendPrompt:
    @staticmethod
    def send(caesarcrud : CaesarCRUD,anthapi:AnthropicAPI,username,question_set_title):
        user_exists = caesarcrud.check_exists(("*"),"hackathon",f"username = '{username}'")
        if not user_exists:
                return {"error":"user has not done any tasks"}
        else:
            result_info = caesarcrud.get_data(("username","question_set_title","question","useranswered","answer","numofattempts","hintsused"),"hackathon",f"username = '{username}' AND question_set_title = '{question_set_title}'")
            final_message = ""
            for question_set in result_info:
                message = f"""
                        using {username} as the students name.
                        Question Set Title: {question_set['question_set_title']}
                        Question: {question_set['question']}
                        User Answered: {question_set['useranswered']}
                        Real Answer: {question_set['answer']}
                        Number of Attempts and it was wrong: {question_set['numofattempts']}

                        
                        Hints Used: {str(question_set['hintsused'])}
                        
                        """
                final_message += message + "\n"
            # TODO Prompt Engineering here.
                # 
            prompt = f"Using this as context: {final_message}\n Generate a profile on how the teacher can improve in guiding the student. Using these answer with these results in a test. Provide an analysis on the student for each question."
            #print(prompt)
            result = anthapi.create_message(prompt)
            return result