import secrets
from datetime import datetime, timezone, timedelta
from typing import cast

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.session_postgresql import AsyncPostgresqlSessionLocal

from src.config.dependencies import get_jwt_auth_manager
from src.database.models.accounts import (
    UserModel, UserGroupModel, ActivationTokenModel,
    PasswordResetTokenModel, RefreshTokenModel
)
from src.schemas.accounts import (
    UserRegistrationRequestSchema, UserRegistrationResponseSchema,
    UserActivationRequestSchema, PasswordResetRequestSchema,
    PasswordResetCompleteSchema, TokenResponseSchema,
    TokenRefreshRequestSchema
)
from src.security.passwords import hash_password, verify_password


async def get_db():
    async with AsyncPostgresqlSessionLocal() as session:
        yield session

router = APIRouter(tags=["Accounts"])


@router.post("/register/", response_model=UserRegistrationResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegistrationRequestSchema, db: AsyncSession = Depends(get_db)):
    try:
        query = select(UserModel).where(UserModel.email == user_data.email)
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A user with this email {user_data.email} already exists."
            )

        group_query = select(UserGroupModel).where(UserGroupModel.name == "USER")
        group_result = await db.execute(group_query)
        user_group = group_result.scalar_one_or_none()

        new_user = UserModel(
            email=user_data.email,
            password=user_data.password,
            is_active=False,
            group_id=user_group.id if user_group else None
        )

        new_user.password = hash_password(user_data.password)

        db.add(new_user)
        await db.flush()

        act_token = ActivationTokenModel(
            token=secrets.token_urlsafe(32),
            expires_at=datetime.now(timezone.utc) + timedelta(days=2),
            user_id=cast(int, new_user.id)
        )
        db.add(act_token)

        await db.commit()
        return new_user

    except HTTPException:
        await db.rollback()
        raise

    except ValueError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    except Exception as e:
        await db.rollback()
        print(f"\n\n!!! THE REAL ERROR IS HERE -> {repr(e)}\n\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during user creation."
        )


@router.post("/activate/", status_code=status.HTTP_200_OK)
async def activate_account(data: UserActivationRequestSchema, db: AsyncSession = Depends(get_db)):
    query = select(UserModel).where(UserModel.email == data.email)
    res = await db.execute(query)
    user = res.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired activation token.")

    if user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User account is already active.")

    token_query = select(ActivationTokenModel).where(
        ActivationTokenModel.user_id == user.id,
        ActivationTokenModel.token == data.token
    )
    token_res = await db.execute(token_query)
    token_record = token_res.scalar_one_or_none()

    if not token_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired activation token.")

    expires_at = cast(datetime, token_record.expires_at).replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expires_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired activation token.")

    user.is_active = True
    await db.delete(token_record)
    await db.commit()

    return {"message": "User account activated successfully."}


@router.post("/password-reset/request/", status_code=status.HTTP_200_OK)
async def request_password_reset(data: PasswordResetRequestSchema, db: AsyncSession = Depends(get_db)):
    success_msg = {"message": "If you are registered, you will receive an email with instructions."}

    query = select(UserModel).where(UserModel.email == data.email)
    res = await db.execute(query)
    user = res.scalar_one_or_none()

    if not user or not user.is_active:
        return success_msg

    old_tokens_query = select(PasswordResetTokenModel).where(PasswordResetTokenModel.user_id == user.id)
    old_tokens_res = await db.execute(old_tokens_query)
    for old_token in old_tokens_res.scalars():
        await db.delete(old_token)

    new_reset_token = PasswordResetTokenModel(
        token=secrets.token_urlsafe(32),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
        user_id=cast(int, user.id)
    )
    db.add(new_reset_token)

    await db.commit()
    return success_msg


@router.post("/reset-password/complete/", status_code=status.HTTP_200_OK)
async def complete_password_reset(data: PasswordResetCompleteSchema, db: AsyncSession = Depends(get_db)):
    query = select(UserModel).where(UserModel.email == data.email)
    res = await db.execute(query)
    user = res.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or token.")

    token_query = select(PasswordResetTokenModel).where(
        PasswordResetTokenModel.user_id == user.id,
        PasswordResetTokenModel.token == data.token
    )
    token_res = await db.execute(token_query)
    token_record = token_res.scalar_one_or_none()

    if not token_record:
        old_tokens_query = select(PasswordResetTokenModel).where(PasswordResetTokenModel.user_id == user.id)
        old_tokens_res = await db.execute(old_tokens_query)
        for old_token in old_tokens_res.scalars():
            await db.delete(old_token)
        await db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or token.")

    expires_at = cast(datetime, token_record.expires_at).replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expires_at:
        await db.delete(token_record)
        await db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or token.")

    try:
        user.password = data.password
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while resetting the password."
        )

    return {"message": "Password reset successfully."}


@router.post("/login/", response_model=TokenResponseSchema, status_code=status.HTTP_201_CREATED)
async def login(user_data: UserRegistrationRequestSchema, db: AsyncSession = Depends(get_db),
                jwt_manager=Depends(get_jwt_auth_manager)):
    query = select(UserModel).where(UserModel.email == user_data.email)
    res = await db.execute(query)
    user = res.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is not activated.")

    try:
        token_data = {
            "sub": user.email,
            "user_id": user.id
        }
        access_token = jwt_manager.create_access_token(data=token_data)
        refresh_token_string = jwt_manager.create_refresh_token(data=token_data)

        refresh_lifetime = timedelta(days=7)

        db_refresh_token = RefreshTokenModel(
            token=refresh_token_string,
            expires_at=datetime.now(timezone.utc) + refresh_lifetime,
            user_id=cast(int, user.id)
        )
        db.add(db_refresh_token)

        await db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_string,
            "token_type": "bearer"
        }

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the request."
        )


@router.post("/refresh/", status_code=200)
async def refresh_access_token(
        refresh_token_data: TokenRefreshRequestSchema,
        db: AsyncSession = Depends(get_db),
        jwt_manager=Depends(get_jwt_auth_manager)
):
    import base64
    import json

    token_str = refresh_token_data.refresh_token

    if hasattr(jwt_manager, "decode_token"):
        try:
            jwt_manager.decode_token(token_str)
        except (HTTPException, Exception, BaseException):
            raise HTTPException(
                status_code=400,
                detail="Token has expired."
            )

    try:
        if token_str and token_str.count('.') == 2:
            payload_b64 = token_str.split('.')[1]
            payload_b64 += '=' * (-len(payload_b64) % 4)
            payload_data = json.loads(base64.urlsafe_b64decode(payload_b64).decode('utf-8'))

            if "exp" in payload_data:
                if datetime.now(timezone.utc).timestamp() > payload_data["exp"]:
                    raise HTTPException(
                        status_code=400,
                        detail="Token has expired."
                    )
    except HTTPException:
        raise
    except (ValueError, KeyError, json.JSONDecodeError):
        pass

    query = select(RefreshTokenModel).where(RefreshTokenModel.token == token_str)
    res = await db.execute(query)
    db_token = res.scalar_one_or_none()

    if not db_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token not found."
        )

    expires_at = cast(datetime, db_token.expires_at).replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expires_at:
        await db.delete(db_token)
        await db.commit()
        raise HTTPException(
            status_code=400,
            detail="Token has expired."
        )

    user_query = select(UserModel).where(UserModel.id == db_token.user_id)
    user_res = await db.execute(user_query)
    user = user_res.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    try:
        token_data = {
            "sub": user.email,
            "user_id": user.id
        }

        new_access_token = jwt_manager.create_access_token(data=token_data)
        new_refresh_token_string = jwt_manager.create_refresh_token(data=token_data)

        await db.delete(db_token)
        await db.commit()

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token_string,
            "token_type": "bearer"
        }

    except Exception as e:
        await db.rollback()
        raise e
