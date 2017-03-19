from generator import Generator

gen = Generator('test.yaml')

with open('test.sql', 'w') as f:
    for s in gen.generate():
        f.write(s)
