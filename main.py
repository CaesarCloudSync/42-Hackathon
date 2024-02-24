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
from SendPrompt import SendPrompt
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

@app.post('/storequestion')# GET # allow all origins all methods.
async def storequestion(data: JSONStructure = None):
        try:
            data = dict(data)
            username = data["username"]

            question_set_title = data["question_set_title"]
            question = data["question"]
            useranswered = data["useranswered"]
            answer = data["answer"]
            numofattempts =data["numofattempts"]
            hintsused = data["hintsused"]
            question_exists = caesarcrud.check_exists(("*"),"hackathon",f"username = '{username}' AND question_set_title = '{question_set_title}' AND question = '{question}'")
            if question_exists:
                 return {"error":"question already answered"}
            else:
                 res = caesarcrud.post_data(("username","question_set_title","question","useranswered","answer","numofattempts","hintsused"),(username,question_set_title,question,useranswered,answer,int(numofattempts),hintsused),"hackathon")
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
async def create_profile_for_parent(email:str,username:str):
        try:
            result = caesarcrud.get_data(("username","question_set_title"),"hackathon",f"username = '{username}'")
            if result:
                for user in result:
                    question_set_title = user["question_set_title"]
                    check_exists = caesarcrud.check_exists(("*"),"hackathonprompts",f"username = '{username}' AND question_set_title = '{question_set_title}'")
                    if not check_exists:
                        res = SendPrompt.send(caesarcrud,anthapi,username,question_set_title)
                    else:
                         caesarcrud.get_data
                    CaesarAIEmail.send(**{"email":email,"subject":f"{username} | {question_set_title} Report","message":res})
                return {"username":username,"question set":question_set_title,"message":res}
            else:
                return {"error":"doesn't exist."}
    

        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.get('/create_profile_for_teacher')# GET # allow all origins all methods.
async def create_profile_for_teacher():
        # Create 
        try:    
            print("start")
            users_exist = caesarcrud.check_exists(("*"),"hackathon")
            if users_exist:
                users= caesarcrud.get_data(("username","question_set_title"),"hackathon")
                user_done = []
                user_result = []
                for user in users:
                    username = user["username"]
                    question_set_title = user["question_set_title"]
                    if username not in user_done:
                        print(username,question_set_title)
                        check_exists = caesarcrud.check_exists(("*"),"hackathonprompts",f"username = '{username}' AND question_set_title = '{question_set_title}'")
                        if not check_exists:
                            res = SendPrompt.send(caesarcrud,anthapi,username,question_set_title)
                            res = res.replace("\n","<br>")
                            caesarcrud.post_data(("username","question_set_title","prompt"),(username,question_set_title,res),"hackathonprompts")
                        user_result.append({"username":username,"message":res})
                        #CaesarAIEmail.send(**{"email":"amari.lawal@gmail.com","subject":"Profile Generated","message":"Profile Generated."})
                    user_done.append(username)

                return {"result":user_result}
  
  
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.get('/get_profile_for_teacher')# GET # allow all origins all methods.
async def get_profile_for_teacher():
        # Create 
        try:    
            print("start")
            users_exist = caesarcrud.check_exists(("*"),"hackathon")
            if users_exist:
                users= caesarcrud.get_data(("username","question_set_title","prompt"),"hackathonprompts")
                user_result = []
                for user in users:
                    username = user["username"]
                    question_set_title = user["question_set_title"]
                    prompt = user["prompt"]

                    user_result.append({"username":username,"question_set_title":question_set_title,"message":prompt})


                return {"result":user_result}
  
  
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
    #asyncio.run(main())clear