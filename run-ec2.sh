set -ex

IMAGE_ID=ami-0a92f9c258c79dc9b
EC2_TYPE=g4dn.2xlarge
SUBNET_ID=subnet-083d5fe2232a86bee

aws ec2 run-instances \
--image-id $IMAGE_ID \
--count 1 --instance-type $EC2_TYPE \
--key-name ai-labo-key --security-group-ids sg-0e9ae38bd96f2c56a --subnet-id $SUBNET_ID \
--iam-instance-profile "Arn=arn:aws:iam::896349459446:instance-profile/ai-labo-ec2-role" \
--instance-market-options "MarketType=spot,SpotOptions={SpotInstanceType=one-time}" \
--block-device-mappings "DeviceName=/dev/xvda,Ebs={VolumeSize=200}"
