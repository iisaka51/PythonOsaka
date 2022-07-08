%%timeit
animals = ['aardvark', 'bee', 'cat', 'dog']
flowers = ['allium', 'bellflower', 'crocus', 'dahlia']
[(animals[i], flowers[i]) for i in range(min(len(animals), len(flowers)))]
