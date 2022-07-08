from behold import Behold, Item

# define a global variable
g = 'global_content'

def example_func():
    employee = Item(name='Toby')
    boss = Item(employee=employee, name='Michael')

    print('# グローバル変数は参照できない')
    Behold().show('boss', 'employee', 'g')

    print('\n#上司の名前は表示されるけれど、社員の名前は表示されない')
    Behold('no_employee_name').show(boss)

    print('\n# グローバル変数を参照できるようにする')
    Behold().show(global_g=g, boss=boss)

    print('\n# 文字列の引数を与えることで、変数の順序を強制する')
    Behold().show('global_g', 'boss', global_g=g, boss=boss)

    print('\n# 入れ子になっている属性に対しても同様の方法で指定')
    Behold().show(employee_name=boss.employee.name)

example_func()
