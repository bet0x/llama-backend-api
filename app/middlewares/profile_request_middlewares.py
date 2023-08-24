from app.middlewares.authentication_authorization_middlewares import verify_authentication_authorization


def profile_requests_middleware():
    print('profile_requests_middleware')
    verify_authentication_authorization()
