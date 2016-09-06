import os
import logging

from eve import Eve
from eve_app.eve_oauth2 import create_server, EveOAuth2

package_directory = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger('todo/eve_app')

eapp = Eve(auth=EveOAuth2, settings='eve_app/settings.py', template_folder=os.path.join(package_directory, 'templates'))
eapp.config.update({
    'OAUTH2_PROVIDER_TOKEN_EXPIRES_IN': 20,
    'OAUTH2_PROVIDER_REFRESH_TOKEN_GENERATOR': None,
    'OAUTH2_PROVIDER_TOKEN_GENERATOR': None,
})
create_server(eapp)
