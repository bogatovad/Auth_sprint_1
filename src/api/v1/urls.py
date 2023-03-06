from .users import (ChangePersonalData, History, Login, Logout, RefreshToken,
                    SignUp, SocialServiceRedirect, SocialService)

API_URL = "/api/v1"
AUTH_URL = f"{API_URL}/auth"


def path(resource: str) -> str:
    return f"{AUTH_URL}/{resource}"


urls = [
    (SignUp, path("signup")),
    (Login, path("login")),
    (RefreshToken, path("refresh")),
    (Logout, path("logout")),
    (History, path("history_auth")),
    (ChangePersonalData, path("change")),
    (SocialServiceRedirect, path("login/vk")),
    (SocialService, path("vk_logic"))
]
