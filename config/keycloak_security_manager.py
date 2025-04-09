from flask_appbuilder.security.manager import AUTH_OID
from superset.security import SupersetSecurityManager
from flask_oidc import OpenIDConnect
from flask_appbuilder.security.views import AuthOIDView
from flask_login import login_user
from urllib.parse import quote
from flask_appbuilder.views import ModelView, SimpleFormView, expose
from flask import (
    redirect,
    request,
    g
)
import json
import os

class OIDCSecurityManager(SupersetSecurityManager):

    def __init__(self, appbuilder):
        super(OIDCSecurityManager, self).__init__(appbuilder)
        if self.auth_type == AUTH_OID:
            self.oid = OpenIDConnect(self.appbuilder.get_app)
        self.authoidview = AuthOIDCView

    def extract_roles(self, user_info):
        """Extract and map roles from Keycloak user info."""
        roles = set()
        keycloak_roles = user_info.get('roles', [])
        realm_access = user_info.get('realm_access', {})
        keycloak_realm_roles = realm_access.get('roles', [])
        resource_access = user_info.get('resource_access', {})
        client_roles = resource_access.get(os.environ.get('OAUTH_CLIENT_ID'), {}).get('roles', [])

        role_mapping = self.auth_roles_mapping
        mapped_roles = set()

        for keycloak_role in keycloak_roles + keycloak_realm_roles + client_roles:
            for superset_role, mapped_keycloak_roles in role_mapping.items():
                if keycloak_role in mapped_keycloak_roles:
                    mapped_roles.add(self.find_role(superset_role))
                    break

        if not mapped_roles:
            mapped_roles.add(self.find_role(self.auth_user_registration_role))

        return list(mapped_roles)

    def update_user_roles(self, user, new_roles):
        """Update the user's roles in Superset."""
        if not user:
            return
        current_roles = set(user.roles)
        updated = False
        for role in new_roles:
            if role not in current_roles:
                user.roles.append(role)
                updated = True
        for role in list(current_roles):
            if role not in new_roles and role.name != self.auth_user_registration_role:
                user.roles.remove(role)
                updated = True
        if updated:
            self.get_session.commit()

class AuthOIDCView(AuthOIDView):

    @expose('/login/', methods=['GET', 'POST'])
    def login(self, flag=True):
        sm = self.appbuilder.sm
        oidc = sm.oid

        @oidc.require_login
        def handle_login():
            try:
                email = oidc.user_getfield('email')
                if not email:
                    return redirect('/login')

                user = sm.find_user(email=email)
                user_info = oidc.user_getinfo(['preferred_username', 'given_name', 'family_name', 'email', 'roles', 'realm_access', 'resource_access'])

                if user is None:
                    roles = sm.extract_roles(user_info)
                    user = sm.add_user(
                        username=user_info.get('preferred_username', email),
                        first_name=user_info.get('given_name', ''),
                        last_name=user_info.get('family_name', ''),
                        email=email,
                        role=roles
                    )
                else:
                    updated_roles = sm.extract_roles(user_info)
                    sm.update_user_roles(user, updated_roles)

                if user and user.is_active:
                    login_user(user, remember=True)
                    g.user = user

                return redirect(self.appbuilder.get_url_for_index)
            except Exception:
                return redirect('/login')

        return handle_login()

    @expose('/logout/', methods=['GET', 'POST'])
    def logout(self):
        oidc = self.appbuilder.sm.oid
        oidc.logout()
        super(AuthOIDCView, self).logout()
        redirect_url = request.url_root.strip('/') + self.appbuilder.get_url_for_login
        return redirect(
            os.environ.get("KEYCLOAK_BASE_URL") + '/realms/' + os.environ.get("KEYCLOAK_REALM") + '/protocol/openid-connect/logout?redirect_uri=' + quote(redirect_url))