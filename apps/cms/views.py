from datetime import datetime
from . import cms

@cms.route('/')
def index():
    return "Content Manager System"
