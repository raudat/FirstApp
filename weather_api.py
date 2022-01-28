from typing import Optional
import fastapi
import httpx
from models.location import Location
from models.umbrella_status import UmbrellaStatus

router = fastapi.APIRouter()


@router.get('/api/umbrella', response_model=UmbrellaStatus)
async def do_i_need_an_umbrella(location: Location = fastapi.Depends()):
    url = f'https://weather.talkpython.fm/api/weather?city={location.city}&country={location.country}&units=imperial'
    if location.state:
        url += f'&state={location.state}'

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
    weather = data.get('weather', {})
    category = weather.get('category', "unknown")

    forecast = data.get('forecast', {})
    temp = forecast.get('temp', 0.0)

    bring = category.lower().strip() in {'rain', 'mist'}

    umbrella = UmbrellaStatus(bring_umbrella=bring, temp=temp, weather=category)
    return umbrella
