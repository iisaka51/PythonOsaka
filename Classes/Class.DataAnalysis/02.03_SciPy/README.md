SciPy を使ってみよう
=================
### SciPy
SciPy は科学技術計算の問題を処理するためのたくさんの関数やツールがあり、応用範囲ごとにサブモジュールにまとめられています。

 SciPy のサブモジュールと応用範囲

| サブモジュール | 応用範囲 |
|:--|:--|
| scipy.cluster | 階層的クラスタリング、ベクトル量子化、K平均 |
| scipy.constants | 物理数学定数 |
| scipy.fftpack | フリーエ変換 |
| scipy.integrate | 積分ルーチン |
| scipy.interpolate | 補間ルーチン |
| scipy.io | データ入出力 |
| scipy.linalg | 線形代数ルーチン |
| scipy.misc | 画像の幾何学的変換など |
| scipy.ndimage | 多次元画像処理のためのさまざまな機能 |
| scipy.odr | 直交距離回帰 |
| scipy.optimize | 線形計画法を含む最適化アルゴリズム |
| scipy.signal | 信号処理 |
| scipy.sparse | スパース行列と関連アルゴリズム |
| scipy.spatial | 空間データ構造とアルゴリズム |
| scipy.special | 任意の数学特殊関数 |
| scipy.stats | 統計関数 |
| scipy.weave | C / C ++コードをPythonの複数行の文字列として書くためのツール |

これらのサブモジュールをどのように使うのかという説明を個々に細かくしてしまうと、とても時間も足りないうえに数学や統計学の講義のように退屈なだけです。
微分方程式をSciPy を使って解くことをここで説明しても、楽しくないでしょう？

必要になったときに調べてみる、あるいは利用しているプログラムを読んでみるのが一番だと考えています。
そのため、ここでは紹介にとどめておくことにします。


### インストール
SciPy は拡張モジュールなので次のようにインストールします。
 bash condaの場合
```
 $ conda install scipy
 bash pipの場合
```
 $ pip install scipy
```

### SciPy の利用準備

SciPy の関数のほとんどは、NumPy に依存しているので、併せてインポートします。
またSciPy は広範囲の領域をカバーしているため、必要なサブモジュールだけをインポートする方がよいでしょう。

scipy.stats をインポートする場合の例：
 Ipython
```
 In [1]: import numpy as np                                                 In [2]: from scipy import stats 
```


### 画像処理
単純に**フーリエ変換(fourier transform)**と聞くとWebアプリケーションなどでは使う場面がなさそうに思われるかもしれません。しかし、フーリエ変換は画像や音声のノイズ除去などで使われることが多い計算処理です。アプリケーションによっては使うこともあるかもしれませんよね。

> **高速フーリエ変換（FFT: Fast Fourier Transform)**
> **離散フーリエ変換（DFT Discrete Fourier Transform)**をコンピュータで高速に計算する
> アルゴリズムです。コンピュータ領域では単にフーリエ変換と言われることもあります。
> FFTの逆変換を**逆高速フーリエ変換（IFFT: Inverse Fast Fourier Transform)** といいます。

[SciPy Lecture notes ](https://scipy-lectures.org/) で説明されているコードを紹介しておきます。

次の月面着陸の画像 [moonlanding.png ](https://scipy-lectures.org/_downloads/moonlanding.png) には周期的なノイズがあります。

[](https://scipy-lectures.org/_downloads/moonlanding.png)

この画像のノイズ除去をしてみましょう。
これには、フーリエ変換を使って次の畳込みを行うとノイズ除去ができます。


[$ f_{1}\left( t\right) =\int dt'K\left( t-t' \right) f_{0}\left( t' \right) ]
[$ \tilde f_{1}(w) = \tilde K(w)\tilde f_{0}(w)]


まず、画像を読み込みましょう。
 IPython
```
 In [1]: %matplotlib                                                        Using matplotlib backend: MacOSX
 
 In [2]: %load moonlanding.py                                               In [3]: # %load moonlanding.py 
    ...: import numpy as np 
    ...: import matplotlib.pyplot as plt 
    ...:  
    ...: im = plt.imread('./moonlanding.png').astype(float) 
    ...:  
    ...: plt.figure() 
    ...: plt.imshow(im, plt.cm.gray) 
    ...: plt.title('Original image') 
    ...:                                                                    Out[3]: Text(0.5, 1.0, 'Original image')
```


![](https://gyazo.com/29bfcdb2885efbf47d884380697573d1.png)

#### ２次元FFT変換
読み込んだ画像データを２次元FFT変換を行い周波数スペクトルに変換します。
次のコードはプロットするために少し長くなっていますが、
２次元FFT変換の計算は、 `fftpack.fft2()` を呼び出すだけです。
 IPyhon
```
 In [6]: # %load 2ndfft.py 
    ...: from scipy import fftpack 
    ...: im_fft = fftpack.fft2(im) 
    ...:  
    ...: def plot_spectrum(im_fft): 
    ...:     from matplotlib.colors import LogNorm 
    ...:     # A logarithmic colormap 
    ...:     plt.imshow(np.abs(im_fft), norm=LogNorm(vmin=5)) 
    ...:     plt.colorbar() 
    ...:  
    ...: plt.figure() 
    ...: plot_spectrum(im_fft) 
    ...: plt.title('Fourier transform') 
    ...:                                                                           
 Out[6]: Text(0.5, 1.0, 'Fourier transform')
```

![](https://gyazo.com/42d67793851eccd66226f492624a7b9c.png)


#### フィルタ処理
ローパスフィル処理（カットオフ周波数を超える帯域の周波数スペクトルを0にする）を行います。
まず、保持する係数の割合を `keep_fraction` に定義します。
 IPython
```
 In [6]: keep_fraction = 0.1                                               
```

Numpy配列には `copy()` メソッドを使って、元のFFT変換をコピーします。
 IPython
```
 In [7]: im_fft2 = im_fft.copy() 
```

配列形状の行と列の数を `r` と `c` に設定します。
IPython
```
 In [8]: r, c = im_fft2.shape
```

 `r * keep_fraction` と  `r *(1-keep_fraction)` の間のインデックスを持つ、
すべての行をゼロに設定します
 IPyhton
```
 In [9]: im_fft2[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0
```

同じことをカラム（列）に対して行います。
 IPython
```
 In [10]: im_fft2[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0 
```

これをプロットしてみます。
 IPyhon
```
 In [11]: plt.figure() 
     ...: plot_spectrum(im_fft2) 
     ...: plt.title('Filtered Spectrum')                                           
 Out[11]: Text(0.5, 1.0, 'Filtered Spectrum')
```

![](https://gyazo.com/ee78dd273ac5b77fb579c7fb0d33b319.png)

#### 再構築
フィルター処理されたスペクトルからノイズ除去された画像を再構成します。
これには、逆フーリエ変換(IFFT)を行って処理します。
フーリエ変換は入出力ともの複素数になるため、実部(real)のみを表示用に保持します。

 IPython
```
 In [12]: im_new = fftpack.ifft2(im_fft2).real
```

再構築された画像を表示してみます。
 IPython
```
 In [13]: plt.figure() 
     ...: plt.imshow(im_new, plt.cm.gray) 
     ...: plt.title('Reconstructed Image')                                         
 Out[13]: Text(0.5, 1.0, 'Reconstructed Image')
```


![](https://gyazo.com/579bfe893a0916736a2df3089d2d431f.png)

ここまでのコードを１つにまとめて整理すると次のようになります。

 moonlanding_nose_reduction.py
```
 import numpy as np
 from scipy import fftpack
 import matplotlib.pyplot as plt
 
 im = plt.imread('./moonlanding.png').astype(float)
 
 im_fft = fftpack.fft2(im)
 
 im_fft2 = im_fft.copy()
 r, c = im_fft2.shape
 
 keep_fraction = 0.1
 im_fft2[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0
 im_fft2[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0
 
 im_new = fftpack.ifft2(im_fft2).real
 plt.imsave('moonlanding_new.png', im_new) 
```

数学的なことは「とりあえずおいといて」、わずかなコードで画像のノイズ除去ができることがわかりましたね。

参考:
- [SciPy オフィシャルサイト ](https://www.scipy.org/)
- [SciPy Lecure notes ](https://scipy-lectures.org/)
- [SciPy Lecture notes (日本語) http://www.turbare.net/transl/scipy-lecture-notes/index.html]
- [東北大学 中川教授 - 初心者用 たたみこみの解説 ](https://www.ice.tohtech.ac.jp/nakagawa/laplacetrans/convolution1.htm)



