from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user
from app.models.users import User, UserRole

def require_role(roles: list[UserRole] | UserRole):  #Dependency для ограничения доступа по ролям.
    if not isinstance(roles, list):
        roles = [roles]

        def role_checker(current_user: User = Depends(get_current_user)):
            if current_user.role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied: {roles}",
                )
            return current_user

    return role_checker