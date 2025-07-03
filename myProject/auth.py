from pydantic import BaseModel

class Cur_user(BaseModel):
    user_id: int
    email: str
    role: str
    avatar_url: str

async def get_current_user():

    return Cur_user(
        user_id=1,
        email="emma.tech@example.com",
        role="用户",
        avatar_url="https://avatarhub.com/emma_profile.jpg",
    )