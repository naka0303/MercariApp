# REQUIREMENTS
  - chromedriverのバージョンは「107.0.5304.62」にすること
  ※ 他verでの動作保証なし
  - chromedriverはMercariApp直下に「driver」ディレクトリを作成し、そこに格納すること
  - 

# USAGE
  ```
  cd src/py/
  python3 main.py <arg1> <arg2> <arg3>; echo $?
  ```
  ※ 引数はメルカリでの検索キーワードで、最大3ワード入力可能

# NOTES
  - cronで定期実行することを想定しているが、単発実行でもOK  
  ※ 定期実行の場合は、1時間に1回のペースの予定
  - スプレッドシート出力用
  https://party-engineer.com/%E3%80%90%E3%82%B9%E3%83%97%E3%83%AC%E3%83%83%E3%83%89%E3%82%B7%E3%83%BC%E3%83%88%E3%81%AE%E5%85%B1%E6%9C%89%E4%B8%8D%E8%A6%81%E3%80%91python%E3%81%A7google%E3%82%B9%E3%83%97%E3%83%AC%E3%83%83/#toc1



