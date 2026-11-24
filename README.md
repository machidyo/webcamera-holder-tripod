# webcamera-holder-tripod

ELP USB4KHDR01 (38.17 x 38.17 mm 基板) 用の Web カメラホルダです。
[build123d](https://github.com/gumyr/build123d) で記述したパラメトリックモデルで、
裏蓋中央の 1/4"-20 インサートナットで SmallRig などのボールヘッド (三脚ねじ) に取り付けます。
基板は M2 ねじとインサートナットで本体に固定します。

## 部品

| 部品 | ファイル | 説明 |
|---|---|---|
| housing | `output/housing.stl` | 本体。前面レンズ開口、M2 インサート用ボス 4 本 (下穴 3.05 mm、深さ 6 mm)、縦スロットの通気穴 |
| cover | `output/cover.stl` | 裏蓋。スナップ嵌合。板厚 9.5 mm、中央に 1/4"-20 インサート用の止まり穴 (下穴 7.6 mm、深さ 8.5 mm)。上辺に幅 24 mm のケーブル切り欠き |

`output/webcamera_holder.3mf` に全部品を印刷向きで並べてあります。Bambu Studio にそのまま読み込めます。

## 別途用意するもの

- 1/4"-20 インサートナット 1 個: [Aicosineg 真鍮インサートナット 1/4-20](https://www.amazon.co.jp/dp/B0CMXJ57TP) (外径 8 mm / L 6 mm)
- M2 インサートナット 4 個: [ミスミ MBIS2-3-4](https://jp.misumi-ec.com/vona2/detail/110310292949/?ProductCode=MBIS2-3-4) (D1 3.0 / D2 3.3 / L 4.0 mm)
- M2 ねじ 4 本 (長さ 5 mm 前後。基板厚 1.64 mm + インサート 4 mm)
- 1/4"-20 ねじ付きのボールヘッドや三脚

## 対象基板

- ELP USB4KHDR01: 38.17 mm 角、厚さ 1.64 mm、取付穴ピッチ約 34 mm
- 基板裏面に縦型 4 ピン 2.0 mm ピッチのコネクタがあり、ケーブルが真後ろへ出るタイプ

寸法は `webcamera_holder.py` 先頭のパラメータにまとめてあるので、別の基板に合わせる場合はそこを変更してください。

## 印刷条件

- Bambu Lab A1 mini / PLA
- レイヤ高さ 0.2 mm、壁 2 から 3 本 (インサートまわりは壁を多めにすると保持力が上がる)
- housing はそのままの向き (レンズ面がベッド)、cover は裏返した状態 (外面がベッド) で出力済み (サポート不要)

## 組み立て

1. housing のボス 4 本に M2 インサートナットを基板側から熱圧入する
2. cover の外面中央の穴に 1/4"-20 インサートナットを熱圧入する
3. housing のボスに基板を載せ、M2 ねじ 4 本で留める
4. ケーブルを切り欠きに通し、cover をスナップで閉じる
5. cover のインサートにボールヘッドのねじを締め込む

## 設計メモ

- 通気穴は縦長スロット。印刷時に壁が垂直になるのでブリッジが不要
- cover の板厚は止まり穴深さ 8.5 mm (ボールヘッドのねじ突き出し 約 7 mm + 余裕 1.5 mm) + 穴底 1.0 mm。穴まわりの肉厚は 3.3 mm 以上を確保
- 1/4" インサートの下穴 7.6 mm はローレット外径 8.0 mm より細くして食い込ませるための値。緩い / 入らない場合は `TRIPOD_INSERT_HOLE_D` を調整
- 基板をねじ止めするため、cover の基板押さえ柱は既定で無効 (`BOARD_PRESS`)。ねじを使わない場合は有効にする
- カメラの重さは cover と housing のスナップ嵌合で支える

## モデルの再生成

```sh
pip install -r requirements.txt
python webcamera_holder.py
```

`output/` に STL、STEP、3MF が出力されます。`ocp_vscode` が入っていると実行後にビューワへ表示します。
表示を抑止する場合は環境変数 `NO_SHOW=1` を付けてください。
