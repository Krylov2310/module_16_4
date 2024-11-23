from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Path, HTTPException
from typing import Annotated
from pydantic import BaseModel
from typing import List

app = FastAPI()
users = []

# запуск - python -m uvicorn module_16_4:app
info_ed = ('Домашнее задание по теме "Модели данных Pydantic".<br>'
           'Цель: научиться описывать и использовать Pydantic модель.<br>'
           'Задача "Модель пользователя":<br>'
           'Студент Крылов Эдуард Васильевич<br>'
           'Дата: 23.11.2024г.')


class User(BaseModel):
    id: int = None
    username: str
    age: int


# Вместо главной страници
# http://127.0.0.1:8000/
@app.get("/", response_class=HTMLResponse)
async def welcome():
    return info_ed


# Информация о пользователях
@app.get("/users")
async def get_users() -> List[User]:
    return users


# Добавляет пользователя в базу данных
@app.post("/user/{username}/{age}")
async def post_user(username: Annotated[str, Path(min_length=2, max_length=20,
                                                  description="Введите Ваше имя", example="Edison")],
                    age: Annotated[int, Path(ge=18, le=120, description="Введите ваш возраст", example="25")]) -> User:
    try:
        user_id = (users[-1].id + 1) if users else 1
        user = User(id=user_id, username=username, age=age)
        users.append(user)
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")


# Изменение данных пользователя
@app.put("/user/{user_id}/{username}/{age}")
async def put_user(user_id: int, username: Annotated[str, Path(min_length=2, max_length=20,
                                                               description="Введите Ваше имя", example="Edison")],
                   age: Annotated[int, Path(ge=18, le=120,
                                            description="Введите ваш возраст", example="25")]) -> User:
    try:
        for user in users:
            if user.id == user_id:
                user.username = username
                user.age = age
                return user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


# Удаление пользователя по id
@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> str:
    try:
        users.pop(user_id - 1)
        return f'Данные пользователя № {user_id} удалены.'
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')
