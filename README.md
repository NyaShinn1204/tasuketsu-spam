<p align="center">
    <h3 align="center">tasuketsu.com spammer</h3>
    <p align="center">
        多数決.comのすばらしいスパマーです<br/>
    </p>
</p>

## インストール

**※ Pythonのバージョン3.10以上が必要です**

使うには、以下のコマンドを実行します

> [!TIP]
> これは開發バージョンです！

```bash
git clone https://github.com/NyaShinn1204/tasuketsu-spam

cd tasuketsu-spam

python spam.py
```

また以下の個所の変更が必要です！！！

変更したいときは、spam.py内の265行目
```go
～～～～～
150: zoukaryou = "1" # 増加量                        ！！ここ
151: sent_target = "z-0_{}".format(zoukaryou) 
152: target_id = "" # XeauSxIclNV7ZFXq9zgx など      ！！ここ
～～～～～
```
の二か所を変えてください
