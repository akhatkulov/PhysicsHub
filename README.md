--[#]-- LINUX RUN --[#]--

export FLASK_APP=flasky.py
export FLASK_DEBUG=1

flask db upgrade

flask run


--[?]-- Windows run command --[?]--
set FLASK_APP=flasky.py

set FLASK_DEBUG=1

flask db upgrade

flask run
