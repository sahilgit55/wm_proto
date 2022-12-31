

z = f"""ffmpeg -hide_banner -loglevel quiet -progress {working_dir} -i {the_media} -i {watermark_path} -filter_complex "[1][0]scale2ref=w='iw*{size}/100':h='ow/mdar'[wm][vid];[vid][wm]overlay={position}" -preset {mode} -codec:a copy {output_vid}"""