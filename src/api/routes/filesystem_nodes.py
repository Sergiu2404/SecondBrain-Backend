from fastapi import APIRouter

router = APIRouter()

@router.get('/nodes')
def get_nodes():
    return {"message": "all nodes"}