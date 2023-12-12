import pyflowchart
from pyflowchart import output_html, Flowchart

filepath_infile = 'src/time_management/helpers.py'
filepath_outfile = 'flowcharts/generated/helpers.html'

with open(filepath_infile) as f:
	code = f.read()
generated_flowchart = Flowchart.from_code(code, field="", inner=True, simplify=False, conds_align=False)
output_html(output_name=filepath_outfile , field_name='function', flowchart=generated_flowchart.flowchart()) 