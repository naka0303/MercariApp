import logger

class CsvConditioning:

    # メルカリ画面から取得した商品名と価格の配列から不要情報を除去
    def remove_unneeded(self, args, all_name_price):
        idx = 0
        for name_price in all_name_price:
            name = name_price[0]
            price = name_price[1]

            # 検索ワードが商品名にあるかチェック
            none_cnt = 0
            for arg in args:
                if (arg in name):
                    break

                # 検索ワードが商品名に無い場合にインクリメント実施
                none_cnt += 1
            
            # 検索ワード全てが商品名に無ければ配列から削除
            if (none_cnt == 2):
                all_name_price.pop(idx)
            
            idx += 1
        
        return all_name_price
                
            

            

