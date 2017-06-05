# AutoModel
- Python Version : 3.5.2

# 컴퓨팅 환경
#### AWS EC2 접속
- 자신이 접속하고 있는 IP가 EC2 Inbound Rule에 등록되어있어야 함
```
ssh -i "projects/hwang/key/automodel.pem" ubuntu@ec2-13-124-123-141.ap-northeast-2.compute.amazonaws.com
```
#### 환경 세팅 (Ubuntu)
- 기본으로 python3 사용하기 (bash_aliases에 등록)
```
# bash_aliases 수정
$ sudo vim ~/.bash_aliases
## alias python=/usr/bin/python3 입력 후 wq로 Save&Exit
## alias pip=pip3

# 수정된 bash_aliases 적용
$ source ~/.bash_aliases

# 잘 바뀌었는지 확인
$ python --version
```
- pip install
```
cd ~/projects/automodeling
pip install setuptools pip --upgrade
pip --no-cache-dir install -r dev-requirements.txt
```

# Theano 설정
#### ~/.theanorc
```
[global]
floatX = float32
device = cpu
## Optimizer=None은 절대 하면 안 됨
```

# Octave 설정

# Django 설정

# Lasagne 설정
