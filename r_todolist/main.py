from dataclasses import dataclass
from typing import List
import _sqlite3

import typer
from rich import print


app = typer.Typer()


@dataclass
class Tasklists:
    id: int
    task: str
    is_done: bool


class Sqlite3:
    tablename: str = "tasks"

    def __init__(self):
        self.con = _sqlite3.connect("/tmp/r_tasklist")
        self.cur = self.con.cursor()
        self.create_table(self.tablename)

    def create_table(self, name: str):
        sql = "SELECT * FROM sqlite_master WHERE type='table' and name=?"
        self.cur.execute(sql, (self.tablename,))
        if not self.cur.fetchone():
            self.cur.execute(
                f"CREATE TABLE {self.tablename} (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, is_done INTEGER)"
            )
            self.con.commit()
            self.con.close()

    def insert_task(self, task: str):
        sql = f"INSERT INTO {self.tablename} (task, is_done) VALUES (?, ?)"
        self.cur.execute(sql, (task, 0))
        self.con.commit()
        self.con.close()

    def get_lists(self, done: int = 0) -> List[Tasklists]:
        sql = f"SELECT * FROM {self.tablename} WHERE is_done=?"
        rows = self.cur.execute(sql, (done,)).fetchall()
        self.con.commit()
        self.con.close()
        return [Tasklists(*row) for row in rows]

    def done_task(self, id: int) -> Tasklists:
        done_sql = f"UPDATE {self.tablename} SET is_done=1 WHERE id=?"
        self.cur.execute(done_sql, (id,))
        get_task_sql = f"SELECT * FROM {self.tablename} WHERE id=?"
        row = self.cur.execute(get_task_sql, (id,)).fetchone()
        self.con.commit()
        self.con.close()
        return Tasklists(*row)

    def delete_ids(self, ids: List[int]):
        sql = (
            f"DELETE FROM {self.tablename} WHERE id IN ("
            + ",".join(["?" for _ in ids])
            + ")"
        )
        self.cur.execute(sql, tuple(ids))
        self.con.commit()
        self.con.close()


db = Sqlite3()


@app.command()
def add(
    task: str = typer.Option(
        ...,
        prompt=True,
        help="what you have to do.",
        show_default="send a email",
    )
):
    """
    add task to list
    """
    db.insert_task(task)
    print("[green]added.[/green]")


@app.command()
def ls(done: bool = typer.Option(False, help="Show only DONE tasks.")):
    """
    show incomplete tasks.
    """
    task_lists = db.get_lists(done)
    for l in task_lists:
        is_done = "\[x]" if l.is_done else "[]"
        print(f'- {is_done} {l.id}. "{l.task}"')


@app.command()
def done(
    id: int = typer.Argument(
        ..., help="Select task id", metavar="TASK_ID", show_default="1"
    )
):
    """
    check the task
    """
    task = db.done_task(id)
    print(f'{task.id}. "{task.task}" is done:tada:')


@app.command()
def rm(
    ids: List[int] = typer.Argument(
        ...,
        help="Select task_ids separated by spaces.",
        show_default="1 2",
        metavar="TASK_ID",
    )
):
    """
    delete the tasks
    """
    db.delete_ids(ids)
    print(f"removed: {','.join([str(i) for i in ids])}.")


if __name__ == "__main__":
    app()
