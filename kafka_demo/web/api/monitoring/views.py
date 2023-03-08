from fastapi import APIRouter, status
from fastapi.responses import Response

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK, response_class=Response)
def health_check() -> None:
    """
    # Checks the health of a project.

    ## returns:
    - status 200 if the project is healthy.
    """
