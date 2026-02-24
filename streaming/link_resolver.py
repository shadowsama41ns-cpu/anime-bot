from streaming.drive_resolver import resolve_drive_url as resolve_drive

async def resolve_link(url: str):
    final = await resolve_drive(url)
    return final
