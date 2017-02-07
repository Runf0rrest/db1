from generator import Generator

gen = Generator('test.yaml')

file = open('C:\\test.sql', 'w')

for statement in gen.generate_statements():
    file.write(statement)

file.close()