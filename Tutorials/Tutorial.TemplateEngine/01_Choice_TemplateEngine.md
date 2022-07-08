テンプレートエンジンを選定する
=================
テンプレートエンジンは、テンプレートと呼ばれる雛形にデータを渡すとドキュメントを生成するものです。Python で利用されているテンプレートエンジンも多数あります。
実装されている言語を Python に絞らなければ[もっとたくさん ](https://en.wikipedia.org/wiki/Comparison_of_web_template_engines)あります。

- Django Template：Django で使用される組み込みのテンプレートエンジン
- Jinja2：Django Template に触発されて開発。Ansibleなど多数のプロジェクトで採用
- Mako：[Reddit.com ](https://www.reddit.com/)でも使用される、高速で軽量なテンプレートエンジン
- Cheetah：多用途向けの高速なテンプレートエンジン
- YATL：Web2Py で使用されるXML系テンプレートエンジン
- Genshi：XML系テンプレートエンジン
- Spitfire: Cheetah に触発されて開発。Youtubeでも運用されている高速なテンプレートエンジン

大きく分けるとWebアプリケーションの開発を意識したXML系テンプレートエンジンと、
Web以外のドキュメントを生成することを意識した多用途テンプレートエンジンとに、２つに分類することができます。
多用途テンプレートエンジンでは、LaTeXドキュメントやメール、月次レポートといった用途でひな形としも使うこともできます。

WebフレームワークとしてDjango を使うのであれば、テンプレートエンジンは組み込まれているので、別のものは用意しなくても問題はありません。(ただし、Django TemplateよりもJinja2 の方が多機能で、高速です）

しかし、別のWebフレームワークを使うときや、プロジェクトにテンプレートエンジンを組み込みたいときは、Jinja2 はまず選択肢の第１候補になるでしょう。それは、Jinja2 がDjango Templateにインスパイアされて開発されていることもあり、テンプレートファイルが良く似ていて、学習コストが無駄にならないからです。
Webサイトへの同時アクセス数が非常に多く、パフォーマンスが求められるような場合では、mako の利用を検討してもよいでしょう。
また、WebフレームワークとしてPyramidやPylonsを採用する場合では、デフォルトのテンプレート言語はデフォルトのMakoを利用することになるでしょう。


参考: 
- [Wikipedia テンプレートエンジン ](https://ja.wikipedia.org/wiki/テンプレートエンジン)
- [Jinja オフィシャルサイト http://jinja.pocoo.org/]
- [Cheetah オフィシャルサイト ](https://cheetahtemplate.org/)
- [Mako オフィシャルサイト ](https://www.makotemplates.org/)
- [YATL ソースコード ](https://github.com/web2py/yatl)
- [Genshi オフィシャルサイト ](https://genshi.edgewall.org/)
- [Spitfire ソースコード ](https://github.com/youtube/spitfire)



