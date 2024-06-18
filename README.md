**https://qdgfg6e7h76dotuf43tajcb23m0pbxym.lambda-url.ap-northeast-1.on.aws**  

# Get Started
デプロイには以下のソフトウェアがインストールされている必要があります．  
以下のソフトウェアがインストールされている必要があります．
* Python 3.12
* pipenv
* Docker
* serverless framework v4

## インストール
```sh
pipenv install
```
以下のコマンドを実行して依存をインストールします．

## ローカルで開発
```sh
pipenv run dev
```
http://0.0.0.0:8080 にアクセス  

## デプロイ
```sh
sls deploy
```
slsコマンドが使用できるようにawsクレデンシャルなどを設定する必要あり
[（参考）](https://qiita.com/mkin/items/0a82c84df084496544c6#3-%E4%BD%9C%E6%88%90%E3%81%97%E3%81%9F-iam%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%81%AE%E3%82%AF%E3%83%AC%E3%83%87%E3%83%B3%E3%82%B7%E3%83%A3%E3%83%AB%E6%83%85%E5%A0%B1%E3%82%92%E8%87%AA%E5%88%86%E3%81%AE%E3%83%9E%E3%82%B7%E3%83%B3%E3%81%AB%E8%A8%AD%E5%AE%9A%E3%81%99%E3%82%8B) 
1.  クレデンシャル情報の設定:
```sh
$ serverless config credentials --provider aws --key アクセスキーID --secret シークレットアクセスキー --profile serverless-servicename-agent
```
2. 設定の確認:
```sh
$ less ~/.aws/credentials
```
3. クレデンシャル情報の確認:
```sh
[default]
aws_access_key_id=アクセスキーID
aws_secret_access_key=シークレットアクセスキー

[serverless-servicename-agent]
aws_access_key_id=アクセスキーID
aws_secret_access_key=シークレットアクセスキー
```

## CI/CD -> 完成間に合わなさそう
**GitHub Actions シークレットの設定方法**
1. GitHubリポジトリにアクセス:
リポジトリのホームページに移動します。
2. リポジトリの設定を開く:
ページ右上の「Settings」タブをクリックします。
3. シークレットのセクションに移動:
左側のメニューから「Secrets and variables」を展開し、「Actions」を選択します。
4. 新しいシークレットを追加:
「New repository secret」ボタンをクリックします。
5. シークレットの情報を入力:
AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEYを設定
6. シークレットを保存:
「Add secret」ボタンをクリックしてシークレットを保存します。  

# 実装内容
## 概要  
* pipenv . FastAPI基盤で実装
* ServerlessFrameworkでIaC化
* Docker・ECRにデプロイ
* アルゴリズムはfast_doubling法でやってみる[（参考）](https://www.nayuki.io/page/fast-fibonacci-algorithms#google_vignette)
* pytestでユニットテストを実装
* ~~CI/CDはGithubActionで~~
* [WebAdapter](https://aws.amazon.com/jp/builders-flash/202301/lambda-web-adapter/)を使って汎用性高くローカルでも開発できるようにしてみよう！

## 仕様
### エンドポイント
ドキュメントは[こちら](https://qdgfg6e7h76dotuf43tajcb23m0pbxym.lambda-url.ap-northeast-1.on.aws/docs#/)  
**200** : Successful Response  
**422** : Validation Error 

### 大きい数字対策
* lambda環境において10,000,000のフィボナッチ数（2089877桁）を求めるのに14.7秒かかってる
* timedout: lambda->900s  APIGateway->30s
* DynamoDBに事前に全部保存しておくのは非現実的
* 新出のときはdynamodbに保存して，既出のときはそれを参照する方法もあるがGETメソッドの範疇超えてしまう 
* 最大値30,000,000に設定するしかない（フィボナッチ数は6269629桁になり，lambda環境で約１分）