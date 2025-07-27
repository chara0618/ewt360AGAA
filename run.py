import re
import sys
from streamlit.web import cli

if __name__ == '__main__':
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.argv.append('run')
    sys.argv.append('python/main.py')
    sys.exit(cli.main())