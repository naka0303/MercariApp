# REQUIREMENTS
## ローカル実行
  - chromedriverをインストールしておくこと  
    ※ verは「107.0.5304.62」にし、Google Chromeのverは「107.0.5304.110」にすること  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;なお、他verでの動作保証なし
  - 以下ディレクトリをMercariApp直下に作成すること
    - logs (ログ格納先)
    - csv (商品情報出力csv格納先)
    - driver (chromedriver格納先)
    - oauth (クライアントIDとシークレット情報のJSON格納先)  
    ※ JSON作成方法は、以下サイトを参考  
    https://party-engineer.com/%E3%80%90%E3%82%B9%E3%83%97%E3%83%AC%E3%83%83%E3%83%89%E3%82%B7%E3%83%BC%E3%83%88%E3%81%AE%E5%85%B1%E6%9C%89%E4%B8%8D%E8%A6%81%E3%80%91python%E3%81%A7google%E3%82%B9%E3%83%97%E3%83%AC%E3%83%83/#toc1

## EC2実行
  - chromedriver-binaryをインストールしておくこと  
  ※ verは「107.0.5304.62」にすること  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;なお、他verでの動作保証なし
  - google-chromeをインストールにしておくこと  
  ※ verは「107.0.5304.110」にすること  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;なお、他verでの動作保証なし

# USAGE
  ```
  cd src/py/
  python3 main.py <arg1> <arg2> <arg3>; echo $?
  ```
  ※ 引数はメルカリでの検索キーワードで、最大3ワード入力可能

# NOTES
  - 実行ブランチは以下  
    ローカル: master  
    EC2: release/on_ec2
  - cronで定期実行することを想定しているが、単発実行でもOK  
  ※ 定期実行の場合は、1時間に1回のペースの予定

# FIXME
  - ローカル実行時と、EC2実行時でブランチが異なっているので、同じブランチで設定値を変えるだけで切り替えられるようにする
  - 必須ディレクトリを手動ではなく自動で作成できるようにする