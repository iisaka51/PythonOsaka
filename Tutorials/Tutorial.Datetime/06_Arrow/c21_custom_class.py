import arrow

class Custom(arrow.Arrow):
    def till_christmas(self):
        """
        ある日付がその年のクリスマスの後に来る場合、
        次の年のクリスマスとの差を計算
        """
        christmas = arrow.Arrow(self.year, 12, 25)
        if self > christmas:
              christmas = christmas.shift(years=1)

        return (christmas - self).days

func = arrow.ArrowFactory(Custom)  # create factory function
x = func.now()
days = x.till_christmas()

print(f'次のクリスマスまで、あと{days}日')
