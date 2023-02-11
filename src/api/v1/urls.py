from .users import Login, Logout, RefreshToken, SignUp

API_URL = '/api/v1'
AUTH_URL = f'{API_URL}/auth'

urls = [
    (SignUp, f'{AUTH_URL}/signup'),
    (Login, f'{AUTH_URL}/login'),
    (RefreshToken, f'{AUTH_URL}/refresh'),
    (Logout, f'{AUTH_URL}/logout')
]
