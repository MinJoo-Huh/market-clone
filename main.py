from fastapi import FastAPI, UploadFile, Form, Response
from fastapi.responses import JSONResponse      #json 파일 보내기
from fastapi.encoders import jsonable_encoder   #json code로 변경하기
from fastapi.staticfiles import StaticFiles
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

@app.get('/items')
async def get_items():
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
                insertAt:Annotated[int, Form()]
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

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


