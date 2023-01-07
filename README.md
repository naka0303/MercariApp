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
## 検索文字列入力フォーム生成実行
  ```bash
  cd src/bash/
  ./start_view.sh; echo $?
  ```

## スクレイピング実行
  ```bash
  cd src/bash/
  ./scrape.sh; echo $?
  ```

## 価格・件数グラフ作成実行
  ```bash
  cd src/bash/
  ./make_gragh.sh; echo $?
  ```

## csvファイルの日別格納用シェル
``` bash
  cd src/bash/
  ./move_csv.sh; echo $?
```

# NOTES
  - 実行ブランチは以下  
    ローカル: master  
    EC2: master
  - 2022/11/27現在では、run.shを手動実行しているが、いずれ定期実行に移行する予定  
    ※1 定期実行の場合は、1時間に1回のペースの予定  
    ※2 定期実行の場合は、検索文字列入力フォームは使わず、検索文字列を固定文字にする
  - GCP APIにOAuth2.0でアクセスしようとすると、以下エラーが発生する場合あり  
  "google.auth.exceptions.RefreshError: ('invalid_grant: Token has been expired or revoked.', '{\n  "error": "invalid_grant",\n  "error_description": "Token has been expired or revoked."\n}')"  
  上記エラーが出る理由は、OAuth同意画面が「外部向け」で、公開ステータスが「テスト」になっていると、7日間で有効期限が切れるリフレッシュトークンが発行されてしまうから  
  → 当面は7日ごとに「OAuth 2.0 クライアント ID」を再発行し、oauth下に配置し直し、元から置いてあったauthorized_user.jsonはbkに退避
  - csvファイルに日別格納用シェルは、23:30にCSVファイルを1日単位のディレクトリに格納する予定(以下、日別ディレクトリと表現)  
    例) csv/2022-11-12
  - 日別ディレクトリに格納する際は、1日分のCSVファイルが存在することを確認してから格納する  
    もしCSVファイルが不足していた場合は、格納用スクリプトは実行しない

# FIXME
  - 時間がずれているので、現時間になるよう修正する(EC2実行時のみ)
  - 必須ディレクトリを手動ではなく自動で作成できるようにする
  - 検索文字列に関して、手動実行の場合は検索文字列入力フォームで入力、定期実行の場合は固定文字にするよう修正する
