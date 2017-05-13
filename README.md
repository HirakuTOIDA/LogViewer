### Simple Log Viewer in Python
Libraries used in this script: numpy, scipy, pylab and matplotlib  
This script is checked with Python(x,y) 2.7.6.1 <https://code.google.com/p/pythonxy/>.

#### TotalLogViewer.py
Log viewer script for H page.  
`Usage: python TotalLogViewer.py <dir> <filename>`  
This script automatically add "_H.csv" to &lt;filename&gt;.  
Please use this script to check log file before clipping.

#### LogViewer.py
Log viewer script for G, H and N page. This script also interpolates A, G, H, M and N pages for data analysis.  
`Usage: python LogViewer.py <dir> <filename>`  
This script automatically add "_&lt;pagename&gt;.csv" to &lt;filename&gt;.  
New interpolated files with "_out" and image file of the log will be generated.  

#### calibration.py
Calibration constants. Please modify this file to fit to your sensors.

#### License
Copyright (c) 2014 Hiraku Toida

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
