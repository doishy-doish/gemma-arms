# Q10 REVERSE-TRANSFER (M596, model-free): replay FAILED rail replies through a
# 4-pass grading path (P1 parse blocks, P2 allow-list, P3 search-hit on base,
# P4 full apply + test reset + pytest) plus 2 gold controls. Debugs grading,
# not finding. No rail, no secrets. Duck-6-stagea workflow, OUT_DIR upload.
import os, subprocess, urllib.request, base64
OUT_DIR = "/tmp/duck6_out"
os.makedirs(OUT_DIR, exist_ok=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, ((p.stdout or "")[-2000:] + (p.stderr or "")[-2000:])

def _parse_blocks(body):
    # SLICE-2 delimiter tolerance: models wrap blocks in fences and vary
    # chevrons/spacing (<<<< SEARCH, <<<<<<< SEARCH). Flex ONLY delimiter
    # lines via regex; SEARCH/repl CONTENT bytes stay exact (fidelity gate
    # lives in harness). A trailing ``` fence line is ignored.
    import re as _rx
    _SEARCH_RE = _rx.compile(r"^\s*<{4,8}\s*SEARCH\s*$")
    _SEP_RE = _rx.compile(r"^\s*={4,8}\s*$")
    _END_RE = _rx.compile(r"^\s*>{4,8}\s*$")
    blocks = []
    parts = body.split("FILE:")
    if len(parts) < 2:
        return None
    for p in parts[1:]:
        nl = p.find("\n")
        if nl < 0:
            return None
        path = p[:nl].strip().strip("`").strip()
        if not path:
            return None
        lines = p[nl + 1:].split("\n")
        while lines and lines[-1].strip() in ("```",):
            lines.pop()
        # MULTI-PAIR (M518): successive SEARCH/======/>>>>>> triples under one
        # FILE: header all apply; a malformed triple voids the whole reply.
        triples = []
        i = 0
        n = len(lines)
        while True:
            while i < n and not lines[i].strip():
                i += 1
            if i >= n:
                break
            if not _SEARCH_RE.match(lines[i]):
                return None
            try:
                mi = next(j for j in range(i + 1, n) if _SEP_RE.match(lines[j]))
                ei = next(j for j in range(mi + 1, n) if _END_RE.match(lines[j]))
            except StopIteration:
                return None
            if mi <= i + 1 or ei <= mi + 1:
                return None
            search = "\n".join(lines[i + 1:mi])
            repl = "\n".join(lines[mi + 1:ei])
            if len(search.strip()) < 20:
                return None
            triples.append((search, repl))
            i = ei + 1
        if not triples:
            return None
        for (search, repl) in triples:
            blocks.append((path, search, repl))
    return blocks or None

ALLOWMAP = {
    "fastapi_13537": ["fastapi/dependencies/utils.py"],
    "rich_3894": ["rich/_inspect.py"],
    "fastapi_15589": ["fastapi/dependencies/utils.py"],
}
FAILS = {
    "fastapi_13537": "FILE: fastapi/params.py\n<<<<<< SEARCH\nasync def _extract_form_body(\n    body_fields: List[ModelField],\n    received_body: FormData,\n) -> Dict[str, Any]:\n    values = {}\n======\nasync def _extract_form_body(\n    body_fields: List[ModelField],\n    received_body: FormData,\n) -> Dict[str, Any]:\n    values = {}\n    processed_keys = set()\n>>>>>>\n<<<<<< SEARCH\n        if value is not None:\n            values[field.alias] = value\n    for key, value in received_body.items():\n        if key not in values:\n            values[key] = value\n======\n        if value is not None:\n            values[field.alias] = value\n        processed_keys.add(field.alias)\n    for key, value in received_body.items():\n        if key not in processed_keys:\n            values[key] = value\n>>>>>>",
    "rich_3894": "FILE: rich/inspect.py\n<<<<<< SEARCH\n        qualname = name or getattr(obj, \"__qualname__\", name)\n\n        # If obj is a module, there may be classes (which are callable) to display\n======\n        qualname = name or getattr(obj, \"__qualname__\", name)\n        if not isinstance(qualname, str):\n            qualname = getattr(obj, \"__name__\", name)\n        if not isinstance(qualname, str):\n            qualname = name\n\n        # If obj is a module, there may be classes (which are callable) to display\n>>>>>>",
    "fastapi_15589": "",
}
CONTROLS = {
    "rich_2725": {"repo": "Textualize/rich", "base": "577def22dd83", "pytest": "tests/test_table.py", "k": "test_placement_table_box_elements", "testB64": "LS0tIGEvdGVzdHMvdGVzdF90YWJsZS5weQorKysgYi90ZXN0cy90ZXN0X3RhYmxlLnB5CkBAIC0xLDYgKzEsNyBAQAogIyBlbmNvZGluZz11dGYtOAogCiBpbXBvcnQgaW8KK2Zyb20gdGV4dHdyYXAgaW1wb3J0IGRlZGVudAogCiBpbXBvcnQgcHl0ZXN0CiAKQEAgLTIzNCw2ICsyMzUsMTM0IEBAIGRlZiB0ZXN0X3NlY3Rpb24oKToKICAgICBhc3NlcnQgb3V0cHV0ID09IGV4cGVjdGVkCiAKIAorQHB5dGVzdC5tYXJrLnBhcmFtZXRyaXplKAorICAgICJzaG93X2hlYWRlcixzaG93X2Zvb3RlcixleHBlY3RlZCIsCisgICAgWworICAgICAgICAoCisgICAgICAgICAgICBGYWxzZSwKKyAgICAgICAgICAgIEZhbHNlLAorICAgICAgICAgICAgZGVkZW50KAorICAgICAgICAgICAgICAgICIiIgorICAgICAgICAgICAgICAgIGFiYmJiYmNiYmJiYmJiYmJjYmJiYmNiYmJiYmQKKyAgICAgICAgICAgICAgICAxRGVjICAyU2t5d2Fsa2VyMjI3NU0yMzc1TSAzCisgICAgICAgICAgICAgICAgNE1heSAgNVNvbG8gICAgIDUyNzVNNTM5M00gNgorICAgICAgICAgICAgICAgIGlqampqamtqampqampqamprampqamtqampqamwKKyAgICAgICAgICAgICAgICA3RGVjICA4TGFzdCBKZWRpODI2Mk04MTMzM005CisgICAgICAgICAgICAgICAgcXJycnJyc3JycnJycnJycnNycnJyc3JycnJydAorICAgICAgICAgICAgICAgICIiIgorICAgICAgICAgICAgKS5sc3RyaXAoKSwKKyAgICAgICAgKSwKKyAgICAgICAgKAorICAgICAgICAgICAgVHJ1ZSwKKyAgICAgICAgICAgIEZhbHNlLAorICAgICAgICAgICAgZGVkZW50KAorICAgICAgICAgICAgICAgICIiIgorICAgICAgICAgICAgICAgIGFiYmJiYmNiYmJiYmJiYmJjYmJiYmNiYmJiYmQKKyAgICAgICAgICAgICAgICAxTW9udGgyTmlja25hbWUgMkNvc3QyR3Jvc3MzCisgICAgICAgICAgICAgICAgZWZmZmZmZ2ZmZmZmZmZmZmdmZmZmZ2ZmZmZmaAorICAgICAgICAgICAgICAgIDREZWMgIDVTa3l3YWxrZXI1Mjc1TTUzNzVNIDYKKyAgICAgICAgICAgICAgICA0TWF5ICA1U29sbyAgICAgNTI3NU01MzkzTSA2CisgICAgICAgICAgICAgICAgaWpqampqa2pqampqampqamtqampqa2pqampqbAorICAgICAgICAgICAgICAgIDdEZWMgIDhMYXN0IEplZGk4MjYyTTgxMzMzTTkKKyAgICAgICAgICAgICAgICBxcnJycnJzcnJycnJycnJyc3JycnJzcnJycnJ0CisgICAgICAgICAgICAgICAgIiIiCisgICAgICAgICAgICApLmxzdHJpcCgpLAorICAgICAgICApLAorICAgICAgICAoCisgICAgICAgICAgICBGYWxzZSwKKyAgICAgICAgICAgIFRydWUsCisgICAgICAgICAgICBkZWRlbnQoCisgICAgICAgICAgICAgICAgIiIiCisgICAgICAgICAgICAgICAgYWJiYmJiY2JiYmJiYmJiYmNiYmJiY2JiYmJiZAorICAgICAgICAgICAgICAgIDFEZWMgIDJTa3l3YWxrZXIyMjc1TTIzNzVNIDMKKyAgICAgICAgICAgICAgICA0TWF5ICA1U29sbyAgICAgNTI3NU01MzkzTSA2CisgICAgICAgICAgICAgICAgaWpqampqa2pqampqampqamtqampqa2pqampqbAorICAgICAgICAgICAgICAgIDREZWMgIDVMYXN0IEplZGk1MjYyTTUxMzMzTTYKKyAgICAgICAgICAgICAgICBtbm5ubm5vbm5ubm5ubm5ub25ubm5vbm5ubm5wCisgICAgICAgICAgICAgICAgN01PTlRIOE5JQ0tOQU1FIDhDT1NUOEdST1NTOQorICAgICAgICAgICAgICAgIHFycnJycnNycnJycnJycnJzcnJycnNycnJycnQKKyAgICAgICAgICAgICAgICAiIiIKKyAgICAgICAgICAgICkubHN0cmlwKCksCisgICAgICAgICksCisgICAgICAgICgKKyAgICAgICAgICAgIFRydWUsCisgICAgICAgICAgICBUcnVlLAorICAgICAgICAgICAgZGVkZW50KAorICAgICAgICAgICAgICAgICIiIgorICAgICAgICAgICAgICAgIGFiYmJiYmNiYmJiYmJiYmJjYmJiYmNiYmJiYmQKKyAgICAgICAgICAgICAgICAxTW9udGgyTmlja25hbWUgMkNvc3QyR3Jvc3MzCisgICAgICAgICAgICAgICAgZWZmZmZmZ2ZmZmZmZmZmZmdmZmZmZ2ZmZmZmaAorICAgICAgICAgICAgICAgIDREZWMgIDVTa3l3YWxrZXI1Mjc1TTUzNzVNIDYKKyAgICAgICAgICAgICAgICA0TWF5ICA1U29sbyAgICAgNTI3NU01MzkzTSA2CisgICAgICAgICAgICAgICAgaWpqampqa2pqampqampqamtqampqa2pqampqbAorICAgICAgICAgICAgICAgIDREZWMgIDVMYXN0IEplZGk1MjYyTTUxMzMzTTYKKyAgICAgICAgICAgICAgICBtbm5ubm5vbm5ubm5ubm5ub25ubm5vbm5ubm5wCisgICAgICAgICAgICAgICAgN01PTlRIOE5JQ0tOQU1FIDhDT1NUOEdST1NTOQorICAgICAgICAgICAgICAgIHFycnJycnNycnJycnJycnJzcnJycnNycnJycnQKKyAgICAgICAgICAgICAgICAiIiIKKyAgICAgICAgICAgICkubHN0cmlwKCksCisgICAgICAgICksCisgICAgXSwKKykKK2RlZiB0ZXN0X3BsYWNlbWVudF90YWJsZV9ib3hfZWxlbWVudHMoc2hvd19oZWFkZXIsIHNob3dfZm9vdGVyLCBleHBlY3RlZCk6CisgICAgIiIiRW5zdXJlIGJveCBkcmF3aW5nIGNoYXJhY3RlcnMgY29ycmVjdGx5IHBvc2l0aW9uZWQuIiIiCisKKyAgICB0YWJsZSA9IFRhYmxlKAorICAgICAgICBib3g9Ym94LkFTQ0lJLCBzaG93X2hlYWRlcj1zaG93X2hlYWRlciwgc2hvd19mb290ZXI9c2hvd19mb290ZXIsIHBhZGRpbmc9MAorICAgICkKKworICAgICMgY29udGVudCByb3dzIGluZGljYXRlZCBieSBudW1lcmFscywgcHVyZSBkaXZpZGVycyBieSBsZXR0ZXJzCisgICAgdGFibGUuYm94Ll9fZGljdF9fLnVwZGF0ZSgKKyAgICAgICAgdG9wX2xlZnQ9ImEiLAorICAgICAgICB0b3A9ImIiLAorICAgICAgICB0b3BfZGl2aWRlcj0iYyIsCisgICAgICAgIHRvcF9yaWdodD0iZCIsCisgICAgICAgIGhlYWRfbGVmdD0iMSIsCisgICAgICAgIGhlYWRfdmVydGljYWw9IjIiLAorICAgICAgICBoZWFkX3JpZ2h0PSIzIiwKKyAgICAgICAgaGVhZF9yb3dfbGVmdD0iZSIsCisgICAgICAgIGhlYWRfcm93X2hvcml6b250YWw9ImYiLAorICAgICAgICBoZWFkX3Jvd19jcm9zcz0iZyIsCisgICAgICAgIGhlYWRfcm93X3JpZ2h0PSJoIiwKKyAgICAgICAgbWlkX2xlZnQ9IjQiLAorICAgICAgICBtaWRfdmVydGljYWw9IjUiLAorICAgICAgICBtaWRfcmlnaHQ9IjYiLAorICAgICAgICByb3dfbGVmdD0iaSIsCisgICAgICAgIHJvd19ob3Jpem9udGFsPSJqIiwKKyAgICAgICAgcm93X2Nyb3NzPSJrIiwKKyAgICAgICAgcm93X3JpZ2h0PSJsIiwKKyAgICAgICAgZm9vdF9sZWZ0PSI3IiwKKyAgICAgICAgZm9vdF92ZXJ0aWNhbD0iOCIsCisgICAgICAgIGZvb3RfcmlnaHQ9IjkiLAorICAgICAgICBmb290X3Jvd19sZWZ0PSJtIiwKKyAgICAgICAgZm9vdF9yb3dfaG9yaXpvbnRhbD0ibiIsCisgICAgICAgIGZvb3Rfcm93X2Nyb3NzPSJvIiwKKyAgICAgICAgZm9vdF9yb3dfcmlnaHQ9InAiLAorICAgICAgICBib3R0b21fbGVmdD0icSIsCisgICAgICAgIGJvdHRvbT0iciIsCisgICAgICAgIGJvdHRvbV9kaXZpZGVyPSJzIiwKKyAgICAgICAgYm90dG9tX3JpZ2h0PSJ0IiwKKyAgICApCisKKyAgICAjIGFkZCBjb250ZW50IC0gbm90ZSBoZWFkZXJzIHRpdGxlIGNhc2UsIGZvb3RlcnMgdXBwZXIgY2FzZQorICAgIHRhYmxlLmFkZF9jb2x1bW4oIk1vbnRoIiwgIk1PTlRIIiwgd2lkdGg9NSkKKyAgICB0YWJsZS5hZGRfY29sdW1uKCJOaWNrbmFtZSIsICJOSUNLTkFNRSIsIHdpZHRoPTkpCisgICAgdGFibGUuYWRkX2NvbHVtbigiQ29zdCIsICJDT1NUIiwgd2lkdGg9NCkKKyAgICB0YWJsZS5hZGRfY29sdW1uKCJHcm9zcyIsICJHUk9TUyIsIHdpZHRoPTUpCisKKyAgICB0YWJsZS5hZGRfcm93KCJEZWMiLCAiU2t5d2Fsa2VyIiwgIjI3NU0iLCAiMzc1TSIpCisgICAgdGFibGUuYWRkX3JvdygiTWF5IiwgIlNvbG8iLCAiMjc1TSIsICIzOTNNIikKKyAgICB0YWJsZS5hZGRfc2VjdGlvbigpCisgICAgdGFibGUuYWRkX3JvdygiRGVjIiwgIkxhc3QgSmVkaSIsICIyNjJNIiwgIjEzMzNNIikKKworICAgIGNvbnNvbGUgPSBDb25zb2xlKHJlY29yZD1UcnVlLCB3aWR0aD0yOCkKKyAgICBjb25zb2xlLnByaW50KHRhYmxlKQorICAgIG91dHB1dCA9IGNvbnNvbGUuZXhwb3J0X3RleHQoKQorICAgIHByaW50KHJlcHIob3V0cHV0KSkKKworICAgIGFzc2VydCBvdXRwdXQgPT0gZXhwZWN0ZWQKKworCiBpZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgIHJlbmRlciA9IHJlbmRlcl90YWJsZXMoKQogICAgIHByaW50KHJlbmRlcikK", "fixB64": "LS0tIGEvcmljaC90YWJsZS5weQorKysgYi9yaWNoL3RhYmxlLnB5CkBAIC03NzUsMTYgKzc3NSwxNiBAQAogICAgICAgICAgICAgICAgICAgICBfU2VnbWVudChfYm94LmhlYWRfcmlnaHQsIGJvcmRlcl9zdHlsZSksCiAgICAgICAgICAgICAgICAgICAgIF9TZWdtZW50KF9ib3guaGVhZF92ZXJ0aWNhbCwgYm9yZGVyX3N0eWxlKSwKICAgICAgICAgICAgICAgICApLAogICAgICAgICAgICAgICAgICgKKyAgICAgICAgICAgICAgICAgICAgX1NlZ21lbnQoX2JveC5taWRfbGVmdCwgYm9yZGVyX3N0eWxlKSwKKyAgICAgICAgICAgICAgICAgICAgX1NlZ21lbnQoX2JveC5taWRfcmlnaHQsIGJvcmRlcl9zdHlsZSksCisgICAgICAgICAgICAgICAgICAgIF9TZWdtZW50KF9ib3gubWlkX3ZlcnRpY2FsLCBib3JkZXJfc3R5bGUpLAorICAgICAgICAgICAgICAgICksCisgICAgICAgICAgICAgICAgKAogICAgICAgICAgICAgICAgICAgICBfU2VnbWVudChfYm94LmZvb3RfbGVmdCwgYm9yZGVyX3N0eWxlKSwKICAgICAgICAgICAgICAgICAgICAgX1NlZ21lbnQoX2JveC5mb290X3JpZ2h0LCBib3JkZXJfc3R5bGUpLAogICAgICAgICAgICAgICAgICAgICBfU2VnbWVudChfYm94LmZvb3RfdmVydGljYWwsIGJvcmRlcl9zdHlsZSksCiAgICAgICAgICAgICAgICAgKSwKLSAgICAgICAgICAgICAgICAoCi0gICAgICAgICAgICAgICAgICAgIF9TZWdtZW50KF9ib3gubWlkX2xlZnQsIGJvcmRlcl9zdHlsZSksCi0gICAgICAgICAgICAgICAgICAgIF9TZWdtZW50KF9ib3gubWlkX3JpZ2h0LCBib3JkZXJfc3R5bGUpLAotICAgICAgICAgICAgICAgICAgICBfU2VnbWVudChfYm94Lm1pZF92ZXJ0aWNhbCwgYm9yZGVyX3N0eWxlKSwKLSAgICAgICAgICAgICAgICApLAogICAgICAgICAgICAgXQogICAgICAgICAgICAgaWYgc2hvd19lZGdlOgogICAgICAgICAgICAgICAgIHlpZWxkIF9TZWdtZW50KF9ib3guZ2V0X3RvcCh3aWR0aHMpLCBib3JkZXJfc3R5bGUpCg=="},
    "rich_3296": {"repo": "Textualize/rich", "base": "0d7e598fe7ea", "pytest": "tests/test_syntax.py", "k": "test_background_color_override_includes_padding", "testB64": "ZGlmZiAtLWdpdCBhL3Rlc3RzL3Rlc3Rfc3ludGF4LnB5IGIvdGVzdHMvdGVzdF9zeW50YXgucHkKaW5kZXggMzdjYzI5M2ViNC4uYmJkNGM3YTVjYiAxMDA2NDQKLS0tIGEvdGVzdHMvdGVzdF9zeW50YXgucHkKKysrIGIvdGVzdHMvdGVzdF9zeW50YXgucHkKQEAgLTQwNiw2ICs0MDYsMjMgQEAgZGVmIHRlc3Rfc3ludGF4X21lYXN1cmUoKToKICAgICBhc3NlcnQgY29kZS5fX3JpY2hfbWVhc3VyZV9fKGNvbnNvbGUsIGNvbnNvbGUub3B0aW9ucykgPT0gTWVhc3VyZW1lbnQoMywgMjQpCiAKIAorZGVmIHRlc3RfYmFja2dyb3VuZF9jb2xvcl9vdmVycmlkZV9pbmNsdWRlc19wYWRkaW5nKCk6CisgICAgIiIiUmVncmVzc2lvbiB0ZXN0IGZvciBodHRwczovL2dpdGh1Yi5jb20vVGV4dHVhbGl6ZS9yaWNoL2lzc3Vlcy8zMjk1IiIiCisKKyAgICBzeW50YXggPSBTeW50YXgoCisgICAgICAgICJ4ID0gMSIsCisgICAgICAgIGxleGVyPSJweXRob24iLAorICAgICAgICBwYWRkaW5nPSgxLCAzKSwKKyAgICAgICAgYmFja2dyb3VuZF9jb2xvcj0icmVkIiwKKyAgICApCisgICAgcmVzdWx0ID0gcmVuZGVyKHN5bnRheCkKKyAgICBwcmludChyZXByKHJlc3VsdCkpCisgICAgYXNzZXJ0ICgKKyAgICAgICAgcmVzdWx0CisgICAgICAgID09ICJceDFiWzQxbSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBceDFiWzBtXG5ceDFiWzQxbSAgIFx4MWJbMG1ceDFiWzM4OzI7MjQ4OzI0ODsyNDI7NDFteFx4MWJbMG1ceDFiWzM4OzI7MjQ4OzI0ODsyNDI7NDFtIFx4MWJbMG1ceDFiWzM4OzI7MjU1OzcwOzEzNzs0MW09XHgxYlswbVx4MWJbMzg7MjsyNDg7MjQ4OzI0Mjs0MW0gXHgxYlswbVx4MWJbMzg7MjsxNzQ7MTI5OzI1NTs0MW0xXHgxYlswbVx4MWJbNDFtICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBceDFiWzBtXHgxYls0MW0gICBceDFiWzBtXG5ceDFiWzQxbSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBceDFiWzBtXG4iCisgICAgKQorCisKIGlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICAgc3ludGF4ID0gUGFuZWwuZml0KAogICAgICAgICBTeW50YXgoCgo=", "fixB64": "ZGlmZiAtLWdpdCBhL3JpY2gvc3ludGF4LnB5IGIvcmljaC9zeW50YXgucHkKaW5kZXggZjNjZWZmNzU4ZS4uNGRhNmMzYjdhNiAxMDA2NDQKLS0tIGEvcmljaC9zeW50YXgucHkKKysrIGIvcmljaC9zeW50YXgucHkKQEAgLTYxOSw5ICs2MTksNyBAQCBkZWYgX19yaWNoX2NvbnNvbGVfXygKICAgICApIC0+IFJlbmRlclJlc3VsdDoKICAgICAgICAgc2VnbWVudHMgPSBTZWdtZW50cyhzZWxmLl9nZXRfc3ludGF4KGNvbnNvbGUsIG9wdGlvbnMpKQogICAgICAgICBpZiBzZWxmLnBhZGRpbmc6Ci0gICAgICAgICAgICB5aWVsZCBQYWRkaW5nKAotICAgICAgICAgICAgICAgIHNlZ21lbnRzLCBzdHlsZT1zZWxmLl90aGVtZS5nZXRfYmFja2dyb3VuZF9zdHlsZSgpLCBwYWQ9c2VsZi5wYWRkaW5nCi0gICAgICAgICAgICApCisgICAgICAgICAgICB5aWVsZCBQYWRkaW5nKHNlZ21lbnRzLCBzdHlsZT1zZWxmLl9nZXRfYmFzZV9zdHlsZSgpLCBwYWQ9c2VsZi5wYWRkaW5nKQogICAgICAgICBlbHNlOgogICAgICAgICAgICAgeWllbGQgc2VnbWVudHMKIAo="},
}
sh("pip install -q pytest pytest-timeout pygments typing-extensions 2>&1 | tail -1", timeout=300)
for pid, reply in FAILS.items():
    body = (reply or "").strip()
    if body.startswith("```"):
        _ls = body.split("\n")
        body = "\n".join(_ls[1:-1] if _ls[-1].strip().startswith("```") else _ls[1:])
    bl = _parse_blocks(body)
    if not bl:
        print("GRADE-PATH " + pid + " fails-at=P1 empty-or-unparseable len=" + str(len(body)), flush=True)
        continue
    ok = ALLOWMAP[pid]
    bad = [p for (p, _s, _r) in bl if p not in ok]
    if bad:
        print("GRADE-PATH " + pid + " fails-at=P2 wrong-file " + str(bad) + " allowed=" + str(ok), flush=True)
        continue
    print("GRADE-PATH " + pid + " passes-P1P2 blocks=" + str(len(bl)), flush=True)
for pid, t in CONTROLS.items():
    work = "/tmp/duck6_" + pid
    sh("rm -rf " + work + " && mkdir -p " + work)
    url = "https://github.com/" + t["repo"] + "/archive/" + t["base"] + ".tar.gz"
    try:
        urllib.request.urlretrieve(url, work + "/src.tgz")
    except Exception as e:
        print("TEST-RESULT " + pid + " fetch-fail " + str(e)[:160], flush=True)
        continue
    sh("tar xzf " + work + "/src.tgz -C " + work + " --strip-components=1", timeout=120)
    pyenv = "PYTHONPATH=" + work
    open(work + "/fix.diff", "w").write(base64.b64decode(t["fixB64"]).decode())
    frc, fout = sh("cd " + work + " && git apply --check fix.diff 2>&1; echo P3=$?", timeout=60)
    print("GRADE-PATH " + pid + " P3-apply-check " + fout[-200:], flush=True)
    sh("cd " + work + " && git apply fix.diff 2>&1; echo FIX_RC=$?", timeout=60)
    open(work + "/test_patch.diff", "w").write(base64.b64decode(t["testB64"]).decode())
    sh("cd " + work + " && git apply test_patch.diff 2>&1; echo TEST_RC=$?", timeout=60)
    trc, tout = sh("cd " + work + " && " + pyenv + " python -m pytest " + t["pytest"] + " -k " + t["k"] + " -q --tb=short -p no:cacheprovider > pytest_out.txt 2>&1; echo PYTEST_RC=$?; tail -6 pytest_out.txt", timeout=300)
    sh("cp " + work + "/pytest_out.txt " + OUT_DIR + "/" + pid + ".pytest.txt", timeout=30)
    import re as _re
    _m = _re.search(r"PYTEST_RC=(\d+)", tout)
    print("TEST-RESULT " + pid + " pytest_rc=" + (_m.group(1) if _m else "?") + " " + tout[-400:], flush=True)
print("Q10-DONE", flush=True)
