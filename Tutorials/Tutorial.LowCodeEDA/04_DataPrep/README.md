# 準備

DataPrep はインストールでは SciPy をソースコードからビルドすようになっています。
このためプラットフォームによっては pip でのインストールに失敗する場合があります。

回避策として Anaconda Python を使って環境を構築するようにしてみてください。

```bash
 $ pyenv install -l | grep miniconda3
 $ pyenv install miniconda3-4.7.12
 $ conda create -y -n EDA_dataprep python=3.10 scipy numpy dataprep
````

仮想環境を有効にする

```bash
 $ conda activate EDA_dataprep
```

仮想環境を無効にする

```bash
 $ conda deactivate
```

