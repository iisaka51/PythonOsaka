# 演習１ アプリケーションを作成してみよう

次の２つのファイルは、指定したパスにあるCSVファイルを読み出すもためのプログラムを
argparse で実装したものです。

```

"""
See Also:
 * How can I detect if a file is binary (non-text) in Python?
   - https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
"""

def is_binary(filepath):
    with open(filepath, 'rb') as f:
        if b'\0' in f.read(4096):
            return True
        else:
            return False

```


```
import csv
from is_binary import is_binary

__VERSION__ = "0.1.0"

def cmd(csvfiles):
    for filepath in csvfiles:
        print(f'--- {filepath} ----')
        if is_binary(filepath):
            print('This is not CSVfile.')
            continue
        with open(filepath) as f:
            data = csv.reader(f)
            rawcount = 0
            for row in data:
                print(row)
                rawcount += 1
            else:
                if rawcount == 0:
                    print('This is empty CSVFile.')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description ='show CSV files')
    parser.add_argument(dest ='filepath', metavar ='filepath', nargs ='*')
    args = parser.parse_args()
    cmd(args.filepath)
```


## 演習1.1
　オプション解析処理を `argparse` から `click` に変更してみましょう。
　オプション`--version` でバージョン情報を表示するようにしてみましょう。
　目標時間：２０分

## 演習1.2
 変更したスクリプトを`click` と `pip`コマンドを使って、
 アプリケーション `myreadcsv` として、インストールしてみましょう。
 目標時間：10分

## 演習1.3
 読み込んだ CSVファイルの先頭から5行を、
 `prompt-toolkit` の `message_dialog` を使って表示させてみましょう。
　目標時間：10分

