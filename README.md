# ai-labo-2023

```
$ sudo yum update -y
$ sudo yum install -y zstd tree
```

## S3 マウント

```
$ curl -LO https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm
$ sudo yum install -y ./mount-s3.rpm

$ mkdir -p `pwd`/s3
$ mount-s3 ai-labo-2023 `pwd`/s3
```
