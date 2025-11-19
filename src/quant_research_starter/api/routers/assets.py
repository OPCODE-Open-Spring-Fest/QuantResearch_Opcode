"""Assets router to expose available symbols / sample data."""

from fastapi import APIRouter

from quant_research_starter.data.sample_loader import SampleDataLoader

router = APIRouter(prefix="/api/assets", tags=["assets"])


@router.get("/")
async def list_assets():
    loader = SampleDataLoader()
    df = loader.load_sample_prices()
    symbols = []
    for sym in df.columns:
        symbols.append({"symbol": sym, "price": float(df[sym].iloc[-1])})
    return symbols
