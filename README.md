# cis-lab-smart-lock

学生証によって [情報知能システム研究室](https://vega.is.kit.ac.jp/) の鍵を開けるプログラム

## 環境構築

[uv](https://docs.astral.sh/uv/) を使用して仮想環境を構築する

```
uv sync
```

## 実行方法

`src/.env` ファイルを作成して内容を記述する．

```
cp src/.env.sample src/.env
```

環境変数の一覧

| 環境変数名 | 内容 |
| --- | --- |
| PASORI_BUS_NO |  PaSoRiが接続されているバス番号 |
| PASORI_DEVICE_NO |  PaSoRiが接続されているデバイス番号 |
| PASORI_VENDOR_ID | PaSoRiのベンダーID |
| PASORI_PRODUCT_ID |  PaSoRiのプロダクトID |
| SYSTEM_CODE | 学生証が格納されているSystemコード |
| SERVICE_NO | 学生証が格納されているService番号 |
| SERVICE_ATTR | 学生証が格納されているService属性 |
| BLOCK_NO | 学生証が格納されているBlock番号 |
| SWITCHBOT_TOKEN | SwitchBotのAPIトークン |
| SWITCHBOT_SECRET | SwitchBotの秘密鍵 |
| SLACK_WEBHOOK_URL | Incoming WebhokのURL |

srcディレクトリの直下に `student_id.txt` を作成して入室を許可する学生の学生番号を1行ずつ記述する．

```
24622017
24622033
...
```

仮想環境を有効化して `main.py` を実行する．

```
source .venv/bin/activate
python main.py
```
