
# todolist

[typer](https://typer.tiangolo.com/)で遊ぶ目的で作ったcliのtodolistです。必要最小限のものしか実装していません。

## install

```
pip install r-todolist
```

https://pypi.org/project/r-todolist/

## 仕様

4つのサブコマンドがあり、以下のことができます。

* add: タスクの追加
* ls: タスクの一覧参照
* done: 完了したタスクを完了済みにする
* rm: タスクの削除

### add: タスクの追加

```
$ todo add
Task: buy a shampoo # prompt
added.
```

### add: タスクの一覧

```
$ todo ls
- [] 2. "buy a shampoo"

$ todo ls --done
- [x] 1. "go to the bank"
```

### done: 完了したタスクを完了済みにする

```
$ todo done 2
2. "buy a shampoo" is done🎉
```

### rm: タスクの削除

```
$ todo rm 1 2
removed: 1,2.
```