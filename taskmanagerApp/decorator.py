# デコレーター
from django.shortcuts import redirect


# loginチェッカー
def login_check(func):
    def checker(request, *args, **kwargs):
        # sessionのuser_idがあるかどうか
        if not request.session.get('user_id'):
            return redirect('login')
        # loginされているときに呼び出したい関数
        return func(request, *args, **kwargs)
    return checker
