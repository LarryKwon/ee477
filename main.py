# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import redirect

import bookshelf
import config
from bookshelf import User

app = bookshelf.create_app(config)


# @app.login_manager.user_loader
# def user_loader(user_id):
#     # 사용자 정보 조회
#     user_info = User.get_user_info(user_id)
#     # user_loader함수 반환값은 사용자 '객체'여야 한다.
#     # 결과값이 dict이므로 객체를 새로 생성한다.
#     login_info = User(user_id=user_info['data'][0]['USER_ID'])
#
#     return login_info
#
#
# @app.login_manager.unauthorized_handler
# def unauthorized():
#     # 로그인되어 있지 않은 사용자일 경우 첫화면으로 이동
#     return redirect("/")

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
