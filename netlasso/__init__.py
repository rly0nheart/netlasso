import os

__author__ = "Richard Mwewa"
__about__ = "https://about.me/rly0nheart"
__version__ = "1.4.0"
__description__ = """
# Net Lasso
> **Net Lasso** utilises the [Netlas.io API](https://netlas.io/api) to perform advanced searches for internet-connected 
(IoT) devices based on user-provided search queries.
"""

__epilog__ = f"""
# by [{__author__}]({__about__})
```
MIT License

Copyright © 2023 {__author__}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
"""

# Construct path to the program's directory
PROGRAM_DIRECTORY = os.path.expanduser(os.path.join("~", "netlasso"))

# Construct path to the current file's directory
CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
# Construct paths to directories of CSV and JSON files.
CSV_DIRECTORY = os.path.join(PROGRAM_DIRECTORY, "csv")
JSON_DIRECTORY = os.path.join(PROGRAM_DIRECTORY, "json")
