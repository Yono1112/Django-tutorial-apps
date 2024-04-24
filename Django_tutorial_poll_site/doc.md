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

## Choice, Questionモデルの対話シェル([Django tutorial02](https://docs.djangoproject.com/ja/5.0/intro/tutorial02/))
```bash
>>> from polls.models import Choice, Question  # Import the model classes we just wrote.

# No questions are in the system yet.
>>> Question.objects.all()
<QuerySet []>

# Create a new Question.
# Support for time zones is enabled in the default settings file, so
# Django expects a datetime with tzinfo for pub_date. Use timezone.now()
# instead of datetime.datetime.now() and it will do the right thing.
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())

# Save the object into the database. You have to call save() explicitly.
>>> q.save()

# Now it has an ID.
>>> q.id
1

# Access model field values via Python attributes.
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=datetime.timezone.utc)

# Change values by changing the attributes, then calling save().
>>> q.question_text = "What's up?"
>>> q.save()

# objects.all() displays all the questions in the database.
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>
```

```bash
>>> from polls.models import Choice, Question

# Make sure our __str__() addition worked.
>>> Question.objects.all()
<QuerySet [<Question: What's up?>]>

# Django provides a rich database lookup API that's entirely driven by
# keyword arguments.
>>> Question.objects.filter(id=1)
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(question_text__startswith="What")
<QuerySet [<Question: What's up?>]>

# Get the question that was published this year.
>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
<Question: What's up?>

# Request an ID that doesn't exist, this will raise an exception.
>>> Question.objects.get(id=2)
Traceback (most recent call last):
    ...
DoesNotExist: Question matching query does not exist.

# Lookup by a primary key is the most common case, so Django provides a
# shortcut for primary-key exact lookups.
# The following is identical to Question.objects.get(id=1).
>>> Question.objects.get(pk=1)
<Question: What's up?>

# Make sure our custom method worked.
>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()
True

# Give the Question a couple of Choices. The create call constructs a new
# Choice object, does the INSERT statement, adds the choice to the set
# of available choices and returns the new Choice object. Django creates
# a set (defined as "choice_set") to hold the "other side" of a ForeignKey
# relation (e.g. a question's choice) which can be accessed via the API.
>>> q = Question.objects.get(pk=1)

# Display any choices from the related object set -- none so far.
>>> q.choice_set.all()
<QuerySet []>

# Create three choices.
>>> q.choice_set.create(choice_text="Not much", votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text="The sky", votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text="Just hacking again", votes=0)

# Choice objects have API access to their related Question objects.
>>> c.question
<Question: What's up?>

# And vice versa: Question objects get access to Choice objects.
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
3

# The API automatically follows relationships as far as you need.
# Use double underscores to separate relationships.
# This works as many levels deep as you want; there's no limit.
# Find all Choices for any question whose pub_date is in this year
# (reusing the 'current_year' variable we created above).
>>> Choice.objects.filter(question__pub_date__year=current_year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

# Let's delete one of the choices. Use delete() for that.
>>> c = q.choice_set.filter(choice_text__startswith="Just hacking")
>>> c.delete()
```

## クラスベースビューの処理の流れ

- ビューの書き方は関数ベースでの他に、クラスベースでの書き方もある。
- クラスベースビューは関数ベースビューに比べて、コードがより構造化され、可読性と再利用性が向上するメリットがある。
- (ただ、クラスベースは関数ベースに比べて処理内容がブラックボックス化され過ぎているので、内部でどんな流れになっているのかを把握するのが大変だと個人的には感じた。)

1. URLconfのマッチング:
    1. ユーザーが /polls/ をリクエストすると、Django の URLconf がこのリクエストを IndexView にマッチングします。
1. Viewのインスタンス化:
    1. リクエストがビューに到達すると、as_view() によって、定義されたクラス（例えば IndexView など）の新しいインスタンス、つまりビュー関数が作成されます。
1. リクエストの処理:
    1. 生成されたインスタンスは、リクエストに応じて適切なメソッド（GETやPOSTなど）を呼び出します。
1. HTTPレスポンスの生成:
    1. 最終的に、このクラスのメソッドからHTTPレスポンス（ページの内容を含むレスポンス）が生成され、クライアント（ブラウザなど）に送り返されます。

## getメソッドの処理の流れ

1. リクエストオブジェクトの受け取り:
    1. クライアントからのGETリクエストを受け取り、URLconfによってマッチングされたクラスビューの get() メソッドを呼び出します
1. データの取得:
    1. get() メソッドは最初に `get_queryset()` メソッドを呼び出して、ビューが表示するデータ（この場合はオブジェクトのリスト）を取得します。
    1. 例えば、IndexView では最新の5つの質問を取得します。
1. コンテキストデータの生成:
    1. データが取得された後、`get_context_data()` メソッドが呼び出されます。
    1. このメソッドは、テンプレートに渡すためのコンテキスト変数を作成または更新します。
    1. 通常、このメソッドはクエリセット以外の追加のコンテキスト（ページタイトルやフォームオブジェクトなど）を辞書に追加するために使われます。
1. テンプレートのレンダリング:
    1. コンテキストデータが準備できたら、`render_to_response()` メソッドが呼び出されます。
    1. このメソッドは、準備したコンテキストデータと指定されたテンプレートを使用してHTMLを生成します。
1. HTTPレスポンスの返送:
    1. レンダリングされたHTMLは、`HttpResponse` オブジェクトに格納され、最終的にクライアントに送り返されます。
    1. これにより、ユーザーはブラウザで生成されたページを見ることができます。

## 自動テストでのデータベースの設定

- Djangoで自動テストを行う際は、一時的に作成されたデータベースでテストが行われるため、settings.pyで設定しているデータベースのユーザーにデータベース作成の権限を付与する必要がある。
```bash
psql -u <DefaultUser> -d postgres

ALTER USER <DetabaseUser> CREATEDB;

\q
```

## 自動テストにおけるHTMLエンティティに関する問題について

- HTMLエンティティ
    - HTMLで特別な意味を持つ文字（例えば <, >, & など）や、直接HTMLに含めることができない特殊な文字を表現するために使用されます。
    - シングルクォートの場合、次のようにいくつかの形式で表現されることがあります
        - \&#39; – Decimal形式
        - \&#x27; – Hexadecimal形式
        - \&apos; – Entity name（HTML5ではサポートされていない場合があります）
- 自動テストのコードに`self.assertContains(response, "You didn't select a choice")`のようなHTMLエンティティが含まれている場合、Django テンプレートシステムでは、デフォルトで HTML を自動的にエスケープします。これは、XSS 攻撃などのセキュリティリスクを軽減するために重要です。
- テスト目的でエスケープを無効にしたい場合
1. エンティティのデコード
    - テストでHTMLエンティティを扱わないようにする方法は、レスポンスを解析してデコードすることです。PythonにはHTMLエンティティをデコードするためのツールがいくつかあります。 
    - HTMLパーサーを使用
        - html モジュールを使ってエンティティをデコードします。
    ```python
    import html

    def test_vote_without_choice(self):
        url = reverse('polls:vote', args=(self.question.id,))
        response = self.client.post(url)
        content = html.unescape(response.content.decode('utf-8'))
        self.assertIn("You didn't select a choice", content)

    ```
- 注意事項
    - HTMLエンティティをデコードまたは無効にすることは、テストの便宜を図るために有用ですが、本番環境ではセキュリティ上の観点から自動エスケープ機能を無効にすることは推奨されません。
    - テスト環境と本番環境の挙動が異なる場合は、その違いを理解し、適切に対処することが重要です。

## Djangoのソースファイルのパスを出力するコマンド[Django のソースファイルの場所はどこ？](https://docs.djangoproject.com/ja/5.0/intro/tutorial07/)

```bash
python -c "import django; print(django.__path__)"
```

## Djangoのログアウトビューについて

```
Djangoのデフォルトのログアウトビュー（LogoutView）は、GETリクエストを受け付けないように設定されており、主にPOSTメソッドを使用することを想定しています。
これは、ログアウトアクションが状態を変更する操作であるため、セキュリティ上の理由からPOSTを通じてのみ行うべきだとされているためです。

解決策

ログアウト機能を適切に実装するには、以下の方法があります：

- ログアウトリンクにPOSTリクエストを使用する
    - ログアウトを行うためには、フォームを介してPOSTリクエストを送信する方法が推奨されます。これにより、CSRF保護を活用し、ログアウトが安全に行われます。

以下のように、ログアウト用のフォームを追加し、ボタンクリックでPOSTリクエストを送信するようにします：

html
<!-- index.html -->
<li class="nav-item">
    <form action="{% url 'user_auth:logout' %}" method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-link nav-link" style="border: none; background-color: transparent;">Log out</button>
    </form>
</li>

``` 