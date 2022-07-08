import pypeln as pl

pl.process.map(f, stage) = pl.process.flat_map(lambda x: [f(x)], stage)
pl.process.filter(f, stage) = pl.process.flat_map(
                                   lambda x: [x] if f(x) else [], stage)
