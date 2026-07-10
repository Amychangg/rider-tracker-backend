from fastapi import APIRouter

router = APIRouter(
    tags=["auth"], prefix="/auth"
)



@router.get('/')
def user_login_by_line():
    response_type = ''
    client_id = ''
    redirect_uri = ''
    state = ''
    scope = ''
    nonce = ''
    print(f'https://access.line.me/oauth2/v2.1/authorize?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope={scope}&nonce={nonce}')



# 接收flutter回傳的line auth code
@router.post('/line/login/')
def auth_line_login():
    pass