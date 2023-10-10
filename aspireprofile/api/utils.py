from _aspirebase.api.utils import BaseApiUtils
from aspireprofile.api.data_utils import ProfileDataUtils


class ProfileViewUtils:

    data_utils = ProfileDataUtils()

    def username_login(self, request):
        login_data = request.data
        user_agent = request.user_agent
        u_name = login_data.get('username')
        password = login_data.get('password')
        client_app = login_data.get('client_app', "pos")
        if not (u_name and password):
            return {"error": "Please send valid username/password"}, 400
        profile = self.data_utils.get_profile(u_name)
        if not profile:
            return {"error": "Unregistered user"}, 400
        if not profile.user.check_password(password):
            return {"error": "Invalid username/password"}, 400
        token = self.data_utils.token_flow(
            profile.user, user_agent=user_agent,
            app_name=client_app,
            ip_address=BaseApiUtils.get_client_ip(request))
        if not token:
            return {"error": "Maximum devices exceeded"}, 400
        return self.data_utils.map_to_data_dict(
            token, profile), 200

    @staticmethod
    def logout(request):
        request.auth.delete()
        return {"message": "Logged out successfully"}, 200