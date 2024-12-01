from os.path import join
import random
import lorem

random.seed(4090)
root = r'file-transfered'
dirs = ['client-send', 'server-send']

for dir in dirs:
    dir = join(root,dir)
    for i in range(1,10):
        with open(join(dir, f'dummy{i}.txt'), 'w') as f:
            random_text = lorem.paragraph()
            f.write(random_text)