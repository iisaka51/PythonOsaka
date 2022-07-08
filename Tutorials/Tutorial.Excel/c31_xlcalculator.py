from xlcalculator import ModelCompiler, Evaluator, Model

workbook_path = './output_formula.xlsx'
compiler = ModelCompiler()
new_model = compiler.read_and_parse_archive(workbook_path)
evaluator = Evaluator(new_model)
val1 = evaluator.evaluate('Sheet!A1').value
val2 = evaluator.evaluate('Sheet!A2').value

evaluator.set_cell_value('Sheet!A1', 100)
val3 = evaluator.evaluate('Sheet!A1').value
val4 = evaluator.evaluate('Sheet!A2').value

# val1
# val2
# val3
# val4
