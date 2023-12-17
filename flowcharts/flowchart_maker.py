import os
import ast
from pyflowchart import Flowchart, output_html

class AutoFlowchartMaker:
    def __init__(self, root_directory ,output_folder ):
        self.generate_flowcharts_in_directory(root_directory, output_folder)

    def generate_flowcharts_in_directory(self, root_directory, output_folder):
        for root, _, files in os.walk(root_directory):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    file_path = os.path.join(root, file)
                    self.process_python_file(file_path, output_folder)

    def process_python_file(self, file_path, output_folder):
        with open(file_path) as f:
            code = f.read()

        tree = ast.parse(code)

        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                output_filename = f'{output_folder}{node.name}.html'
                self.generate_flowchart(node, output_filename)

    def generate_flowchart(self, node, filename):
        generated_flowchart = Flowchart.from_code(node, field=node.name, inner=True, simplify=False, conds_align=False)
        output_html(output_name=filename, field_name='function', flowchart=generated_flowchart.flowchart())

if __name__ == "__main__":
    root_directory = 'src'
    output_folder = 'flowcharts/generated/'
    AutoFlowchartMaker(root_directory, output_folder)
