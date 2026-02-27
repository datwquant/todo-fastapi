from repositories.todo_repository import TodoRepository
from schemas.todo import TodoListResponse


class TodoService:
    def __init__(self, repo: TodoRepository):
        self.repo = repo

    def get_todos(self, is_done=None, q=None, sort=None, limit=10, offset=0):
        result = self.repo.get_all()

        if is_done is not None:
            result = [t for t in result if t.is_done == is_done]

        if q is not None:
            result = [t for t in result if q.lower() in t.title.lower()]

        if sort is not None:
            reverse = False
            if sort.startswith("-"):
                reverse = True
                sort_field = sort[1:]
            else:
                sort_field = sort

            if sort_field == "created_at":
                result = sorted(result, key=lambda x: x.created_at, reverse=reverse)

        total = len(result)
        result = result[offset: offset + limit]

        return TodoListResponse(
            items=result,
            total=total,
            limit=limit,
            offset=offset
        )