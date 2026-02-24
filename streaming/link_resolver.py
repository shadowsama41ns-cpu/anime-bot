from streaming.drive_resolver import resolve_drive_url as resolve_drive

async def resolve_link(url: str):
    """
    Resolve qualquer link suportado (Drive, CDN etc)
    """
    # por enquanto apenas Drive
    final = await resolve_drive(url)
    return final
