# Python関連

## Pypi
- [pypiserver · PyPI](https://pypi.org/project/pypiserver/)
- [python-pypi-mirror · PyPI](https://pypi.org/project/python-pypi-mirror/)
- [twine · PyPI](https://pypi.org/project/twine/)  
  Twine is a utility for publishing Python packages on PyPI or pypiserver.


## CLIのオプション解析


### Typer
[Typer](https://github.com/tiangolo/type) はオプション解析処理してくれるPythonモジュールです。内部ではClicjkを利用しています。
Click がデコレータでオプション解析処理の指示を与えるのに対して、Typer は変数のタイプヒントを利用して定義するため、より簡潔な記述となるのが特徴です。
タイプヒントを使用しているため、オプションや引数が増えてもコードがスッキリ読みやすくなります。反面、既存の関数については定義を修正するか、ラッパー関数を定義する必要があることと、使用できるPython のバージョンに制限があります。
また、可変長キーワード引数で受け取るような関数には直接適用できません。


- [オプション解析モジュールTyperを使いこなそう - PythonOsaka](https://scrapbox.io/PythonOsaka/%E3%82%AA%E3%83%97%E3%82%B7%E3%83%A7%E3%83%B3%E8%A7%A3%E6%9E%90%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%ABTyper%E3%82%92%E4%BD%BF%E3%81%84%E3%81%93%E3%81%AA%E3%81%9D%E3%81%86)


### cmdkit
[cmdkit](https://github.com/glentner/CmdKit) は rgparse を派生させて、コンソールアプリケーションに必要ないくつかの共通パターンを実装したもの。クラス定義としてCLIを構築してゆくため非常に柔軟で開発がしやすく、小規模なコンソールツールから、git のようなサブコマンドを持つ複雑なアプリケーションもカバーしています。

- [CLIアプリケーションフレームワークcmdkitを使ってみよう - PythonOsaka](https://scrapbox.io/PythonOsaka/CLI%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%95%E3%83%AC%E3%83%BC%E3%83%A0%E3%83%AF%E3%83%BC%E3%82%AFcmdkit%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%88%E3%81%86)
  
  
## Excel ファイルの読み書き
Python でExcelファイルを扱うためには、いくつかの方法があります。用途により使い分けることが多いです。
Pandas や Polars はデータ処理を行う場合に便利ですが、Excelファイルの読み書きだけの目的では、モジュールのサイズは大きくなってしまいます。
読み込んだデータを DataFrame として処理できるので扱いやすいのですが、
セルの書式を扱えません。
その場合は、openpyxl を使用することになります。

- [Excelファイルの読み書きしてみよう - PythonOsaka](https://scrapbox.io/PythonOsaka/Excel%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E8%AA%AD%E3%81%BF%E6%9B%B8%E3%81%8D%E3%81%97%E3%81%A6%E3%81%BF%E3%82%88%E3%81%86)
- [Python openpyxl - Excel Formatting Cells - Python In Office](https://pythoninoffice.com/python-openpyxl-excel-formatting-cells/)




## CISCO

### IOS
CSICO IOSでのパスワード変更の手順は次の資料が参考になる  


- [IOS-XR: パスワードリカバリ手順 - Cisco Community](https://community.cisco.com/t5/tkb-%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E3%83%97%E3%83%AD%E3%83%90%E3%82%A4%E3%83%80-%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88/ios-xr-%E3%83%91%E3%82%B9%E3%83%AF%E3%83%BC%E3%83%89%E3%83%AA%E3%82%AB%E3%83%90%E3%83%AA%E6%89%8B%E9%A0%86/ta-p/3161259)
- [Ciscoルータのパスワードを忘れた時のリカバリー方法（特権モード、ログイン、コンソール、telnet、ssh含む） | purpledice.jp](https://www.purpledice.jp/cisco/cisco-router-password-reset-guide/)
- [シスコルータのコンフィグ作成をPythonで自動化してみた！ - 株式会社ライトコード](https://rightcode.co.jp/blogs/26533)


### SonicOS

- [SonicOS API with python3 — SonicWall Community](https://community.sonicwall.com/technology-and-support/discussion/2301/sonicos-api-with-python3)

### Python 経由でIOSを操作する方法

- [pythonを使ってCisco IOS機器のバックアップを取得してみた #Python - Qiita](https://qiita.com/inetcpl/items/54199b0bc9e07598929d)
- [ネットワークエンジニアのプログラミング【Python入門(設定変更)】](https://infrastructure-engineer.com/python-network-003/)
- [plumbum](https://plumbum.readthedocs.io/en/latest/)  
  Pythonでシェルスクリプトのようなプログラムを書くためのライブラリ。CLI も作成できる
