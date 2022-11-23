import os
import gspread

class SpreadSheeter:
    def make_sheet(self, oauth_path, yyyymmddhhmmss, all_idx_name_price_img_removed):
        # OAuthキーの利用
        gc = gspread.oauth(
            # client_secretパスを格納
            credentials_filename=os.path.join(oauth_path, 'client_secret_708479444314-ijf2a2p87lf2nvpn7p4tbid79uglb4ub.apps.googleusercontent.com.json'),
            # 認証ファイルの保存先パスを格納
            authorized_user_filename=os.path.join(oauth_path, 'authorized_user.json')
        )

        # 書き込み先のスプレッドシートの取得
        wb = gc.open_by_key('1VeC31uBKnkrYm7MrzVag1Fo9f0lZzw4Qw4Ty68W0v5Q')

        # 書き込むシートを作成
        ws = wb.add_worksheet(title=str(yyyymmddhhmmss), rows=100, cols=5)
        cell_list = ws.range('A1:D500')

        # 書き込み用リスト作成
        for i, j in enumerate(all_idx_name_price_img_removed):
            for k, data in enumerate(j):
                updateNum = i * 4 + k
                cell_list[updateNum].value = data

        # 書き込み
        ws.update_cells(cell_list, value_input_option='USER_ENTERED')
