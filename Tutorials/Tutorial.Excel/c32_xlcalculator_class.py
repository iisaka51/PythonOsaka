from xlcalculator import ModelCompiler, Evaluator, Model
from typing import Optional

class Workbook:
    def __init__(self,
                 workbook: str = "./sample.xlsx",
                 evaluator: Optional[Evaluator] = None):
        if evaluator:
            self.evaluator = evaluator
        else:
            compiler = ModelCompiler()
            new_model = compiler.read_and_parse_archive(workbook)
            self.evaluator = Evaluator(new_model)
        self.workbook = workbook
        self.worksheet = None

    def get_cell_value(self,
                       worksheet: Optional[str]=None,
                       address: str='A1'):
        if worksheet:
            self.worksheet = worksheet

        return (self.evaluator
                .evaluate(f"{self.worksheet}!{address}")
                .value)

    def set_cell_value(self,
                       worksheet: Optional[str]=None,
                       address: str='A1',
                       value: str=0):
        if worksheet:
            self.worksheet = worksheet

        self.evaluator.set_cell_value(
                           f"{self.worksheet}!{address}",
                           value)

wb = Workbook('output_formula.xlsx')

val1 = wb.get_cell_value(worksheet='Sheet', address='A1')
val2 = wb.get_cell_value(address='A2')
wb.set_cell_value(address='A1', value=100)
val3 = wb.get_cell_value(address='A2')

# val1
# val2
# val3
