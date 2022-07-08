from sspipe import p

# ビューオブジェクトにはパイプ演算子は使用できない
# 次の式は返ってこない...
#  {1: 2, 3: 4}.items() | p(list) | p(print)

# スラッシュ演算子ではOK
{1: 2, 3: 4}.items() / p(list) | p(print)

# 私はこちらの記述の方が好き。 pathlib の Path との関係
list({1: 2, 3: 4}.items()) | p(print)
