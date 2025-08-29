# app.py — Intentionally vulnerable demo app for Tracer `discover` testing

# This script pulls in several libraries with known historical issues, and intentionally
# uses risky code paths so your runtime tracer can detect imports and execution.
# ⚠️ For educational/testing purposes only. Do not expose to the internet.
# Recommended: Python 3.10 in a virtualenv.


import argparse
import json
import os
import sys

# Runtime imports that Tracer should see:
import yaml  # PyYAML (unsafe load used below)
from jinja2 import Template  # older Jinja2
import urllib3  # older urllib3
import requests  # older requests, will exercise urllib3 under the hood
from lxml import etree  # lxml XML parsing
from PIL import Image  # Pillow

def demo_yaml(unsafe_yaml: str):
    \"\"\"
    INTENTIONALLY UNSAFE: yaml.load without a safe loader.
    In old PyYAML versions this could allow arbitrary object construction.
    \"\"\"
    print("[demo_yaml] loading YAML UNSAFELY ...")
    data = yaml.load(unsafe_yaml, Loader=None)  # ⚠️ intentional
    print("[demo_yaml] loaded:", data)


def demo_template(untrusted_template: str, ctx_json: str):
    \"\"\"
    Potential SSTI risk in older template engines if app renders untrusted templates.
    \"\"\"
    print("[demo_template] rendering untrusted template ...")
    t = Template(untrusted_template)  # ⚠️ intentional: untrusted template
    ctx = json.loads(ctx_json) if ctx_json else {}
    rendered = t.render(**ctx)
    print("[demo_template] result:", rendered)


def demo_fetch(url: str):
    \"\"\"
    Use urllib3 directly (older vulnerable version in requirements).
    \"\"\"
    print("[demo_fetch] fetching via urllib3 ...")
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    print("[demo_fetch] status:", r.status)
    body = r.data[:200]
    print("[demo_fetch] body (first 200 bytes):", body)


def demo_requests(url: str):
    \"\"\"
    Exercise requests (will import/use urllib3 internally).
    \"\"\"
    print("[demo_requests] fetching via requests ...")
    r = requests.get(url, timeout=5)
    print("[demo_requests] status:", r.status_code)
    print("[demo_requests] body (first 200 bytes):", r.text[:200])


def demo_xml(xml_string: str):
    \"\"\"
    Parse XML (older lxml). Intentionally no hardening to demonstrate parsing path.
    \"\"\"
    print("[demo_xml] parsing XML ...")
    root = etree.fromstring(xml_string.encode("utf-8"))
    print("[demo_xml] root tag:", root.tag)


def demo_image(path: str):
    \"\"\"
    Open an image using Pillow to trigger import and decode path.
    \"\"\"
    print("[demo_image] opening image ...")
    with Image.open(path) as im:
        print("[demo_image] format:", im.format, "size:", im.size, "mode:", im.mode)


def main():
    parser = argparse.ArgumentParser(description="Vulnerable demo app for Tracer discover")
    sub = parser.add_subparsers(dest="cmd")

    p_yaml = sub.add_parser("yaml", help="Unsafe YAML load")
    p_yaml.add_argument("--data", required=True, help="YAML string to load (UNSAFE)")

    p_tpl = sub.add_parser("tpl", help="Render untrusted Jinja2 template")
    p_tpl.add_argument("--template", required=True, help="Untrusted template string")
    p_tpl.add_argument("--ctx", default="{}", help="JSON context for rendering")

    p_fetch = sub.add_parser("fetch", help="Fetch URL via urllib3")
    p_fetch.add_argument("--url", required=True)

    p_req = sub.add_parser("req", help="Fetch URL via requests")
    p_req.add_argument("--url", required=True)

    p_xml = sub.add_parser("xml", help="Parse XML string via lxml")
    p_xml.add_argument("--data", required=True)

    p_img = sub.add_parser("img", help="Open an image via Pillow")
    p_img.add_argument("--path", required=True)

    args = parser.parse_args()

    try:
        if args.cmd == "yaml":
            demo_yaml(args.data)
        elif args.cmd == "tpl":
            demo_template(args.template, args.ctx)
        elif args.cmd == "fetch":
            demo_fetch(args.url)
        elif args.cmd == "req":
            demo_requests(args.url)
        elif args.cmd == "xml":
            demo_xml(args.data)
        elif args.cmd == "img":
            demo_image(args.path)
        else:
            parser.print_help()
            raise SystemExit(2)
    except Exception as e:
        print("[error]", repr(e), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
