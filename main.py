from fastapi import FastAPI, UploadFile, Form, Response, Depends
from fastapi.responses import JSONResponse      #json 파일 보내기
from fastapi.encoders import jsonable_encoder   #json code로 변경하기
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException    # 유효하지 않는 에러 처리
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()      # db - cursor = insert, select할 때 사용...?

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
	            id INTEGER PRIMARY KEY,
	            title TEXT NOT NULL,
	            image BLOB,
	            price INTEGER NOT NULL,
	            description TEXT,
	            place TEXT NOT NULL,
	            insertAt INTEGER NOT NULL
            );
            """)    # IF NOT EXISTS : 테이블이 없을 때만 생성한다.

app = FastAPI()

SECRET = "super-coding"
manager = LoginManager(SECRET, '/login')    # 적당한 토큰을 만들어주는 라이브러리

@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data['id']}"'''
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * FROM users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

@app.post('/login')
def login(id:Annotated[str, Form()], 
           password:Annotated[str, Form()]):
    user = query_user(id)
    if not user:
        raise InvalidCredentialsException   # 유효하지 않는 에러 처리리
    elif password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(data={
        'sub': {
            'id':user['id'],
            'name':user['name'],
            'email':user['email']
        }
    })
    
    return {'access_token': access_token}
    

@app.post('/signup')
def signup(id:Annotated[str, Form()], 
           password:Annotated[str, Form()],
           name:Annotated[str, Form()],
           email:Annotated[str, Form()]           
           ):
    cur.execute(f"""
                INSERT INTO users(id, name, email, password)
                VALUES ('{id}', '{name}', '{email}','{password}')
                """)
    con.commit()
    return '200'



@app.get('/items')
async def get_items(user=Depends(manager)): # 토큰 manager
    con.row_factory = sqlite3.Row   #column명도 같이 가져옴.
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * FROM items;
                       """).fetchall() 
    
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))

@app.post('/items')
async def create_item(image:UploadFile,               #FastAPI 변수 지정방법
                title:Annotated[str, Form()], 
                price:Annotated[int, Form()], 
                description:Annotated[str, Form()], 
                place:Annotated[str, Form()],
                insertAt:Annotated[int, Form()],
                user=Depends(manager)
                ):
            
    #print(image, title, price, description, place)
    
    image_bytes = await image.read()    # 이미지를 가져올 시간
    cur.execute(f"""
                INSERT INTO 
                items(title, image, price, description, place, insertAt)
                VALUES ('{title}', '{image_bytes.hex()}', {price}, '{description}', '{place}', {insertAt})   
                """)    # 쌍따옴표 6개 : ``이랑 같은 원리       # hex - 16진법 : 데이터 길이를 줄이기 위해서
                        # items 안에 values 값을 넣을 것이다.
    con.commit()
    return '200'

# 이미지 가져오기
@app.get('/images/{item_id}')
async def get_image(item_id):
        cur = con.cursor()
        # hex로 넘겼으니 hes로 올거임.
        image_bytes = cur.execute(f"""
                                    SELECT image FROM items WHERE id={item_id}
                                  """).fetchone()[0]  #특정 아이디에 맞는 이미지만 가져오고 싶다. tuple?
        return Response(content=bytes.fromhex(image_bytes), media_type='image/*') #hex로 된 것을 bytes로 바꿔주겠다.



# 기존 회원 확인 코드 넣기 - "id가 존재합니다"
# @app.get('/signup/{user_id_email}')
# async def get_sign_id(user_id_email):
#     con.row_factory = sqlite3.Row   #column명도 같이 가져옴.
#     cur = con.cursor()
#     select_id = cur.execute(f"""
#                        SELECT id FROM users WHERE id = {user_id_email[0]};
#                        """)
#     select_email = cur.execute(f"""
#                        SELECT email FROM users WHERE id = {user_id_email[1]};
#                        """)
    
#     print("select id : " + select_id)
#     print("select email : " + select_email)
    
#     # 없을 경우 예외 처리
    
#     return "id, email 정보를 받았습니다."



app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


