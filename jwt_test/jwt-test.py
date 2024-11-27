import jwt

SECRET_KEY = "vfzvzfewfingirnwagwrlgwrgwr"

ALGORITHM = "HS256"

USER_INFO = {
    "id": 1,
    "name": "KMK",
    "email": "kyun9151@naver.com"
}

acceess_token = jwt.encode(USER_INFO, SECRET_KEY, algorithm=ALGORITHM)
decoded_token = jwt.decode(acceess_token, SECRET_KEY, algorithms=[ALGORITHM])

print(decoded_token)