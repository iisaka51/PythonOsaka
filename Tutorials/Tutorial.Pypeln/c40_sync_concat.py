import pypeln as pl

stage_1 = [1, 2, 3]
stage_2 = [4, 5, 6, 7]


def main():
    stage_3 = pl.sync.concat([stage_1, stage_2])
    data = list(stage_3)
    print(data)

if __name__ == '__main__':
    main()
