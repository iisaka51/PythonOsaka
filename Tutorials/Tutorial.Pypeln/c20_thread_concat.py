import pypeln as pl

stage_1 = [1, 2, 3]
stage_2 = [4, 5, 6, 7]


def main():
    stage_3 = pl.thread.concat([stage_1, stage_2])
    for d in stage_3:
        print(d)

if __name__ == '__main__':
    main()
