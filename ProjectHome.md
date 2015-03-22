用LaTeX写论文, PPT或者书籍的过程中, 相信很多人熟悉如下的编译过程

xelatex art.tex

bibtex  art.aux

xelatex art.tex

xelatex art.tex

bibtex 的作用是由辅助文件 art.aux, 参考文献 ref.bib
以及样式文件 style.bst 来生成 art.bbl 文件,
在接下来的两次xelatex编译中, 将 art.bbl 文件中的内容放到 art.tex 中的\bibliography{ref.bib} 的位置.

然而, 当论文的参考文献中含有中文字符时, bibtex没法很好的处理参考文献的顺序.
bibtex依赖于一个bst文件来配置参考文献的样式,
如plain.bst, unsrt.bst, siam.bst, ieee.pst等等, 这些都不能处理中文字符的顺序.

此时, 使用如下的编译过程

xelatex  art.tex

pybibtex art.aux

xelatex  art.tex

xelatex  art.tex

就能解决您的问题, 和 bibtex 一样,
pybibtex 也生成 art.bbl 文件, 英文在前, 中文在后.

并且 pybibtex 可以根据参数配置您的参考文献 ref.bib 的编码,
也就是说, 您的 ref.bib 可以是utf-8, gbk 等任意编码!





As we all know, bibtex can not process bibliography with Chinese Character correctly,
pybibtex can process Chinese bibliography very well.