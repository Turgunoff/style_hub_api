from fastapi import APIRouter

router = APIRouter()

# Import and include all API routers
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.categories import router as categories_router
from app.api.services import router as services_router
from app.api.appointments import router as appointments_router
from app.api.barbers import router as barbers_router
from app.api.banners import router as banners_router

# Include routers
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(categories_router, prefix="/categories", tags=["categories"])
router.include_router(services_router, prefix="/services", tags=["services"])
router.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
router.include_router(barbers_router, prefix="/barbers", tags=["barbers"])
router.include_router(banners_router, prefix="/banners", tags=["banners"])

# Uncomment the above imports and includes as you implement each router 