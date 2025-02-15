import bson
import fastapi
from starlette.requests import Request

from db.job import JobActions
from services import background_service
from viewmodels.ai.start_job_viewmodel import StartJobViewModel

router = fastapi.APIRouter()


@router.get("/ai/start/{action}/{podcast_id}/episode/{episode_number}")
async def start_job(
    request: Request, action: JobActions, podcast_id: str, episode_number: int
):

    vm = StartJobViewModel(request, podcast_id, episode_number, action)
    job = await background_service.create_background_job(
        action, podcast_id, episode_number
    )

    return {
        "action": action,
        "podcast_id": podcast_id,
        "episode_number": episode_number,
        "job_id": str(job.id),
    }


@router.get("/ai/check-status/{job_id}")
async def check_job_status(request: Request, job_id: str):
    finished = await background_service.is_job_finished(bson.ObjectId(job_id))
    print(f"The job {job_id} is finished?")
    return {"status": "OK"}
