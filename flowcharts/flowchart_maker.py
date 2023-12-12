import ast
from pyflowchart import Flowchart, output_html

filepath_infile = 'src/time_management/helpers.py'
output_folder = 'flowcharts/generated/'

with open(filepath_infile) as f:
    code = f.read()

tree = ast.parse(code)

def generate_flowchart(node, filename):
    generated_flowchart = Flowchart.from_code(node, field="", inner=True, simplify=False, conds_align=False)
    output_html(output_name=filename, field_name='function', flowchart=generated_flowchart.flowchart())

for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        output_filename = f'{output_folder}{node.name}.html'
        generate_flowchart(node, output_filename)

