from flask import redirect, request, url_for, render_template, session
from requests_oauthlib import OAuth2Session
from flask.views import MethodView
from llm import myllm
from oauth_config import client_id, authorization_base_url, redirect_callback

class Query(MethodView):
    def get(self):
        # If client has an OAuth2 token, use it to get their information and render
        #   the signing page with it
        userinfo = { 'name': 'Wu', 'email':'wuchang@pdx.edu', 'picture':'https://lh3.googleusercontent.com/ogw/AKPQZvz_tj5zP8uDHrcMXyy2GX3fDu7YQ1MAdZWJOb-elw=s32-c-mo'}
        # if 'oauth_token' in session:
        if True:
            #google = OAuth2Session(client_id, token=session['oauth_token'])
            #userinfo = google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
            return render_template('query.html', name=userinfo['name'], email=userinfo['email'], picture=userinfo['picture'])
        else:
        # Redirect to the identity provider and ask the identity provider to return the client
        #   back to /callback route with the code
            google = OAuth2Session(client_id,
                    redirect_uri = redirect_callback,
                    scope = 'https://www.googleapis.com/auth/userinfo.email ' +                   
                            'https://www.googleapis.com/auth/userinfo.profile'
            )
            authorization_url, state = google.authorization_url(authorization_base_url, prompt='login')

            # Identity provider returns URL and random "state" that must be echoed later
            #   to prevent CSRF.
            session['oauth_state'] = state
            return redirect(authorization_url)

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        if True:
        #if 'oauth_token' in session:
            # Insert based on form fields only if an OAuth2 token is present to ensure
            #   values in all fields exist
            #myllm.query(request.form['message'])
            return render_template('query.html',question=request.form['message'],answer="Pretend that LLM gave you this")
        else:
            return redirect(url_for('query'))
