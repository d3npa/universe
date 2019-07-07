#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, make_response, render_template, abort, request, redirect
from mimetypes import guess_type as guess_mime
from werkzeug.utils import secure_filename
from os.path import realpath
import os, sys, time, universe, markdown

app = Flask(__name__)
app.url_map.strict_slashes = False
universe.root = realpath(__file__)[:-len("/app.py")]
os.chdir(universe.root)

# デフォルトログを無効化する
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.after_request
def log_access(response):
        connecting_ip = return_ip().data.decode("utf-8")
        http_verb = request.method
        accessed_path = request.path
        status_code = response.status
        sys.stdout.write("[{0}] {1} - {2} - {3} {4}\n".format(
                time.strftime("%y/%m/%d %H:%M:%S"),
                connecting_ip,
                status_code,
                http_verb,
                accessed_path
        ))
        sys.stdout.flush()
        return response

@app.route("/ip")
def return_ip():
        ip = remote_addr = request.headers["X-Forwarded-For"] if "X-Forwarded-For" in request.headers else request.remote_addr
        res = make_response(ip, 200)
        res.headers["Content-Type"] = "text/plain; charset=UTF-8"
        return res

@app.route("/robots.txt")
def return_robotstxt():
        data = "User-agent: *\nDisallow: /\n"
        response = make_response(data)
        response.headers["Content-Type"] = "text/plain; charset=UTF-8;"
        return response

@app.route("/")
def catch_index():
        return catch_all(".index.txt")

@app.route("/.index.txt")
def reroute_index():
        return redirect("/", code=302)

@app.route("/<path:path>")
def catch_all(path):
        path = universe.flatten(path).split("/")
        # print("[* catch_all] Path: %s" % path)
        if path[0] in ["css", "js"]:
                return get_resource("/".join(path))
        else:
                return get_document("/".join(path))
        abort(404)

def get_resource(path):
        path = universe.root + "/res/" + path
        # print("[* get_resource] Path: " + path)
        if os.path.exists(path) and not os.path.isdir(path):
                data = universe.fread(path)
                if data:
                        res = make_response(data, 200)
                        res.headers["Content-Type"] = "%s; charset=UTF-8" % guess_mime(path)[0]
                        return res
        abort(404)

def get_document(path):
        path = universe.root + "/content/" + path
        # print("[* get_document] Path: " + path)
        if os.path.exists(path):
                data = universe.fread(path)
                if data:
                        meta = {
                                "ip" : return_ip().data.decode("utf-8"),
                                "up" : ".." if os.path.isdir(path) else "."
                        }
                        extension = path.split(".")[-1]
                        res = make_response("", 200)
                        if extension in ["txt"] or os.path.isdir(path):
                                html = universe.parse(data.decode("utf-8"), path)
                                meta.update({"content" : html})
                                res.headers["Content-Type"] = "text/html; charset=UTF-8"
                                res.set_data(render_template("txt.html.jinja", data=meta))
                        elif extension in ["md", "markdown"]:
                                html = markdown.markdown(data.decode("utf-8"), extensions=['extra'])
                                meta.update({"content" : html})
                                res.headers["Content-Type"] = "text/html; charset=UTF-8"
                                res.set_data(render_template("txt.html.jinja", data=meta))
                        elif extension in ["png", "jpg", "pdf", "mp3", "mp4"]:
                                res.headers["Content-Type"] = "%s; charset=UTF-8" % guess_mime(path)[0]
                                res.set_data(data)
                        elif extension in ["html", "htm"]:
                                res.headers["Content-Type"] = "text/html; charset=UTF-8"
                                res.set_data(data)
                        else:
                                res.headers["Content-Type"] = "text/plain; charset=UTF-8"
                                res.set_data(data)
                        return res
        abort(404)

if __name__ == '__main__':
    app.run()