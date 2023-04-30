from flask_login import logout_user, login_user, current_user

from bookshelf import get_model, User
from flask import Blueprint, redirect, render_template, request, url_for

auth = Blueprint('login', __name__)


@auth.route('/')
def root():
    return redirect('auth/login')


@auth.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        print("authenticated")
        print(current_user.id)
        return render_template('/login.html', user={})
    else:
        print("not authenticated")
        print(current_user)
        return render_template('/login.html', user={})


@auth.route('/signUp', methods=['POST'])
def sign_up():
    user_email = request.form.get('email')
    # print(user_email)
    user_pw = request.form.get('password')
    # print(user_pw)
    user = get_model().create_user(user_email, user_pw)
    return redirect('/auth/login')


@auth.route('signIn', methods=['POST'])
def sign_in():
    user_email = request.form.get('email')
    user_pw = request.form.get('password')

    if user_email is None or user_pw is None:
        return redirect('/auth/relogin')

    # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
    user_info = get_model().getUserInfo(user_email, user_pw)
    # print(user_info)
    if user_info['id']:
        # 사용자 객체 생성
        login_info = User(user_email, user_pw)
        login_info.id = user_info['id']
        # 사용자 객체를 session에 저장
        login_user(login_info)
        return redirect('/')
    else:
        return redirect('auth/relogin')


#
# 로그인 실행
# 로그인 계정 정보는 post로 받아오지만
# 일반 리소스들은 get으로 받아오므로 get과 post모두 선언해줘야 한다.
# @auth.route('/login/get_info', methods=['GET', 'POST'])
# def login_get_info():
#     user_id = request.form.get('userID')
#     user_pw = request.form.get('userPW')
#
#     if user_id is None or user_pw is None:
#         return redirect('/relogin')
#
#     # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
#     user_info = User.get_user_info(user_id, user_pw)
#
#     if user_info['result'] != 'fail' and user_info['count'] != 0:
#         # 사용자 객체 생성
#         login_info = User(user_id=user_info['data'][0]['USER_ID'])
#         # 사용자 객체를 session에 저장
#         login_user(login_info)
#         return redirect('/')
#     else:
#         return redirect('/auth/relogin')


#
#
# 로그인 실패 시 재로그인
@auth.route('/relogin')
def relogin():
    login_result_text = "로그인에 실패했습니다. 다시 시도해주세요."

    return render_template('/login.html', login_result_text=login_result_text)

#
# 로그아웃
@auth.route('/logout')
def logout():
    # session 정보를 삭제한다.
    logout_user()
    return redirect('/')

