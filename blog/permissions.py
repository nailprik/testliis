from rest_framework import permissions

class IsAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_author
        else:
            print(view.action)
            return False

    def has_object_permission(self, request, view, article_obj):

        if view.action in ['update', 'partial_update', 'destroy']:
            return article_obj.author.id == request.user.id
        else:
            return True
        

