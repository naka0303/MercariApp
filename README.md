# REQUIREMENTS
  - chromedriverのバージョンは「107.0.5304.62」にすること
  ※ 他verでの動作保証なし
  - chromedriverはMercariApp直下に「driver」ディレクトリを作成し、そこに格納すること

# USAGE
  ```
  cd src/
  python3 main.py <arg1> <arg2> <arg3>; echo $?
  ```
  ※ 引数はメルカリでの検索キーワードで、最大3ワード入力可能

# NOTES
  - cronで定期実行することを想定しているが、単発実行でもOK


