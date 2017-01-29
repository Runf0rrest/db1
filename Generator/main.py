from generator import Generator

gen = Generator('test.yaml')

for statement in gen.generate_statements():
    print(statement)
