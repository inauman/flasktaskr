#below two lines are for importing a package from parent or sibling.
import sys
sys.path.insert(0, '..')

from project.views import app

app.run(debug=True)