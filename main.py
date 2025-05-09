from fastapi import (FastAPI, Query, BackgroundTasks, File, Form, UploadFile
                     ) 
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import Optional, Dict, Annotated
import json
from pprint import pprint
from fastapi.concurrency import run_in_threadpool
import asyncio
app = FastAPI()


class ManagerSocket:

    def __init__(self):
        """
            definition de variable active_connection qui est un dictionnaire 
            qui a pour valeur un dictionnaire avec une representation de la values 

            {
                "socket': Obj,
                "user_id": str,
            }
        """
        self.active_conniction : Dict[str, Dict] = {}

    async def connection_socket(self,websocket : WebSocket, user_id : str):
        await websocket.accept()

        # pprint(websocket.scope)
        self.active_conniction[user_id] = {
            "websocket" : websocket,
            "user_id": user_id
        }


    async def send_message(self, msg: Dict):
        """
            la fonction send permet de declancher un message websocket

            msg : {
                "type: "descrit le type de message utiliser",
                "message": "le message de type text",
                "file": "doit etre le lient de ",
                "id_conversation"? : "peut etre null ",
                "sender": "",
                "recever":"
            }
        """
        # print("je suis la pour ", self.active_conniction.scope)
        print("je suis la ", msg)
        if msg and msg["recever"]:
            print("je web", self.active_conniction)
            try :
                print("je web", self.active_conniction[msg["recever"]]["websocket"])
                await self.active_conniction[msg["recever"]]["websocket"].send_json(json.dumps(msg))
            except KeyError:
                print("je suis erreur ")


    def disconnect(self, websocket:WebSocket):
         if self.active_conniction == websocket:
           self.active_conniction = None



async def back_tache(msg:Dict):
    await manager.send_message(msg=msg)


manager = ManagerSocket()

@app.get("/")
async def root():
    return HTMLResponse(open('index.html', 'r').read())


@app.get("/send")
async def send():
    msg = {"message":'Someone view test route bien jouer',
                             "user_id":"j8559566getgdj89p",
                            "type":"message", "recever":"j8559566getgdj89p"  }
    loop = asyncio.get_event_loop()
    loop.create_task(back_tache(msg))
    



@app.websocket("/ws/{user_id}/")
async def mysoc(websocket:WebSocket, user_id:str ):
    await manager.connection_socket(websocket, user_id)
    try:
        ## to keep websocket conniction work
        while True:
            data = await websocket.receive_json()
            print(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.post("/create-post")
def create_post(file: Annotated[UploadFile | None, File()] = None, 
                description: Annotated[str, Form()] = "je test"):
    print(description)
    print(file)

    return True


if __name__ == "__main__":
    app.run(debug=True)