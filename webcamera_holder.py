"""
ELP USB4KHDR01 (38.17 x 38.17 mm, t=1.64 mm) 用 Web カメラホルダ (三脚ねじ取付版)
---------------------------------------------------------------------
参考: "ELP Camera Housing (USBFHD04H)" by Azure (BY-NC) の構成を踏襲し、
基板サイズ 32mm -> 38.17mm、裏面縦型 4P コネクタ (配線が真後ろへ出る) に合わせて
作り直したもの。SmallRig などの 1/4"-20 ボールヘッドを土台にする。部品は 2 種類:

  1. housing : 本体 (前面レンズ開口 + ボス 4 本 + 通気スロット)。
               ボスには M2 インサートナット (ミスミ MBIS2-3-4) を熱圧入し、基板を M2 ねじで留める
  2. cover   : 裏蓋 (スナップ嵌合、コネクタ直上にケーブル切り欠き)。
               中央に 1/4"-20 インサートナット (外径 8 x 長さ 6 mm) を熱圧入できるよう
               板を厚くしてあり、ここにボールヘッドのねじを締め込む

座標系 (housing):
  原点 = 基板中心、+Z = 基板の裏側 (カバー側)、-Z = レンズ側、+Y = 上 (コネクタ側)
  housing はレンズ面が Z=0 にあり、そのままの向きで印刷できる (レンズ面がベッド)。
  cover は外面 (インサート穴の開口側) を下にして印刷する。

Bambu Lab A1 mini / PLA, 0.2mm レイヤ, 壁 2-3 本を想定。
"""

import os
from pathlib import Path

from build123d import *  # noqa: F401,F403

try:
    from ocp_vscode import show
except ImportError:  # viewer が無い環境でも実行できるように
    show = None

# ---------------------------------------------------------------------------
# パラメータ (単位 mm)
# ---------------------------------------------------------------------------
# --- 基板 (実測値) ---
BOARD = 38.17            # 基板 縦横
BOARD_T = 1.64           # 基板 厚さ
BOARD_CLR = 0.40         # 基板周囲の片側クリアランス
HOLE_PITCH = 34.0        # 取付穴ピッチ (写真から推定、要確認)
# M2 インサートナット (ミスミ MBIS2-3-4: D1=3.0, D2=3.3, L=4.0)
#   メーカー推奨: 下穴 = D1 + 0.05、穴深さ >= L + 0.5 (熱圧入)、ボス外径 >= D1 x 2
M2_INSERT_HOLE_D = 3.05  # 下穴径
M2_INSERT_L = 4.0        # インサート長さ
M2_INSERT_DEPTH = 6.0    # 穴深さ (L + 0.5 = 4.5 以上。ねじ先の逃げを含めて深めに)
BOSS_D = 6.0             # ボス外径 (D1 x 2)

LENS_OPEN = 22.5         # 前面レンズ開口 (正方形)。ホルダ台座 約20mm角 + 余裕
LENS_OPEN_R = 1.0        # 開口の角 R

# --- コネクタ (基板裏面の縦型 4P 2.0mm) ---
CONN_X = 0.0             # 基板中心からの X オフセット (前面から見て右が +)
CONN_FROM_EDGE = 6.0     # 基板上辺 (+Y 端) からコネクタ中心までの距離
CONN_W = 10.5            # コネクタ (プラグ込み) X 方向寸法
CONN_D = 5.0             # コネクタ (プラグ込み) Y 方向寸法
CONN_CLR = 1.0           # 切り欠きの片側余裕
# 裏蓋のケーブル切り欠き。ELP (コネクタ中央) と ArduCam UC-844 (横向きコネクタが前面から見て
# 右寄り X=+1..+9 付近、配線が基板に沿って出る) の両方に使えるよう左右対称に広げる
NOTCH_W = 24.0           # 切り欠き幅 (X)。押さえ柱 (X=±17) とその根元を残せる上限付近
NOTCH_FROM_EDGE = 11.5   # 基板上辺から切り欠き下端までの距離 (中央のインサート穴の肉厚を残す)
CABLE_WALL_SLOT = True   # 上壁にもケーブル用スリットを入れる (上方向にも逃がせる)
CABLE_SLOT_W = 5.0       # 上壁スリット幅 (ケーブル径 + 余裕)
CABLE_SLOT_D = 6.0       # 上壁スリット深さ (背面端から)

# --- 本体 ---
WALL = 2.0               # 壁厚 (1.5 -> 2.0: スナップ受け溝を深くできるように)
FRONT_T = 1.0            # 前面板厚
STANDOFF = 7.0           # 前面板内面 -> 基板表面 (ボス高さ)
REAR = 10.0              # 基板裏面 -> 本体背面端 (コネクタ + プラグ 約 8mm)
CORNER_R = 2.0           # 外形 縦エッジ R
FRONT_CHAMFER = 1.0      # 前面外周の面取り
LEAD_IN = 0.6            # 背面開口の内側エッジ面取り (裏蓋リップの入口)

INNER = BOARD + 2 * BOARD_CLR            # 内寸 38.97
OUTER = INNER + 2 * WALL                 # 外寸 42.97
DEPTH = FRONT_T + STANDOFF + BOARD_T + REAR  # 本体奥行 19.64
BOARD_Z = FRONT_T + STANDOFF             # 基板表面の Z
HOLE_OFF = HOLE_PITCH / 2

# --- 通気スロット (縦長の長穴。印刷時は壁が垂直なので縦スロットはブリッジ不要) ---
VENTS = True
VENT_SLOT_W = 1.8        # スロット幅
VENT_PITCH = 3.5         # スロット間隔
VENT_SIDE_XS = [i * VENT_PITCH for i in range(-3, 4)]        # 左右壁: 7 本 (|Y| <= 11.4、ボスと干渉しない)
VENT_TOP_XS = [s * x for s in (-1, 1) for x in (4.5, 8.0, 11.5)]  # 上壁: 中央のケーブルスリットを避けて 6 本

# --- 裏蓋 ---
# 中央の 1/4"-20 インサートナット (Aicosineg 真鍮ローレット: 外径 8.0, L=6.0。Amazon B0CMXJ57TP)
#   下穴はローレット外径より 0.4 mm 細くして樹脂に食い込ませる (印刷で穴はさらに 0.1 mm ほど縮む)。
#   穴深さはインサート長ではなく、ボールヘッドのねじの突き出し (実測 約 7 mm) + 余裕で決める。
TRIPOD_INSERT_OD = 8.0         # インサートのローレット外径
TRIPOD_INSERT_L = 6.0          # インサート長さ
TRIPOD_SCREW_LEN = 7.0         # ボールヘッドの 1/4 ねじの突き出し長さ (実測)
TRIPOD_INSERT_HOLE_D = 7.6     # 下穴径 (緩ければ 7.5、入らなければ 7.7)
TRIPOD_INSERT_DEPTH = TRIPOD_SCREW_LEN + 1.5   # 止まり穴の深さ 8.5 (ねじが底突きしない)
TRIPOD_INSERT_WALL = 3.3       # 穴まわりの最小肉厚
TRIPOD_INSERT_FLOOR = 1.0      # 穴底に残す板厚 (基板側へ貫通させない)
assert TRIPOD_INSERT_DEPTH >= TRIPOD_INSERT_L + 0.5, "1/4 インサート穴が浅すぎる"
COVER_T = TRIPOD_INSERT_DEPTH + TRIPOD_INSERT_FLOOR   # 板厚 9.5 (インサートとねじが入る分だけ厚くする)
LIP_H = 3.5              # 嵌合リップ高さ (1.5 -> 3.5: 溝の上に受け棚を残すため)
LIP_T = 2.0              # リップ厚
LIP_CLR = 0.15           # リップ外面と本体内壁の片側隙間
SNAP_LEN = 12.0          # スナップ突起の長さ (左右壁、Y 方向)
SNAP_PROUD = 0.8         # 突起の出っ張り (0.45 -> 0.8)
SNAP_H = 1.6             # 突起の高さ (Z)。下側 SNAP_PROUD 分は 45° の導入テーパ
GROOVE_DEPTH = 0.9       # 本体内壁の受け溝深さ (0.5 -> 0.9)
# 溝の上に残る受け棚の厚さ。旧設計は 0.3 (ほぼ 1 層) しか無く、これが抜けやすさの原因
LEDGE_T = LIP_H - 0.1 - (SNAP_H + 0.3)
assert LEDGE_T >= 1.0, f"受け棚が薄すぎる: {LEDGE_T:.2f}"
assert SNAP_PROUD <= GROOVE_DEPTH + LIP_CLR, "突起が溝に収まらない"
assert M2_INSERT_DEPTH >= M2_INSERT_L + 0.5 and M2_INSERT_DEPTH <= STANDOFF, "M2 インサート穴の深さが不正"
assert BOARD / 2 - NOTCH_FROM_EDGE >= TRIPOD_INSERT_HOLE_D / 2 + TRIPOD_INSERT_WALL,     "ケーブル切り欠きが 1/4 インサート穴に近すぎる"

# --- 基板押さえ (裏蓋の柱。ねじを使わない場合に基板をボスとの間に挟む) ---
BOARD_PRESS = False      # 柱を付ける (M2 ねじ止めではねじ頭と干渉するので無効)
PRESS_POST_D = 3.5       # 柱の直径 (取付穴まわりのランドを押す)
PRESS_INTERF = 0.15      # 押し込み量 (スナップの遊び 0.2mm 以内)
PRESS_PIN = False        # 柱の先に基板穴へ入る位置決めピンを付ける
PRESS_PIN_D = 1.6        #   (穴ピッチ HOLE_PITCH が推定値なので既定は無効)
PRESS_PIN_LEN = 2.5

LIP_OUT = INNER - 2 * LIP_CLR
LIP_IN = LIP_OUT - 2 * LIP_T

OUT_DIR = Path(__file__).with_name("output")


# ---------------------------------------------------------------------------
# 補助
# ---------------------------------------------------------------------------
def vent_cutter(xs, height: float, width: float = VENT_SLOT_W) -> Part:
    """縦長スロット列のカッター。ローカル XY に作り (Y がスロット長手)、
    Z 方向に壁を貫通する厚みで押し出す。"""
    with BuildSketch() as sk:
        with Locations(*[(x, 0) for x in xs]):
            SlotCenterToCenter(height - width, width, rotation=90)
    with BuildPart() as cutter:
        add(sk.sketch)
        extrude(amount=WALL + 0.6, both=True)
    return cutter.part


def place(part: Part, x: float, y: float) -> Part:
    """部品の XY 中心を (x, y) に、底面を Z=0 に移す (3MF の配置用)。"""
    bb = part.bounding_box()
    c = bb.center()
    return part.moved(Location((x - c.X, y - c.Y, -bb.min.Z)))


# ---------------------------------------------------------------------------
# 1. 本体 housing
# ---------------------------------------------------------------------------
def build_housing() -> Part:
    with BuildPart() as hp:
        # 外形ボックス (前面 Z=0, 背面 Z=DEPTH)
        Box(OUTER, OUTER, DEPTH, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(hp.edges().filter_by(Axis.Z), CORNER_R)

        # 前面外周の面取り
        try:
            chamfer(hp.faces().sort_by(Axis.Z)[0].edges(), FRONT_CHAMFER)
        except Exception:
            pass

        # 内部キャビティ (基板が入る空間)
        with BuildSketch(Plane.XY.offset(FRONT_T)):
            RectangleRounded(INNER, INNER, 0.8)
        extrude(amount=DEPTH, mode=Mode.SUBTRACT)

        # 背面開口の内側エッジ面取り (裏蓋リップの導入)
        try:
            back = hp.faces().sort_by(Axis.Z)[-1]
            chamfer(back.inner_wires()[0].edges(), LEAD_IN)
        except Exception as e:
            print("lead-in chamfer skipped:", e)

        # M2 インサート用ボス (前面板内面から STANDOFF の高さ)
        with BuildSketch(Plane.XY.offset(FRONT_T)):
            with Locations((HOLE_OFF, HOLE_OFF), (-HOLE_OFF, HOLE_OFF),
                           (HOLE_OFF, -HOLE_OFF), (-HOLE_OFF, -HOLE_OFF)):
                Circle(BOSS_D / 2)
        extrude(amount=STANDOFF)
        # M2 インサートの下穴 (基板側から熱圧入。前面板は貫通させない)
        with BuildSketch(Plane.XY.offset(BOARD_Z)):
            with Locations((HOLE_OFF, HOLE_OFF), (-HOLE_OFF, HOLE_OFF),
                           (HOLE_OFF, -HOLE_OFF), (-HOLE_OFF, -HOLE_OFF)):
                Circle(M2_INSERT_HOLE_D / 2)
        extrude(amount=-M2_INSERT_DEPTH, mode=Mode.SUBTRACT)

        # レンズ開口
        with BuildSketch(Plane.XY):
            RectangleRounded(LENS_OPEN, LENS_OPEN, LENS_OPEN_R)
        extrude(amount=FRONT_T + 0.1, both=True, mode=Mode.SUBTRACT)

        # 裏蓋スナップ受け溝 (左右内壁)。溝の上に LEDGE_T の受け棚が残る
        groove_zc = DEPTH - LIP_H + 0.1 + (SNAP_H + 0.3) / 2
        for sx in (-1, 1):
            with Locations((sx * (INNER / 2 + GROOVE_DEPTH / 2 - 0.01), 0, groove_zc)):
                Box(GROOVE_DEPTH + 0.02, SNAP_LEN + 1.0, SNAP_H + 0.3, mode=Mode.SUBTRACT)

        # 上壁ケーブルスリット
        if CABLE_WALL_SLOT:
            with Locations((CONN_X, OUTER / 2 - WALL / 2, DEPTH - CABLE_SLOT_D / 2 + 0.5)):
                Box(CABLE_SLOT_W, WALL + 2.0, CABLE_SLOT_D + 1.0, mode=Mode.SUBTRACT)

        # 通気スロット (上壁 + 左右壁)
        if VENTS:
            z_lo = FRONT_T + 2.0
            z_hi = DEPTH - LIP_H - 0.5
            zc = (z_lo + z_hi) / 2
            h = z_hi - z_lo - 1.0
            # 上壁 (+Y): ローカル X->X, ローカル Y->Z
            top = vent_cutter(VENT_TOP_XS, h)
            add(top.rotate(Axis.X, 90).moved(Location((0, OUTER / 2, zc))), mode=Mode.SUBTRACT)
            # 左右壁 (±X): ローカル X->Y, ローカル Y->Z
            side = vent_cutter(VENT_SIDE_XS, h)
            side = side.rotate(Axis.X, 90).rotate(Axis.Z, 90)
            for sx in (-1, 1):
                add(side.moved(Location((sx * OUTER / 2, 0, zc))), mode=Mode.SUBTRACT)

    return hp.part


# ---------------------------------------------------------------------------
# 2. 裏蓋 cover (本体座標で作成: 板は Z=DEPTH..DEPTH+COVER_T、リップは本体内へ。印刷用に後で裏返す)
# ---------------------------------------------------------------------------
def build_cover() -> Part:
    notch_w = max(NOTCH_W, CONN_W + 2 * CONN_CLR)
    notch_y0 = min(BOARD / 2 - NOTCH_FROM_EDGE,
                   BOARD / 2 - CONN_FROM_EDGE - CONN_D / 2 - CONN_CLR)
    with BuildPart() as cp:
        # 板
        Box(OUTER, OUTER, COVER_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(cp.edges().filter_by(Axis.Z), CORNER_R)
        chamfer(cp.faces().sort_by(Axis.Z)[-1].edges(), FRONT_CHAMFER)
        # リップ (板の下、本体内壁に沿う枠)
        with BuildSketch(Plane.XY):
            RectangleRounded(LIP_OUT, LIP_OUT, 0.8 - LIP_CLR)
            RectangleRounded(LIP_IN, LIP_IN, 0.5, mode=Mode.SUBTRACT)
        extrude(amount=-LIP_H)
        # スナップ突起 (左右、リップ先端寄り。下側 SNAP_PROUD 分は 45° テーパ、上面は垂直の掛かり面)
        z_tip = -LIP_H
        for sx in (-1, 1):
            x0 = sx * LIP_OUT / 2
            pts = [
                (x0 - sx * 0.3, z_tip + 0.2),
                (x0 + sx * SNAP_PROUD, z_tip + 0.2 + SNAP_PROUD),
                (x0 + sx * SNAP_PROUD, z_tip + 0.2 + SNAP_H),
                (x0 - sx * 0.3, z_tip + 0.2 + SNAP_H),
            ]
            with BuildSketch(Plane.XZ):
                Polygon(*pts, align=None)
            extrude(amount=SNAP_LEN / 2, both=True)
        # ケーブル切り欠き (コネクタ直上から上端まで)
        with Locations((0.0, (notch_y0 + OUTER / 2 + 1) / 2, 0)):
            Box(notch_w, OUTER / 2 + 1 - notch_y0, 2 * (COVER_T + LIP_H + 1), mode=Mode.SUBTRACT)
        # 1/4"-20 インサートナットの下穴 (外面中央から止まり穴。外面側から熱圧入する)
        with BuildSketch(Plane.XY.offset(COVER_T)):
            Circle(TRIPOD_INSERT_HOLE_D / 2)
        extrude(amount=-TRIPOD_INSERT_DEPTH, mode=Mode.SUBTRACT)
        # 基板押さえの柱 (板の内面 Z=0 から基板裏面まで + 押し込み量)
        if BOARD_PRESS:
            post_len = DEPTH - (BOARD_Z + BOARD_T) + PRESS_INTERF
            corners = [(sx * HOLE_OFF, sy * HOLE_OFF) for sx in (-1, 1) for sy in (-1, 1)]
            with BuildSketch(Plane.XY):
                with Locations(*corners):
                    Circle(PRESS_POST_D / 2)
            extrude(amount=-post_len)
            if PRESS_PIN:
                with BuildSketch(Plane.XY.offset(-post_len)):
                    with Locations(*corners):
                        Circle(PRESS_PIN_D / 2)
                extrude(amount=-PRESS_PIN_LEN)
    return cp.part.moved(Location((0, 0, DEPTH)))


# ---------------------------------------------------------------------------
# 部品の生成
# ---------------------------------------------------------------------------
housing = build_housing()
cover = build_cover()
# 印刷向きの部品 (housing はそのまま、cover は裏返して外面を Z=0 に)
housing_print = housing
cover_print = cover.rotate(Axis.Y, 180).moved(Location((0, 0, DEPTH + COVER_T)))
if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    export_stl(housing_print, str(OUT_DIR / "housing.stl"))
    export_stl(cover_print, str(OUT_DIR / "cover.stl"))
    export_step(housing_print, str(OUT_DIR / "housing.step"))
    export_step(cover_print, str(OUT_DIR / "cover.step"))
    # 全部品を並べた 3MF (Bambu Studio にそのまま読み込める)
    m = Mesher()
    m.add_shape([
        place(housing_print, -35, 10),
        place(cover_print, 25, 10),
    ], part_number="webcamera_holder")
    m.write(str(OUT_DIR / "webcamera_holder.3mf"))
    print("exported to", OUT_DIR)

    if show is not None and not os.environ.get("NO_SHOW"):
        try:
            # 印刷向きの部品
            show(
                housing_print,
                cover_print.moved(Location((60, 10, 0))),
                names=["housing", "cover"],
                colors=["lightblue", "gray"],
            )
        except Exception as e:  # viewer 未起動など
            print("show() skipped:", e)
