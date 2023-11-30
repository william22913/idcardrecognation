from i18n import I18N
from config import AppConfig
from flask import Flask
from service.http import *
i18n = I18N()
appConfig = AppConfig()
app = Flask(__name__)


@app.route('/id-card/reader', methods=['POST'])
def id_card_without_selfie():
    return handle_request_without_selfie()


@app.route('/id-card/selfie/reader', methods=['POST'])
def id_card_with_selfie():
    return handle_request_with_selfie()


if __name__ == '__main__':
    app.run(debug=False, host=appConfig.server_host, port=appConfig.server_port)


