# ai-labo-2023

## 第２回

### BLIP

https://huggingface.co/stabilityai/japanese-instructblip-alpha

https://huggingface.co/docs/transformers/main/model_doc/instructblip

https://trail.t.u-tokyo.ac.jp/ja/blog/22-12-02-clip/


### ELYZA

https://huggingface.co/elyza/ELYZA-japanese-Llama-2-7b-instruct

https://huggingface.co/mmnga/ELYZA-japanese-Llama-2-7b-instruct-gguf

https://huggingface.co/mmnga/ELYZA-japanese-Llama-2-7b-instruct-gguf/resolve/main/ELYZA-japanese-Llama-2-7b-instruct-q5_K_M.gguf

https://rye-up.com/

https://github.com/marella/ctransformers


## EC2 準備

今回は、Amazon Linux 2 の代わりに Ubuntu を使います。

## EC2 起動後

```
$ sudo apt update -q
$ sudo apt upgrade -qy
$ sudo apt install -y zstd tree
```

## S3 マウント

```
$ curl -LO https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.deb
$ sudo apt install -y ./mount-s3.deb

$ mkdir -p `pwd`/s3
$ mount-s3 ai-labo-2023 `pwd`/s3
```

## BLIP デモ

```
$ docker pull public.ecr.aws/hic-ai-labo/pynt
$ docker tag public.ecr.aws/hic-ai-labo/pynt pynt

$ git clone https://github.com/hicsoft/ai-labo-2023.git
$ cd ai-labo-2023

$ mkdir .cache
$ zstd -dc ~/s3/blip/models-blip.tar.zst | tar -xf -

$ docker run --gpus all -it --rm \
-v `pwd`/.cache:/home/ubuntu/.cache \
-v `pwd`/blip-study:/home/ubuntu/blip-study \
-v `pwd`/models:/home/ubuntu/models \
--net=host \
-w /home/ubuntu/blip-study pynt
```

```
$ python3 infer.py

$ python3 blip-web.py

$ exit
```

## ELYZA

```
$ mkdir ~/elyza
$ cd ~/elyza

$ curl -sSf https://rye-up.com/get | bash
$ source "$HOME/.rye/env"

$ rye init
$ rye add ctransformers
$ rye sync

$ cp ../ai-labo-2023/ELYZA/infer.py .
$ cp ~/s3/elyza/ELYZA-japanese-Llama-2-7b-instruct-q5_K_M.gguf .

$ python3 infer.py
```

## 後始末

```
$ sudo poweroff
```

## 第１回

https://ja.wikipedia.org/wiki/Stable_Diffusion

https://gigazine.net/news/20221006-visuals-explaining-stable-diffusion/

https://zenn.dev/fusic/articles/paper-reading-lora

## EC2 準備

VPC の設定 (subnet-id, security-group)

SSH キーを登録 (key-name)

EC2 ロールの設定 (iam-instance-profile)

```
Host ai-labo
  HostName xx.yy.zz.ww
  User ec2-user
  IdentityFile ~/.ssh/ai-labo.pem
  ServerAliveInterval 15
  LocalForward 7860 localhost:7860
```

## EC2 起動後

```
$ sudo yum update -y
$ sudo yum install -y zstd tree
```

## S3 マウント (新機能)

```
$ curl -LO https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm
$ sudo yum install -y ./mount-s3.rpm

$ mkdir -p `pwd`/s3
$ mount-s3 ai-labo-2023 `pwd`/s3
```

## SD デモ

```
$ docker pull public.ecr.aws/hic-ai-labo/pynt
$ docker tag public.ecr.aws/hic-ai-labo/pynt pynt

$ git clone https://github.com/hicsoft/ai-labo-2023.git
$ cd ai-labo-2023
$ zstd -dc ~/s3/sd/models.tar.zst | tar -xf -

$ mkdir .cache
$ docker run --gpus all -it --rm \
-v `pwd`/.cache:/home/ubuntu/.cache \
-v `pwd`/sd-study:/home/ubuntu/sd-study \
-v `pwd`/models:/home/ubuntu/models \
--net=host -e "SLACK=xoxb-XXXX:YYYY" \
-w /home/ubuntu/sd-study pynt
```

```
$ python3 sd-gen.py

$ python3 sd-web.py

$ exit
```

```
$ sudo poweroff
```
