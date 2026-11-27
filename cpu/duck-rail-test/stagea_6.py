# POOL HARNESS-FIT PROBE v2 (M586/M589): model-free. Gold-apply + targeted pytest for 2725/3296/3454.
# No rail, no secrets, no model calls. Deterministic: same tarball + same diffs = same result.
# Two-phase per task: test-only apply -> pytest (expect FAIL = base-fail proof), then fix apply -> pytest (expect PASS).
# Ends: TEST-RESULT per task + {pid}.pytest.txt + {pid}.applied.txt in OUT_DIR (/tmp/duck6_out).
import os, subprocess, urllib.request, base64
OUT_DIR = "/tmp/duck6_out"
os.makedirs(OUT_DIR, exist_ok=True)
TASKS = {
  "rich_2725": {
    "repo": "Textualize/rich",
    "base": "577def22dd83",
    "pytest": "tests/test_table.py",
    "k": "test_placement_table_box_elements",
    "src": "rich/table.py",
    "fixB64": "LS0tIGEvcmljaC90YWJsZS5weQorKysgYi9yaWNoL3RhYmxlLnB5CkBAIC03NzUsMTYgKzc3NSwxNiBAQAogICAgICAgICAgICAgICAgICAgICBfU2VnbWVudChfYm94LmhlYWRfcmlnaHQsIGJvcmRlcl9zdHlsZSksCiAgICAgICAgICAgICAgICAgICAgIF9TZWdtZW50KF9ib3guaGVhZF92ZXJ0aWNhbCwgYm9yZGVyX3N0eWxlKSwKICAgICAgICAgICAgICAgICApLAogICAgICAgICAgICAgICAgICgKKyAgICAgICAgICAgICAgICAgICAgX1NlZ21lbnQoX2JveC5taWRfbGVmdCwgYm9yZGVyX3N0eWxlKSwKKyAgICAgICAgICAgICAgICAgICAgX1NlZ21lbnQoX2JveC5taWRfcmlnaHQsIGJvcmRlcl9zdHlsZSksCisgICAgICAgICAgICAgICAgICAgIF9TZWdtZW50KF9ib3gubWlkX3ZlcnRpY2FsLCBib3JkZXJfc3R5bGUpLAorICAgICAgICAgICAgICAgICksCisgICAgICAgICAgICAgICAgKAogICAgICAgICAgICAgICAgICAgICBfU2VnbWVudChfYm94LmZvb3RfbGVmdCwgYm9yZGVyX3N0eWxlKSwKICAgICAgICAgICAgICAgICAgICAgX1NlZ21lbnQoX2JveC5mb290X3JpZ2h0LCBib3JkZXJfc3R5bGUpLAogICAgICAgICAgICAgICAgICAgICBfU2VnbWVudChfYm94LmZvb3RfdmVydGljYWwsIGJvcmRlcl9zdHlsZSksCiAgICAgICAgICAgICAgICAgKSwKLSAgICAgICAgICAgICAgICAoCi0gICAgICAgICAgICAgICAgICAgIF9TZWdtZW50KF9ib3gubWlkX2xlZnQsIGJvcmRlcl9zdHlsZSksCi0gICAgICAgICAgICAgICAgICAgIF9TZWdtZW50KF9ib3gubWlkX3JpZ2h0LCBib3JkZXJfc3R5bGUpLAotICAgICAgICAgICAgICAgICAgICBfU2VnbWVudChfYm94Lm1pZF92ZXJ0aWNhbCwgYm9yZGVyX3N0eWxlKSwKLSAgICAgICAgICAgICAgICApLAogICAgICAgICAgICAgXQogICAgICAgICAgICAgaWYgc2hvd19lZGdlOgogICAgICAgICAgICAgICAgIHlpZWxkIF9TZWdtZW50KF9ib3guZ2V0X3RvcCh3aWR0aHMpLCBib3JkZXJfc3R5bGUpCg==",
    "testB64": "LS0tIGEvdGVzdHMvdGVzdF90YWJsZS5weQorKysgYi90ZXN0cy90ZXN0X3RhYmxlLnB5CkBAIC0xLDYgKzEsNyBAQAogIyBlbmNvZGluZz11dGYtOAogCiBpbXBvcnQgaW8KK2Zyb20gdGV4dHdyYXAgaW1wb3J0IGRlZGVudAogCiBpbXBvcnQgcHl0ZXN0CiAKQEAgLTIzNCw2ICsyMzUsMTM0IEBAIGRlZiB0ZXN0X3NlY3Rpb24oKToKICAgICBhc3NlcnQgb3V0cHV0ID09IGV4cGVjdGVkCiAKIAorQHB5dGVzdC5tYXJrLnBhcmFtZXRyaXplKAorICAgICJzaG93X2hlYWRlcixzaG93X2Zvb3RlcixleHBlY3RlZCIsCisgICAgWworICAgICAgICAoCisgICAgICAgICAgICBGYWxzZSwKKyAgICAgICAgICAgIEZhbHNlLAorICAgICAgICAgICAgZGVkZW50KAorICAgICAgICAgICAgICAgICIiIgorICAgICAgICAgICAgICAgIGFiYmJiYmNiYmJiYmJiYmJjYmJiYmNiYmJiYmQKKyAgICAgICAgICAgICAgICAxRGVjICAyU2t5d2Fsa2VyMjI3NU0yMzc1TSAzCisgICAgICAgICAgICAgICAgNE1heSAgNVNvbG8gICAgIDUyNzVNNTM5M00gNgorICAgICAgICAgICAgICAgIGlqampqamtqampqampqamprampqamtqampqamwKKyAgICAgICAgICAgICAgICA3RGVjICA4TGFzdCBKZWRpODI2Mk04MTMzM005CisgICAgICAgICAgICAgICAgcXJycnJyc3JycnJycnJycnNycnJyc3JycnJydAorICAgICAgICAgICAgICAgICIiIgorICAgICAgICAgICAgKS5sc3RyaXAoKSwKKyAgICAgICAgKSwKKyAgICAgICAgKAorICAgICAgICAgICAgVHJ1ZSwKKyAgICAgICAgICAgIEZhbHNlLAorICAgICAgICAgICAgZGVkZW50KAorICAgICAgICAgICAgICAgICIiIgorICAgICAgICAgICAgICAgIGFiYmJiYmNiYmJiYmJiYmJjYmJiYmNiYmJiYmQKKyAgICAgICAgICAgICAgICAxTW9udGgyTmlja25hbWUgMkNvc3QyR3Jvc3MzCisgICAgICAgICAgICAgICAgZWZmZmZmZ2ZmZmZmZmZmZmdmZmZmZ2ZmZmZmaAorICAgICAgICAgICAgICAgIDREZWMgIDVTa3l3YWxrZXI1Mjc1TTUzNzVNIDYKKyAgICAgICAgICAgICAgICA0TWF5ICA1U29sbyAgICAgNTI3NU01MzkzTSA2CisgICAgICAgICAgICAgICAgaWpqampqa2pqampqampqamtqampqa2pqampqbAorICAgICAgICAgICAgICAgIDdEZWMgIDhMYXN0IEplZGk4MjYyTTgxMzMzTTkKKyAgICAgICAgICAgICAgICBxcnJycnJzcnJycnJycnJyc3JycnJzcnJycnJ0CisgICAgICAgICAgICAgICAgIiIiCisgICAgICAgICAgICApLmxzdHJpcCgpLAorICAgICAgICApLAorICAgICAgICAoCisgICAgICAgICAgICBGYWxzZSwKKyAgICAgICAgICAgIFRydWUsCisgICAgICAgICAgICBkZWRlbnQoCisgICAgICAgICAgICAgICAgIiIiCisgICAgICAgICAgICAgICAgYWJiYmJiY2JiYmJiYmJiYmNiYmJiY2JiYmJiZAorICAgICAgICAgICAgICAgIDFEZWMgIDJTa3l3YWxrZXIyMjc1TTIzNzVNIDMKKyAgICAgICAgICAgICAgICA0TWF5ICA1U29sbyAgICAgNTI3NU01MzkzTSA2CisgICAgICAgICAgICAgICAgaWpqampqa2pqampqampqamtqampqa2pqampqbAorICAgICAgICAgICAgICAgIDREZWMgIDVMYXN0IEplZGk1MjYyTTUxMzMzTTYKKyAgICAgICAgICAgICAgICBtbm5ubm5vbm5ubm5ubm5ub25ubm5vbm5ubm5wCisgICAgICAgICAgICAgICAgN01PTlRIOE5JQ0tOQU1FIDhDT1NUOEdST1NTOQorICAgICAgICAgICAgICAgIHFycnJycnNycnJycnJycnJzcnJycnNycnJycnQKKyAgICAgICAgICAgICAgICAiIiIKKyAgICAgICAgICAgICkubHN0cmlwKCksCisgICAgICAgICksCisgICAgICAgICgKKyAgICAgICAgICAgIFRydWUsCisgICAgICAgICAgICBUcnVlLAorICAgICAgICAgICAgZGVkZW50KAorICAgICAgICAgICAgICAgICIiIgorICAgICAgICAgICAgICAgIGFiYmJiYmNiYmJiYmJiYmJjYmJiYmNiYmJiYmQKKyAgICAgICAgICAgICAgICAxTW9udGgyTmlja25hbWUgMkNvc3QyR3Jvc3MzCisgICAgICAgICAgICAgICAgZWZmZmZmZ2ZmZmZmZmZmZmdmZmZmZ2ZmZmZmaAorICAgICAgICAgICAgICAgIDREZWMgIDVTa3l3YWxrZXI1Mjc1TTUzNzVNIDYKKyAgICAgICAgICAgICAgICA0TWF5ICA1U29sbyAgICAgNTI3NU01MzkzTSA2CisgICAgICAgICAgICAgICAgaWpqampqa2pqampqampqamtqampqa2pqampqbAorICAgICAgICAgICAgICAgIDREZWMgIDVMYXN0IEplZGk1MjYyTTUxMzMzTTYKKyAgICAgICAgICAgICAgICBtbm5ubm5vbm5ubm5ubm5ub25ubm5vbm5ubm5wCisgICAgICAgICAgICAgICAgN01PTlRIOE5JQ0tOQU1FIDhDT1NUOEdST1NTOQorICAgICAgICAgICAgICAgIHFycnJycnNycnJycnJycnJzcnJycnNycnJycnQKKyAgICAgICAgICAgICAgICAiIiIKKyAgICAgICAgICAgICkubHN0cmlwKCksCisgICAgICAgICksCisgICAgXSwKKykKK2RlZiB0ZXN0X3BsYWNlbWVudF90YWJsZV9ib3hfZWxlbWVudHMoc2hvd19oZWFkZXIsIHNob3dfZm9vdGVyLCBleHBlY3RlZCk6CisgICAgIiIiRW5zdXJlIGJveCBkcmF3aW5nIGNoYXJhY3RlcnMgY29ycmVjdGx5IHBvc2l0aW9uZWQuIiIiCisKKyAgICB0YWJsZSA9IFRhYmxlKAorICAgICAgICBib3g9Ym94LkFTQ0lJLCBzaG93X2hlYWRlcj1zaG93X2hlYWRlciwgc2hvd19mb290ZXI9c2hvd19mb290ZXIsIHBhZGRpbmc9MAorICAgICkKKworICAgICMgY29udGVudCByb3dzIGluZGljYXRlZCBieSBudW1lcmFscywgcHVyZSBkaXZpZGVycyBieSBsZXR0ZXJzCisgICAgdGFibGUuYm94Ll9fZGljdF9fLnVwZGF0ZSgKKyAgICAgICAgdG9wX2xlZnQ9ImEiLAorICAgICAgICB0b3A9ImIiLAorICAgICAgICB0b3BfZGl2aWRlcj0iYyIsCisgICAgICAgIHRvcF9yaWdodD0iZCIsCisgICAgICAgIGhlYWRfbGVmdD0iMSIsCisgICAgICAgIGhlYWRfdmVydGljYWw9IjIiLAorICAgICAgICBoZWFkX3JpZ2h0PSIzIiwKKyAgICAgICAgaGVhZF9yb3dfbGVmdD0iZSIsCisgICAgICAgIGhlYWRfcm93X2hvcml6b250YWw9ImYiLAorICAgICAgICBoZWFkX3Jvd19jcm9zcz0iZyIsCisgICAgICAgIGhlYWRfcm93X3JpZ2h0PSJoIiwKKyAgICAgICAgbWlkX2xlZnQ9IjQiLAorICAgICAgICBtaWRfdmVydGljYWw9IjUiLAorICAgICAgICBtaWRfcmlnaHQ9IjYiLAorICAgICAgICByb3dfbGVmdD0iaSIsCisgICAgICAgIHJvd19ob3Jpem9udGFsPSJqIiwKKyAgICAgICAgcm93X2Nyb3NzPSJrIiwKKyAgICAgICAgcm93X3JpZ2h0PSJsIiwKKyAgICAgICAgZm9vdF9sZWZ0PSI3IiwKKyAgICAgICAgZm9vdF92ZXJ0aWNhbD0iOCIsCisgICAgICAgIGZvb3RfcmlnaHQ9IjkiLAorICAgICAgICBmb290X3Jvd19sZWZ0PSJtIiwKKyAgICAgICAgZm9vdF9yb3dfaG9yaXpvbnRhbD0ibiIsCisgICAgICAgIGZvb3Rfcm93X2Nyb3NzPSJvIiwKKyAgICAgICAgZm9vdF9yb3dfcmlnaHQ9InAiLAorICAgICAgICBib3R0b21fbGVmdD0icSIsCisgICAgICAgIGJvdHRvbT0iciIsCisgICAgICAgIGJvdHRvbV9kaXZpZGVyPSJzIiwKKyAgICAgICAgYm90dG9tX3JpZ2h0PSJ0IiwKKyAgICApCisKKyAgICAjIGFkZCBjb250ZW50IC0gbm90ZSBoZWFkZXJzIHRpdGxlIGNhc2UsIGZvb3RlcnMgdXBwZXIgY2FzZQorICAgIHRhYmxlLmFkZF9jb2x1bW4oIk1vbnRoIiwgIk1PTlRIIiwgd2lkdGg9NSkKKyAgICB0YWJsZS5hZGRfY29sdW1uKCJOaWNrbmFtZSIsICJOSUNLTkFNRSIsIHdpZHRoPTkpCisgICAgdGFibGUuYWRkX2NvbHVtbigiQ29zdCIsICJDT1NUIiwgd2lkdGg9NCkKKyAgICB0YWJsZS5hZGRfY29sdW1uKCJHcm9zcyIsICJHUk9TUyIsIHdpZHRoPTUpCisKKyAgICB0YWJsZS5hZGRfcm93KCJEZWMiLCAiU2t5d2Fsa2VyIiwgIjI3NU0iLCAiMzc1TSIpCisgICAgdGFibGUuYWRkX3JvdygiTWF5IiwgIlNvbG8iLCAiMjc1TSIsICIzOTNNIikKKyAgICB0YWJsZS5hZGRfc2VjdGlvbigpCisgICAgdGFibGUuYWRkX3JvdygiRGVjIiwgIkxhc3QgSmVkaSIsICIyNjJNIiwgIjEzMzNNIikKKworICAgIGNvbnNvbGUgPSBDb25zb2xlKHJlY29yZD1UcnVlLCB3aWR0aD0yOCkKKyAgICBjb25zb2xlLnByaW50KHRhYmxlKQorICAgIG91dHB1dCA9IGNvbnNvbGUuZXhwb3J0X3RleHQoKQorICAgIHByaW50KHJlcHIob3V0cHV0KSkKKworICAgIGFzc2VydCBvdXRwdXQgPT0gZXhwZWN0ZWQKKworCiBpZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgIHJlbmRlciA9IHJlbmRlcl90YWJsZXMoKQogICAgIHByaW50KHJlbmRlcik=",
  },
  "rich_3296": {
    "repo": "Textualize/rich",
    "base": "0d7e598fe7ea",
    "pytest": "tests/test_syntax.py",
    "k": "test_background_color_override_includes_padding",
    "src": "rich/syntax.py",
    "fixB64": "ZGlmZiAtLWdpdCBhL3JpY2gvc3ludGF4LnB5IGIvcmljaC9zeW50YXgucHkKaW5kZXggZjNjZWZmNzU4ZS4uNGRhNmMzYjdhNiAxMDA2NDQKLS0tIGEvcmljaC9zeW50YXgucHkKKysrIGIvcmljaC9zeW50YXgucHkKQEAgLTYxOSw5ICs2MTksNyBAQCBkZWYgX19yaWNoX2NvbnNvbGVfXygKICAgICApIC0+IFJlbmRlclJlc3VsdDoKICAgICAgICAgc2VnbWVudHMgPSBTZWdtZW50cyhzZWxmLl9nZXRfc3ludGF4KGNvbnNvbGUsIG9wdGlvbnMpKQogICAgICAgICBpZiBzZWxmLnBhZGRpbmc6Ci0gICAgICAgICAgICB5aWVsZCBQYWRkaW5nKAotICAgICAgICAgICAgICAgIHNlZ21lbnRzLCBzdHlsZT1zZWxmLl90aGVtZS5nZXRfYmFja2dyb3VuZF9zdHlsZSgpLCBwYWQ9c2VsZi5wYWRkaW5nCi0gICAgICAgICAgICApCisgICAgICAgICAgICB5aWVsZCBQYWRkaW5nKHNlZ21lbnRzLCBzdHlsZT1zZWxmLl9nZXRfYmFzZV9zdHlsZSgpLCBwYWQ9c2VsZi5wYWRkaW5nKQogICAgICAgICBlbHNlOgogICAgICAgICAgICAgeWllbGQgc2VnbWVudHMKIAo=",
    "testB64": "ZGlmZiAtLWdpdCBhL3Rlc3RzL3Rlc3Rfc3ludGF4LnB5IGIvdGVzdHMvdGVzdF9zeW50YXgucHkKaW5kZXggMzdjYzI5M2ViNC4uYmJkNGM3YTVjYiAxMDA2NDQKLS0tIGEvdGVzdHMvdGVzdF9zeW50YXgucHkKKysrIGIvdGVzdHMvdGVzdF9zeW50YXgucHkKQEAgLTQwNiw2ICs0MDYsMjMgQEAgZGVmIHRlc3Rfc3ludGF4X21lYXN1cmUoKToKICAgICBhc3NlcnQgY29kZS5fX3JpY2hfbWVhc3VyZV9fKGNvbnNvbGUsIGNvbnNvbGUub3B0aW9ucykgPT0gTWVhc3VyZW1lbnQoMywgMjQpCiAKIAorZGVmIHRlc3RfYmFja2dyb3VuZF9jb2xvcl9vdmVycmlkZV9pbmNsdWRlc19wYWRkaW5nKCk6CisgICAgIiIiUmVncmVzc2lvbiB0ZXN0IGZvciBodHRwczovL2dpdGh1Yi5jb20vVGV4dHVhbGl6ZS9yaWNoL2lzc3Vlcy8zMjk1IiIiCisKKyAgICBzeW50YXggPSBTeW50YXgoCisgICAgICAgICJ4ID0gMSIsCisgICAgICAgIGxleGVyPSJweXRob24iLAorICAgICAgICBwYWRkaW5nPSgxLCAzKSwKKyAgICAgICAgYmFja2dyb3VuZF9jb2xvcj0icmVkIiwKKyAgICApCisgICAgcmVzdWx0ID0gcmVuZGVyKHN5bnRheCkKKyAgICBwcmludChyZXByKHJlc3VsdCkpCisgICAgYXNzZXJ0ICgKKyAgICAgICAgcmVzdWx0CisgICAgICAgID09ICJceDFiWzQxbSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBceDFiWzBtXG5ceDFiWzQxbSAgIFx4MWJbMG1ceDFiWzM4OzI7MjQ4OzI0ODsyNDI7NDFteFx4MWJbMG1ceDFiWzM4OzI7MjQ4OzI0ODsyNDI7NDFtIFx4MWJbMG1ceDFiWzM4OzI7MjU1OzcwOzEzNzs0MW09XHgxYlswbVx4MWJbMzg7MjsyNDg7MjQ4OzI0Mjs0MW0gXHgxYlswbVx4MWJbMzg7MjsxNzQ7MTI5OzI1NTs0MW0xXHgxYlswbVx4MWJbNDFtICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBceDFiWzBtXHgxYls0MW0gICBceDFiWzBtXG5ceDFiWzQxbSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBceDFiWzBtXG4iCisgICAgKQorCisKIGlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICAgc3ludGF4ID0gUGFuZWwuZml0KAogICAgICAgICBTeW50YXgoCgo=",
  },
  "rich_3454": {
    "repo": "Textualize/rich",
    "base": "e1e6d745f670",
    "pytest": "tests/test_highlighter.py",
    "k": "test_wrong_type",
    "src": "rich/highlighter.py",
    "fixB64": "ZGlmZiAtLWdpdCBhL3JpY2gvaGlnaGxpZ2h0ZXIucHkgYi9yaWNoL2hpZ2hsaWdodGVyLnB5CmluZGV4IDI3NzE0YjI1YjQuLmU0YzQ2MmUyYjYgMTAwNjQ0Ci0tLSBhL3JpY2gvaGlnaGxpZ2h0ZXIucHkKKysrIGIvcmljaC9oaWdobGlnaHRlci5weQpAQCAtOTgsNyArOTgsNyBAQCBjbGFzcyBSZXBySGlnaGxpZ2h0ZXIoUmVnZXhIaWdobGlnaHRlcik6CiAgICAgICAgICAgICByIig/UDxudW1iZXI+KD88IVx3KVwtP1swLTldK1wuP1swLTldKihlWy0rXT9cZCs/KT9cYnwweFswLTlhLWZBLUZdKikiLAogICAgICAgICAgICAgciIoP1A8cGF0aD5cQigvWy1cdy5fK10rKSpcLykoP1A8ZmlsZW5hbWU+Wy1cdy5fK10qKT8iLAogICAgICAgICAgICAgciIoPzwhW1xcXHddKSg/UDxzdHI+Yj8nJycuKj8oPzwhXFwpJycnfGI/Jy4qPyg/PCFcXCknfGI/XCJcIlwiLio/KD88IVxcKVwiXCJcInxiP1wiLio/KD88IVxcKVwiKSIsCi0gICAgICAgICAgICByIig/UDx1cmw+KGZpbGV8aHR0cHN8aHR0cHx3c3x3c3MpOi8vWy0wLTlhLXpBLVokXyshYCgpLC4/Lzs6Jj0lI35dKikiLAorICAgICAgICAgICAgciIoP1A8dXJsPihmaWxlfGh0dHBzfGh0dHB8d3N8d3NzKTovL1stMC05YS16QS1aJF8rIWAoKSwuPy87OiY9JSN+QF0qKSIsCiAgICAgICAgICksCiAgICAgXQogCg==",
    "testB64": "ZGlmZiAtLWdpdCBhL3Rlc3RzL3Rlc3RfaGlnaGxpZ2h0ZXIucHkgYi90ZXN0cy90ZXN0X2hpZ2hsaWdodGVyLnB5CmluZGV4IDMwODUxY2Y3OWMuLmQxOTkyODI3NGEgMTAwNjQ0Ci0tLSBhL3Rlc3RzL3Rlc3RfaGlnaGxpZ2h0ZXIucHkKKysrIGIvdGVzdHMvdGVzdF9oaWdobGlnaHRlci5weQpAQCAtMTM0LDYgKzEzNCw3IEBAIGRlZiB0ZXN0X3dyb25nX3R5cGUoKToKICAgICAoIiBodHRwOi8vZXhhbXBsZS5vcmcgIiwgW1NwYW4oMSwgMTksICJyZXByLnVybCIpXSksCiAgICAgKCIgaHR0cDovL2V4YW1wbGUub3JnL2luZGV4Lmh0bWwgIiwgW1NwYW4oMSwgMzAsICJyZXByLnVybCIpXSksCiAgICAgKCIgaHR0cDovL2V4YW1wbGUub3JnL2luZGV4Lmh0bWwjYW5jaG9yICIsIFtTcGFuKDEsIDM3LCAicmVwci51cmwiKV0pLAorICAgICgiaHR0cHM6Ly93d3cueW91dHViZS5jb20vQExpbnVzVGVjaFRpcHMiLCBbU3BhbigwLCAzOCwgInJlcHIudXJsIildKSwKICAgICAoCiAgICAgICAgICIgaHR0cDovL2V4YW1wbGUub3JnL2luZGV4Lmh0bWw/cGFyYW0xPXZhbHVlMSAiLAogICAgICAgICBbCgo=",
  },
}
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, ((p.stdout or "")[-2000:] + (p.stderr or "")[-2000:])
sh("pip install -q pytest pytest-timeout pygments typing-extensions 2>&1 | tail -1", timeout=300)
for pid, t in TASKS.items():
    work = "/tmp/duck6_" + pid
    sh("rm -rf " + work + " && mkdir -p " + work)
    url = "https://github.com/" + t["repo"] + "/archive/" + t["base"] + ".tar.gz"
    print("FETCH " + pid + " " + url, flush=True)
    try:
        urllib.request.urlretrieve(url, work + "/src.tgz")
    except Exception as e:
        print("TEST-RESULT " + pid + " fetch-fail " + str(e)[:160], flush=True)
        continue
    sh("tar xzf " + work + "/src.tgz -C " + work + " --strip-components=1", timeout=120)
    pyenv = "PYTHONPATH=" + work
    mrc, mout = sh("cd " + work + " && " + pyenv + " python -c \"import rich; print(rich.__file__)\" 2>&1 | tail -2", timeout=60)
    print("MODFILE " + pid + " rich " + mout[-160:], flush=True)
    if (work + "/") not in mout:
        print("TEST-RESULT " + pid + " shadow-fail " + mout[-160:], flush=True)
        continue
    open(work + "/fix.diff", "w").write(base64.b64decode(t["fixB64"]).decode())
    frc, fout = sh("cd " + work + " && git apply fix.diff 2>&1; echo FIX_APPLIED_RC=$?", timeout=60)
    print("FIX-APPLY " + pid + " " + fout[-200:], flush=True)
    if "FIX_APPLIED_RC=0" not in fout:
        print("TEST-RESULT " + pid + " fix-apply-fail", flush=True)
        continue
    open(work + "/test_patch.diff", "w").write(base64.b64decode(t["testB64"]).decode())
    trc2, tout2 = sh("cd " + work + " && git apply test_patch.diff 2>&1; echo TEST_APPLIED_RC=$?", timeout=60)
    print("TEST-APPLY " + pid + " " + tout2[-200:], flush=True)
    if "TEST_APPLIED_RC=0" not in tout2:
        print("TEST-RESULT " + pid + " test-apply-fail", flush=True)
        continue
    brc, bout = sh("cd " + work + " && " + pyenv + " python -m pytest " + t["pytest"] + " -k " + t["k"] + " -q --tb=no -p no:cacheprovider > basefail_out.txt 2>&1; echo BASE_RC=$? > base_rc.txt; tail -5 basefail_out.txt; cat base_rc.txt", timeout=300)
    import re as _re2
    _bm = _re2.search(r"BASE_RC=(\d+)", bout)
    _brc = _bm.group(1) if _bm else "?"
    print("BASE-FAIL-PROOF " + pid + " base_rc=" + _brc + " " + bout[-300:], flush=True)
    crc, cout = sh("cd " + work + " && python -m py_compile " + t["src"] + " 2>&1; echo COMPILE_RC=$?", timeout=60)
    print("COMPILE " + pid + " " + cout[-200:], flush=True)
    trc, tout = sh("cd " + work + " && " + pyenv + " python -m pytest " + t["pytest"] + " -k " + t["k"] + " -v --tb=short -p no:cacheprovider > pytest_out.txt 2>&1; echo PYTEST_RC=$?; tail -15 pytest_out.txt", timeout=300)
    sh("cp " + work + "/pytest_out.txt " + OUT_DIR + "/" + pid + ".pytest.txt", timeout=30)
    open(OUT_DIR + "/" + pid + ".applied.txt", "w").write("fix_rc=0 test_rc=0 pytest_out_tail:\n" + tout[-1500:])
    import re as _re
    _m = _re.search(r"PYTEST_RC=(\d+)", tout)
    _ptr = _m.group(1) if _m else "?"
    print("TEST-RESULT " + pid + " rc=" + str(trc) + " pytest_rc=" + _ptr + " " + tout[-800:], flush=True)
print("PROBE-DONE", flush=True)
