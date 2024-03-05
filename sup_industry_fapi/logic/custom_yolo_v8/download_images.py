from simple_image_download import simple_image_download as simp

response=simp.simple_image_download

keyword=["building workers"]

for kw in keyword:
    response().download(kw,limit=200)