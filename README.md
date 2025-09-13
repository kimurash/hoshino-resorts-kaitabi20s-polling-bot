# hoshino-resorts-kaitabi20s-polling

[界タビ20s](https://hoshinoresorts.com/jp/sp/kaitabi20s/) の出雲の予約サイトをポーリングして予約可能な日程を通知するプログラム

## 環境構築

> [!IMPORTANT]
> [uv](https://docs.astral.sh/uv/) を使用して仮想環境を構築する。

必要なパッケージをインストールする。

```
uv sync
```

環境変数を記入する。

```
cp src/.env.sample src/.env
```

| 環境変数名                 | 値                                       | 
| -------------------------- | ---------------------------------------- | 
| LINE_USER_ID               | 通知先のユーザーID                       | 
| LINE_CHANNEL_ACCESS_TOKEN  | メッセージを送信するために必要な機密情報 | 
| SLACK_WEBHOOK_URL          | Slack に通知するための Webhook URL     | 

`LINE_CHANNEL_ACCESS_TOKEN` の値は [shunsei](https://github.com/kimurash) からもらってください。

`src` 直下に以下の内容で `notification.json` を作成する。

```json
[]
```

## Windows での定期実行

[この記事](https://zenn.dev/t0mzenn/articles/e59395528684fe) を参考にして定期実行を試みる。
