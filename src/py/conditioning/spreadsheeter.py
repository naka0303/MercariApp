import os
import gspread

class SpreadSheeter:
    def make_sheet(self, oauth_path, all_idx_name_price_img_removed):
        # OAuthキーの利用
        gc = gspread.oauth(
            # client_secretパスを格納
            credentials_filename=os.path.join(oauth_path, "client_secret_708479444314-fkprkidrq71eab4kogdep1hcac4pvr55.apps.googleusercontent.com.json"),
            # 認証ファイルの保存先パスを格納
            authorized_user_filename=os.path.join(oauth_path, "authorized_user.json")
        )

        # 書き込み先のスプレッドシートの取得
        wb = gc.open_by_key("1VeC31uBKnkrYm7MrzVag1Fo9f0lZzw4Qw4Ty68W0v5Q")
        # 書き込むシートを取得
        ws = wb.worksheet("シート1")

        # 書き込み
        for row in all_idx_name_price_img_removed:
            ws.append_row([row[0], row[1], row[2], row[3]])
