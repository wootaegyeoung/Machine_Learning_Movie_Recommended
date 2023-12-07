import content
import user
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post('/content')
async def content_post(request: Request):
    data = await request.json()  # 요청으로부터 JSON 데이터 받기
    movie_list = content.get_recommendations(data['data'])  # 입력으로 받은 영화 리스트
    return JSONResponse(content=movie_list)  # 입력 데이터를 그대로 JSON 형태로 반환

@app.get('/user/{user_id}')
async def user_get(user_id: int):
    movie_list = user.get_recommendations(user_id)
    return JSONResponse(content=movie_list)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)
