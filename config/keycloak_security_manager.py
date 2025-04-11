from flask_appbuilder.security.manager import AUTH_OID
from superset.security import SupersetSecurityManager
from flask_oidc import OpenIDConnect
from flask_appbuilder.security.views import AuthOIDView
from flask_login import login_user, logout_user
from urllib.parse import quote
from flask_appbuilder.views import expose
from flask import (
    redirect,
    request,
    g,
    session
)
import os

class OIDCSecurityManager(SupersetSecurityManager):

    def __init__(self, appbuilder):
        super(OIDCSecurityManager, self).__init__(appbuilder)
        if self.auth_type == AUTH_OID:
            self.oid = OpenIDConnect(self.appbuilder.get_app)
        self.authoidview = AuthOIDCView

    def is_authenticated(self):
        if not super().is_authenticated():
            return False
            
        if hasattr(self, 'oid'):
            try:
                self.oid.user_getfield('email')
                return True
            except Exception:
                self.invalidate_session(g.user.id if hasattr(g, 'user') and g.user else None)
                return False
        return True

    def invalidate_session(self, user_id):
        try:
            session.clear()
            logout_user()
            
            if hasattr(self, 'oid'):
                self.oid.logout()
                
            if hasattr(self.appbuilder.app, 'cache'):
                cache_key = f"user_session_{user_id}"
                self.appbuilder.app.cache.delete(cache_key)
                
            return True
        except Exception:
            return False

    def extract_roles(self, user_info):
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
            default_role = self.find_role(self.auth_user_registration_role)
            mapped_roles.add(default_role)

        return list(mapped_roles)

    def update_user_roles(self, user, new_roles):
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
                if not oidc.user_getfield('email'):
                    return redirect('/login')

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
                    sm.invalidate_session(user.id)
                    login_user(user, remember=False)
                    g.user = user
                    return redirect(self.appbuilder.get_url_for_index)
                elif user and not user.is_active:
                    return redirect('/login')
                else:
                    return redirect('/login')
            except Exception:
                return redirect('/login')

        return handle_login()

    @expose('/logout/', methods=['GET', 'POST'])
    def logout(self):
        try:
            user_id = g.user.id if hasattr(g, 'user') and g.user else None
            oidc = self.appbuilder.sm.oid
            
            if user_id:
                self.appbuilder.sm.invalidate_session(user_id)
            
            redirect_uri = request.host_url.rstrip('/') + '/login/'
            keycloak_logout_url = (
                oidc.client_secrets.get('issuer') + 
                '/protocol/openid-connect/logout' +
                '?redirect_uri=' + quote(redirect_uri)
            )
            
            response = redirect(keycloak_logout_url)
            
            for key in request.cookies:
                response.delete_cookie(key)
                
            response.delete_cookie('oidc_id_token')
            response.delete_cookie('oidc_access_token')
            response.delete_cookie('oidc_refresh_token')
            
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            
            return response
        except Exception:
            return redirect('/login/')