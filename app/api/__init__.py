from fastapi import APIRouter

router = APIRouter()

# Import and include all API routers
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.categories import router as categories_router
from app.api.services import router as services_router
from app.api.appointments import router as appointments_router

# Include routers
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(categories_router, prefix="/categories", tags=["categories"])
router.include_router(services_router, prefix="/services", tags=["services"])
router.include_router(appointments_router, prefix="/appointments", tags=["appointments"])

# Uncomment the above imports and includes as you implement each router 