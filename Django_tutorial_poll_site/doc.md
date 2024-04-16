## DjangoとPostgreSQLの接続方法 for Mac

1. PostgreSQLのインストール
```bash
brew install postgresql
```

2. PostgreSQLでデータベース、ユーザーの作成
```bash
brew services start postgresql

psql -U postgres # PostgreSQLのpsqlシェルにpostgresユーザーでログイン

CREATE USER poll_user WITH PASSWORD 'poll_password'; # 新しいユーザーpoll_userを作成

CREATE DATABASE poll_db OWNER poll_user; # 新しいデータベースpoll_dbを作成し、オーナーをpoll_userに設定

GRANT ALL PRIVILEGES ON DATABASE poll_db TO poll_user; # 成したユーザーにデータベースへの接続権限を付与

\q # psqlシェルを終了

psql -U poll_user -d poll_db # 作成したユーザーとデータベースを使ってpsqlシェルに接続できるか確認

\du # ユーザー一覧を表示

\l # データベース一覧を表示

\dt # テーブル一覧を表示
```
- [MacでPostgreSQLを使う](https://django.noizmoon.com/using-postgresql-on-the-mac/)

3. psycopg2のインストール
- DjangoからPostgreSQLに接続するために、psycopg2というPythonのPostgreSQLアダプタをインストールする
```bash
pip install psycopg2
```

4. settings.pyの設定
- 2.で設定したデータベース、ユーザー、パスワードをsetting.pyに書く
- セキュリティ上、データベースの情報は接続サービスファイル（my_service）とパスワードファイル（.my_pgpass）を使用して別で管理する必要がある。([PostgreSQL の接続設定](https://docs.djangoproject.com/ja/5.0/ref/databases/#postgresql-connection-settings))
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'データベース名',
        'USER': 'ユーザー名',
        'PASSWORD': 'パスワード',
        'HOST': 'ホスト名またはIPアドレス',
        'PORT': 'ポート番号',
    }
}
```

5. マイグレーションの実行
- マイグレーションを実行してデータベースのテーブルを作成する
- マイグレーションは現在設定しているモデルに合わせて自動的にデータベースのテーブルを作成する
```bash
python manage.py makemigrations
python manage.py migrate
```

6. 正しくデータベースに接続されているか確認
```bash
psql -U poll_user -d poll_db

\dt # poll_dbのテーブルを一覧表示
```

## makemigrationsとmigrateについて
by perplexity pro
```
python manage.py makemigrationsとpython manage.py migrateの主な違いは以下の通りです。

1. python manage.py makemigrations:
- モデルの変更を検出し、それらの変更を元にマイグレーションファイルを生成するコマンドです。[1][2][6][7]
- モデルを変更した後に実行することで、その変更内容を記述したマイグレーションファイルが作成されます。[1][6][7]
- マイグレーションファイルはmigrationsディレクトリ内に番号付きで生成されます。[5][10]
- マイグレーションファイルはデータベースのスキーマ変更を表すPythonスクリプトです。[2][7]
- マイグレーションファイルはバージョン管理システムでコミットし、アプリケーションと一緒に配布できます。[8]
- マイグレーションファイルを生成するだけで、実際のデータベースは変更されません。[6][7]

2. python manage.py migrate:
- 生成されたマイグレーションファイルを元に、実際にデータベースのスキーマを変更・更新するコマンドです。[1][2][6][7]
- makemigrationsで生成されたマイグレーションファイルを読み取り、その内容をデータベースに反映します。[6][10]
- migrateを実行することで、モデルの変更がデータベースに適用されます。[2][7]
- マイグレーションファイルを順番に適用し、データベースのスキーマを最新の状態に更新します。[5][12]
- マイグレーションの適用状況は、django_migrationsテーブルで管理されます。[4][9]

使い方としては、以下の流れが一般的です。

1. モデルを変更する (models.pyを編集) [6][10][11]
2. python manage.py makemigrations を実行し、マイグレーションファイルを生成する[1][6][10][11]
3. 生成されたマイグレーションファイルを確認し、問題がないことを確認する
4. python manage.py migrate を実行し、マイグレーションを適用してデータベースを更新する[1][6][10][11]

マイグレーションファイルを生成するmakemigrationsと、それを適用するmigrateが分かれている理由は、

- マイグレーションファイルをバージョン管理し、アプリケーションと一緒に配布できるようにするため[8]
- マイグレーションの内容を確認してから適用できるようにするため
- 複数の開発者が同じデータベースを使う場合、マイグレーションのタイミングを制御できるようにするため

などが挙げられます。

このように、makemigrationsはモデルの変更からマイグレーションファイルを生成し、migrateはそのマイグレーションファイルを使ってデータベースを更新する、という役割の違いがあります。モデルを変更した後は、この2つのコマンドを順番に実行することで、データベースのスキーマを安全に更新できます。

Citations:
[1] https://nissy0409.hatenablog.com/entry/2015/09/22/061147
[2] https://note.crohaco.net/2018/django-migration/
[3] https://zenn.dev/kazu1/articles/4e70817baa7dfb
[4] https://qiita.com/okoppe8/items/c9f8372d5ac9a9679396
[5] https://www.ikkitang1211.site/entry/2020/09/30/160025
[6] https://freeheroblog.com/migrations-vs-migrate/
[7] https://qiita.com/frosty/items/8c715a53d7920c9cd1eb
[8] https://docs.djangoproject.com/ja/5.0/intro/tutorial02/
[9] https://zenn.dev/wtkn25/articles/django-migration
[10] https://kuku81kuku81.hatenablog.com/entry/2022/11/8_django_how_to_migrate_models
[11] https://note.com/ym202110/n/n743866ffc3ae
[12] https://selfs-ryo.com/detail/django_migrations_2
[13] https://qiita.com/tfrcm/items/27d2c9e4b3334447b6af
[14] https://hackernoon.com/ja/django-%E3%83%A2%E3%83%87%E3%83%AB%E3%81%AE%E5%A4%89%E6%9B%B4%E3%82%92%E6%9C%AC%E7%95%AA%E7%92%B0%E5%A2%83%E3%81%AB%E3%83%87%E3%83%97%E3%83%AD%E3%82%A4%E3%81%99%E3%82%8B%E3%81%9F%E3%82%81%E3%81%AE%E5%88%9D%E5%BF%83%E8%80%85%E3%82%AC%E3%82%A4%E3%83%89
```

## Djangoの逆参照について

```
Djangoでは、モデル間の関係を定義するために主にForeignKey、OneToOneField、またはManyToManyFieldのようなフィールドを使用します。これらのフィールドは、モデル間で1対多、1対1、多対多のリレーションシップを設定するために使われます。逆参照（逆方向の関連付け）機能は、これらの関係性を活用して、関連するオブジェクト群にアクセスするためのものです。

### 逆参照の基本

たとえば、あるQuestionモデルが複数のChoiceモデルのインスタンスを持つ場合（1対多のリレーションシップ）、ChoiceモデルはForeignKeyを使ってQuestionモデルにリンクされます。この場合、QuestionインスタンスからそのChoiceインスタンス群にアクセスするには逆参照を使用します。

### ForeignKeyの例

Choiceモデルが以下のように定義されているとします。

`
python

from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
`

ここで、ChoiceモデルはQuestionモデルにForeignKeyを通じて紐付けられています。ForeignKeyのon_delete=models.CASCADEは、関連するQuestionが削除された場合に、それに紐付けられたChoiceも自動的に削除されることを指定しています。

### 逆参照の使用

Djangoでは、ForeignKeyフィールドによって作成される逆参照を利用するために、デフォルトで<related_model>_setという属性を提供します。この例では、Questionインスタンスに対してchoice_setという属性を使って、そのQuestionに紐付けられた全てのChoiceオブジェクトにアクセスすることができます。

`
python

question = Question.objects.get(id=1)
choices = question.choice_set.all()  # Questionに紐付けられた全Choiceを取得
`

### カスタム名での逆参照

related_nameオプションをForeignKeyフィールドに指定することで、デフォルトの<related_model>_setではなく、任意の名前で逆参照を行うことができます。例えば、次のように設定することが可能です。

`
python

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
` 

これにより、choice_setの代わりにchoicesを使って逆参照を行うことができるようになります。

`
python

question = Question.objects.get(id=1)
choices = question.choices.all()  # 'choices'を使って逆参照
`

この逆参照機能は、Djangoにおいてリレーショナルデータを扱う際に非常に強力なツールです。これにより、リレーションシップを通じて関連するオブジェクト群を簡単に操作し、アプリケーションのロジックを直感的に記述することが可能になります。
```