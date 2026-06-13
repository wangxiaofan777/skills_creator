# -*- coding: utf-8 -*-
"""一次性生成黑客松提交用的配图(PIL 直接出 PNG,中文用微软雅黑)。"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

REG = r"C:\Windows\Fonts\msyh.ttc"
BLD = r"C:\Windows\Fonts\msyhbd.ttc"
OUT = os.path.dirname(os.path.abspath(__file__))

C = {
    "bg": "#f4f7fb", "card": "#ffffff", "ink": "#0f172a", "sub": "#475569",
    "line": "#cbd5e1", "blue": "#2563eb", "blued": "#1e3a8a", "navy": "#0b1733",
    "green": "#16a34a", "amber": "#d97706", "red": "#dc2626",
    "BLOCKER": "#cf222e", "CRITICAL": "#bc4c00", "MAJOR": "#9a6700",
    "MINOR": "#0969da", "INFO": "#57606a", "chip": "#eaf1ff", "chipink": "#1e40af",
}


def f(sz, bold=False):
    return ImageFont.truetype(BLD if bold else REG, sz)


def box(d, xy, r, fill, outline=None, w=2):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)


def t(d, pos, s, font, fill, anchor="lm"):
    d.text(pos, s, font=font, fill=fill, anchor=anchor)


def arrow(d, p1, p2, color, w=6, head=18):
    d.line([p1, p2], fill=color, width=w)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    for a in (ang + math.radians(152), ang - math.radians(152)):
        d.line([p2, (p2[0] + head * math.cos(a), p2[1] + head * math.sin(a))],
               fill=color, width=w)


def canvas(w, h, bg="bg"):
    im = Image.new("RGB", (w, h), C[bg])
    return im, ImageDraw.Draw(im)


def header(d, w, title, sub):
    box(d, (0, 0, w, 96), 0, C["navy"])
    box(d, (40, 34, 64, 62), 6, C["blue"])
    t(d, (80, 48), title, f(34, True), "#ffffff")
    t(d, (w - 40, 56), sub, f(20), "#9fb3d1", anchor="rm")


def chip(d, x, y, s, pad=16, fg="chipink", bg="chip"):
    tw = d.textlength(s, font=f(20))
    box(d, (x, y, x + tw + pad * 2, y + 40), 20, C[bg])
    t(d, (x + pad, y + 20), s, f(20), C[fg])
    return x + tw + pad * 2


# --------------------------------------------------------------------------- #
def img_architecture():
    w, h = 1480, 840
    im, d = canvas(w, h)
    header(d, w, "SonarGuard · 架构与数据流", "Agent · MCP · 开放 API")

    # 数据源
    box(d, (40, 150, 300, 300), 16, C["card"], C["line"], 2)
    t(d, (170, 188), "SonarQube 服务器", f(24, True), C["ink"], "mm")
    t(d, (170, 226), "开放 API", f(22), C["blue"], "mm")
    t(d, (170, 262), "拉取规则 + 存量 issue", f(18), C["sub"], "mm")

    box(d, (40, 330, 300, 430), 16, "#fff7ed", "#fdba74", 2)
    t(d, (170, 362), "离线 fallback", f(22, True), C["amber"], "mm")
    t(d, (170, 398), "服务器3秒超时→内置规则", f(17), C["sub"], "mm")

    # 管线
    cols = [
        (360, "sonar_api.py", ["开放API封装", "JSON 机器契约"], C["blue"]),
        (700, "scan.py", ["--format", "md / html / json"], C["blued"]),
        (1040, "render.py", ["零依赖渲染", "确定性截断"], "#0e7490"),
    ]
    cy = 200
    for x, name, lines, col in cols:
        box(d, (x, cy, x + 260, cy + 150), 16, C["card"], C["line"], 2)
        box(d, (x, cy, x + 260, cy + 46), 16, col)
        box(d, (x, cy + 30, x + 260, cy + 46), 0, col)
        t(d, (x + 130, cy + 23), name, f(23, True), "#ffffff", "mm")
        for i, ln in enumerate(lines):
            t(d, (x + 130, cy + 80 + i * 30), ln, f(19), C["sub"], "mm")
    arrow(d, (300, cy + 75), (358, cy + 75), C["blue"])
    arrow(d, (620, cy + 75), (698, cy + 75), C["blue"])
    arrow(d, (960, cy + 75), (1038, cy + 75), C["blue"])

    # check_staged 分支
    box(d, (700, 430, 960, 560), 16, C["card"], C["line"], 2)
    box(d, (700, 430, 960, 476), 16, "#7c3aed")
    box(d, (700, 460, 960, 476), 0, "#7c3aed")
    t(d, (830, 453), "check_staged.py", f(21, True), "#ffffff", "mm")
    t(d, (830, 506), "pre-commit 钩子", f(19), C["sub"], "mm")
    t(d, (830, 536), "彩色拦截/警告 · 退出码", f(17), C["sub"], "mm")
    arrow(d, (830, cy + 150), (830, 428), "#7c3aed")

    # 输出
    box(d, (1040, 430, 1440, 620), 16, "#f0fdf4", "#86efac", 2)
    t(d, (1240, 462), "输出", f(22, True), C["green"], "mm")
    outs = ["对话框 Markdown 报告", ".sonarguard/reports/ 时间戳归档",
            "HTML 自动浏览器打开"]
    for i, o in enumerate(outs):
        t(d, (1070, 506 + i * 34), "• " + o, f(19), C["ink"], "lm")
    arrow(d, (1170, cy + 150), (1170, 428), C["green"])

    # /sonar-scan 徽标
    box(d, (360, 470, 660, 560), 18, C["navy"])
    t(d, (510, 500), "/sonar-scan", f(26, True), "#ffffff", "mm")
    t(d, (510, 532), "对话框一键扫描", f(18), "#9fb3d1", "mm")
    arrow(d, (510, 470), (700, 360), C["blued"])

    t(d, (40, 800), "三端统一:Claude Code / Cursor / Codex 共用同一引擎 · 仅标准库零依赖",
      f(20), C["sub"], "lm")
    im.save(os.path.join(OUT, "01-architecture.png"))


def img_two_stage():
    w, h = 1480, 640
    im, d = canvas(w, h)
    header(d, w, "SonarGuard · 两阶段守卫", "质量左移:把上线前救火变成提交前拦截")

    base = 430
    arrow(d, (60, base), (1430, base), C["line"], w=6, head=0)
    stops = [(160, "写代码"), (560, "git add"), (900, "git commit"), (1300, "CI / 上线")]
    for x, lbl in stops:
        d.ellipse((x - 12, base - 12, x + 12, base + 12), fill=C["blue"])
        t(d, (x, base + 40), lbl, f(22, True), C["ink"], "mm")

    # 阶段1
    box(d, (90, 180, 470, 360), 18, "#eff6ff", C["blue"], 2)
    t(d, (280, 218), "① 开发阶段", f(24, True), C["blued"], "mm")
    t(d, (280, 258), "对话内实时审查", f(21), C["ink"], "mm")
    t(d, (280, 296), "每次写完/改完即对照", f(17), C["sub"], "mm")
    t(d, (280, 322), "Sonar 规则审查变更", f(17), C["sub"], "mm")
    arrow(d, (200, 360), (170, base - 16), C["blue"])

    # 阶段2
    box(d, (720, 180, 1100, 360), 18, "#f5f3ff", "#7c3aed", 2)
    t(d, (910, 218), "② 提交阶段", f(24, True), "#6d28d9", "mm")
    t(d, (910, 258), "pre-commit 拦截", f(21), C["ink"], "mm")
    t(d, (910, 296), "暂存区文件按风险", f(17), C["sub"], "mm")
    t(d, (910, 322), "拦截 / 警告", f(17), C["sub"], "mm")
    arrow(d, (910, 360), (900, base - 16), "#7c3aed")

    box(d, (60, 520, 1420, 600), 16, C["navy"])
    t(d, (740, 560), "开发当下就拦截,而不是等 CI 才暴露 —— 治理 AI 生成代码的隐性债务",
      f(22, True), "#ffffff", "mm")
    im.save(os.path.join(OUT, "02-two-stage.png"))


def img_report():
    w, h = 1280, 920
    im, d = canvas(w, h)
    header(d, w, "SonarGuard · 报告样例", "脚本确定性生成 · md / html / json")

    box(d, (40, 130, 1240, 880), 18, C["card"], C["line"], 2)
    box(d, (40, 130, 1240, 188), 18, "#0b1733")
    box(d, (40, 170, 1240, 188), 0, "#0b1733")
    for i, col in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        d.ellipse((70 + i * 26, 150, 70 + i * 26 + 16, 166), fill=col)
    t(d, (170, 159), "Sonar 合规检查报告 — 全项目(模式: 服务器)", f(22, True),
      "#ffffff", "lm")

    # 汇总
    t(d, (70, 226), "严重级汇总", f(24, True), C["ink"], "lm")
    t(d, (1210, 226), "合计 11", f(22, True), C["sub"], "rm")
    sev = [("BLOCKER", 1), ("CRITICAL", 0), ("MAJOR", 2), ("MINOR", 5), ("INFO", 3)]
    x = 70
    for name, n in sev:
        box(d, (x, 256, x + 210, 330), 12, "#f8fafc", C["line"], 1)
        box(d, (x, 256, x + 10, 330), 12, C[name])
        t(d, (x + 30, 286), name, f(19, True), C[name], "lm")
        t(d, (x + 180, 294), str(n), f(30, True), C["ink"], "mm")
        x += 226

    # 明细
    t(d, (70, 372), "问题明细", f(24, True), C["ink"], "lm")
    cols = [(70, "严重级"), (260, "文件:行"), (560, "规则"), (820, "问题"), (1120, "风险")]
    for cx, lbl in cols:
        t(d, (cx, 416), lbl, f(19, True), C["sub"], "lm")
    d.line((70, 442, 1210, 442), fill=C["line"], width=2)
    rows = [
        ("BLOCKER", "Login.java:42", "java:S4973", "字符串用 == 比较", "red"),
        ("MAJOR", "Order.java:88", "java:S106", "System.out 调试输出", "amber"),
        ("MAJOR", "utils.py:13", "python:S5754", "裸 except 吞异常", "amber"),
        ("MINOR", "app.ts:7", "javascript:S1440", "应使用 ===", "green"),
    ]
    y = 470
    for sevn, loc, rule, msg, risk in rows:
        box(d, (70, y, 230, y + 40), 10, C[sevn])
        t(d, (150, y + 20), sevn, f(18, True), "#ffffff", "mm")
        t(d, (260, y + 20), loc, f(19), C["ink"], "lm")
        t(d, (560, y + 20), rule, f(19), C["sub"], "lm")
        t(d, (820, y + 20), msg, f(19), C["ink"], "lm")
        rc = {"red": C["red"], "amber": C["amber"], "green": C["green"]}[risk]
        d.ellipse((1120, y + 8, 1144, y + 32), fill=rc)
        y += 64

    box(d, (70, 760, 1210, 850), 14, "#f1f5f9")
    t(d, (96, 788), "修复风险分级", f(20, True), C["ink"], "lm")
    rx = 96
    for txt_, col in [("🟢 可直接修", C["green"]), ("🟡 修后跑测试", C["amber"]),
                      ("🔴 需确认再动", C["red"])]:
        d.ellipse((rx, 818, rx + 18, 836), fill=col)
        t(d, (rx + 28, 827), txt_[2:], f(19), C["ink"], "lm")
        rx += 360
    im.save(os.path.join(OUT, "03-report-sample.png"))


def img_platforms():
    w, h = 1280, 680
    im, d = canvas(w, h)
    header(d, w, "SonarGuard · 三端统一", "装一次,全员受益")

    plats = [("Claude Code", C["blue"]), ("Cursor", "#7c3aed"), ("Codex", "#0e7490")]
    x = 90
    for name, col in plats:
        box(d, (x, 160, x + 340, 300), 16, C["card"], C["line"], 2)
        box(d, (x, 160, x + 340, 210), 16, col)
        box(d, (x, 194, x + 340, 210), 0, col)
        t(d, (x + 170, 185), name, f(24, True), "#ffffff", "mm")
        t(d, (x + 170, 252), "同一规则与工作流", f(19), C["sub"], "mm")
        arrow(d, (x + 170, 300), (640, 380), col)
        x += 380

    box(d, (340, 380, 940, 480), 18, C["navy"])
    t(d, (640, 415), "统一规则引擎", f(26, True), "#ffffff", "mm")
    t(d, (640, 452), "服务器模式 + 离线 fallback", f(19), "#9fb3d1", "mm")

    y = 540
    x = 90
    for s in ["服务器真实规则", "离线高置信启发式", "风险分级·三档",
              "零依赖 · 秒级", "token 不入库"]:
        x = chip(d, x, y, s) + 18
    im.save(os.path.join(OUT, "04-platforms.png"))


for fn in (img_architecture, img_two_stage, img_report, img_platforms):
    fn()
print("done:", sorted(p for p in os.listdir(OUT) if p.endswith(".png")))
