# scripts/auth.py
import streamlit as st
import streamlit_authenticator as stauth

def get_authenticator():
    """
    Creates and returns an Authenticator object configured from Streamlit secrets.
    """

    # Retrieve user credentials from secrets
    credentials = {
        "usernames": {
            # Instead of emails, we’re using pure 'username' keys.
            "Harry": {
                "name": "Harry",
                "password": st.secrets["auth"]["users"]["Harry"]["password"]  # hashed password
            },
            "Ian": {
                "name": "Ian",
                "password": st.secrets["auth"]["users"]["Ian"]["password"] 
            },
            "Archie": {
                "name": "Archie",
                "password": st.secrets["auth"]["users"]["Archie"]["password"] 
            },
            "Guest": {
                "name": "Guest",
                "password": st.secrets["auth"]["users"]["Guest"]["password"] 
            }
        }
    }

    cookie_settings = {
        "name": st.secrets["auth"]["cookie"]["name"],
        "key": st.secrets["auth"]["cookie"]["key"],
        "expiry_days": st.secrets["auth"]["cookie"]["expiry_days"]
    }

    authenticator = stauth.Authenticate(
        credentials=credentials,
        cookie_name=cookie_settings["name"],
        key=cookie_settings["key"],
        cookie_expiry_days=cookie_settings["expiry_days"]
    )
    
    return authenticator