from streaming.drive_resolver import resolve_drive


async def resolve_link(url: str):

    if "drive.google.com" in url:
        return await resolve_drive(url)

    return url
