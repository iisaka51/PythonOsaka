演習1：分析に挑戦してみよう
=================
### 演習1.1


### チャレンジ課題
#### 演習1.2
1949～1960年における月別飛行機搭乗者数を集計された時系列データ [AirPassengers ](https://www.analyticsvidhya.com/wp-content/uploads/2016/02/AirPassengers.csv) を使ってデータ分析を行ってみましょう。

時系列データなので、通常は次の順序で分析を行います。

- 時系列のパラメータを確認する
  - サンプリングの開始点、終了点、収集間隔（頻度）を知る
- 定常性の確認
- 全体的なトレンドを確認する
  - レベル：時系列データのベースライン値
  - トレンド：時系列データの線形回帰したときの傾きの増加/減少
  - 観察時間窓を広くして平均化し、短期的な変動や、季節性傾向を取り除く
- 周期的なトレンドを確認する
  - 短期的な変動を観察する
  - 季節性傾向：時間の経過にともなう変動の大きさ（レンジ）を観察する
- ノイズ：トレンドと季節性では説明できない観測値の変動性
  - データによっては事故、ニュースイベントなどの外乱要因に影響される
- 考察

実際の分析には、自己分析モデルを構築して、自己相関分析を行い、検定を行う必要があります。これには、統計学の知識が必要になります。



