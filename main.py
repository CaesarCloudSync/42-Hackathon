import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from AnthropicAPI.Anthropic import AnthropicAPI
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables
from CaesarSQLDB.caesarcrud import CaesarCRUD
import uuid
from CaesarAICronEmail.CaesarAIEmail import CaesarAIEmail

caesar_create_table = CaesarCreateTables()
caesarcrud = CaesarCRUD()
caesar_create_table.create(caesarcrud)

anthapi = AnthropicAPI()

load_dotenv(".env")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 1. Store question and answer $
# 2. Update hintsused increment on frontend, then posted to db //
# 3. Count the number of questions correct or inccorrect. $
# 3. Create profile for teacher from the whole set of questions. $
# 4. collect structured data of like amount right, and amount wrong then make report/summary.



JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAI Template. Hello"

@app.get('/storequestion')# GET # allow all origins all methods.
async def storequestion(username:str,question_set_title:str,question:str,useranswered:str,answer:str,result:str,hintsused:str):
        try:

            question_exists = caesarcrud.check_exists(("*"),"hackathon",f"username = '{username}' AND question_set_title = '{question_set_title}' AND question = '{question}'")
            if question_exists:
                 return {"error":"question already answered"}
            else:
                 res = caesarcrud.post_data(("username","question_set_title","question","useranswered","answer","result","hintsused"),(username,question_set_title,question,useranswered,answer,result,hintsused),"hackathon")
            return {"message":"answer was stored."} 
  
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.get('/count_result')# GET # allow all origins all methods.
async def count_result(username:str,question_set_title:str):
        try:

            user_exists = caesarcrud.check_exists(("*"),"hackathon",f"username = '{username}'")
            if not user_exists:
                 return {"error":"question has not answered a question yet."}
            else:
                correctres = caesarcrud.get_data(("username","result"),"hackathon",f"question_set_title = '{question_set_title}' AND username = '{username}' AND result = 'correct'")
                if correctres:
                    correctrescount = len(correctres)
                else:
                    correctrescount = 0
                
                incorrectres = caesarcrud.get_data(("username","result"),"hackathon",f"question_set_title = '{question_set_title}' AND username = '{username}' AND result = 'incorrect'")
                if incorrectres:
                 incorrectrescount = len(incorrectres)
                else:
                 incorrectrescount = 0
                 
                 
                return {"correct":correctrescount,"incorrect":incorrectrescount}

  
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.get('/create_profile_for_parent')# GET # allow all origins all methods.
async def create_profile_for_parent(username:str,question_set_title:str):
        try:
            user_exists = caesarcrud.check_exists(("*"),"hackathon",f"username = '{username}'")
            if not user_exists:
                 return {"error":"user has not done any tasks"}
            else:
                result_info = caesarcrud.get_data(("username","question_set_title","question","useranswered","answer","result","hintsused"),"hackathon",f"username = '{username}' AND question_set_title = '{question_set_title}'")
                final_message = ""
                for question_set in result_info:
                    message = f"""
                            using {username} as the students name.
                            Question Set Title: {question_set['question_set_title']}
                            Question: {question_set['question']}
                            User Answered: {question_set['useranswered']}
                            Real Answer: {question_set['answer']}
                            Question Result: {question_set['result']}
                            Hints Used: {str(question_set['hintsused'])}
                            
                            """
                    final_message += message + "\n"
                prompt = f"Using this as context: {final_message}\n Generate a teachers report for a student with these results in a test. Provide an analysis on the student for each question"
                result = anthapi.create_message(prompt)

                CaesarAIEmail.send(**{"email":"amari.lawal@gmail.com","message":result,"subject":f"{username} Question Set Results: {question_set_title}"})
                return {"message":result}
  
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.get('/create_profile_for_teacher')# GET # allow all origins all methods.
async def create_profile_for_teacher(username:str,question_set_title:str):
        # Create 
        try:
            user_exists = caesarcrud.check_exists(("*"),"hackathon",f"username = '{username}'")
            if not user_exists:
                 return {"error":"user has not done any tasks"}
            else:
                result_info = caesarcrud.get_data(("username","question_set_title","question","useranswered","answer","result","hintsused"),"hackathon",f"username = '{username}' AND question_set_title = '{question_set_title}'")
                final_message = ""
                for question_set in result_info:
                    message = f"""
                            using {username} as the students name.
                            Question Set Title: {question_set['question_set_title']}
                            Question: {question_set['question']}
                            User Answered: {question_set['useranswered']}
                            Real Answer: {question_set['answer']}
                            Question Result: {question_set['result']}
                            Hints Used: {str(question_set['hintsused'])}
                            
                            """
                    final_message += message + "\n"
                # TODO Prompt Engineering here.
                prompt = f"Using this as context: {final_message}\n Generate a teachers report for a student with these results in a test. Provide an analysis on the student for each question"
                print(prompt)
                result = anthapi.create_message(prompt)

                CaesarAIEmail.send(**{"email":"amari.lawal@gmail.com","message":result,"subject":f"{username} Question Set Results: {question_set_title}"})
                return {"message":result}
  
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}


@app.get('/sendmessage')# GET # allow all origins all methods.
async def sendmessage(message:str):
        try:
            result = anthapi.create_message(message)
            return {"message":result} 
  
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}



if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())