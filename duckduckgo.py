# MIT License
#
# Copyright (c) 2017 Deepan Prabhu Babu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# https://github.com/deepanprabhu/duckduckgo-images-api/blob/master/duckduckgo_images_api/api.py
#
# Modified for searching images by Japanese words

import json
import re

import requests


def search(keywords):
    url = "https://duckduckgo.com/"
    params = {"q": keywords}
    res = requests.post(url, data=params)
    search_obj = re.search(r"vqd=([\d-]+)\&", res.text, re.M | re.I)

    if not search_obj:
        return -1

    headers = {
        "authority": "duckduckgo.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "sec-fetch-dest": "empty",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "referer": "https://duckduckgo.com/",
        "accept-language": "ja,en-US;q=0.9,en;q=0.8",
    }

    params = (
        ("l", "jp-jp"),
        ("o", "json"),
        ("q", keywords),
        ("vqd", search_obj.group(1)),
        ("f", ",,,,,"),
        ("p", "1"),
    )

    request_url = url + "i.js"

    while True:
        data = {}

        while True:
            try:
                res = requests.get(request_url, headers=headers, params=params)
                data = json.loads(res.text)
                break
            except ValueError as e:
                print(e)
                break

        if "results" not in data:
            return []
        else:
            return data["results"]


if __name__ == "__main__":
    for image in search("kawasaki ninja"):
        print(image)
