import logging
from struct import pack
import re
import base64
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from info import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = AsyncIOMotorClient(USERS_DB)
db = client[DATABASE_NAME]
instance = Instance.from_db(db)

client1 = AsyncIOMotorClient(FILES_DB1)
db1 = client1[DATABASE_NAME]
instance1 = Instance.from_db(db1)

client2 = AsyncIOMotorClient(FILES_DB2)
db2 = client2[DATABASE_NAME]
instance2 = Instance.from_db(db2)

client3 = AsyncIOMotorClient(FILES_DB3)
db3 = client3[DATABASE_NAME]
instance3 = Instance.from_db(db3)

client4 = AsyncIOMotorClient(FILES_DB4)
db4 = client4[DATABASE_NAME]
instance4 = Instance.from_db(db4)

client5 = AsyncIOMotorClient(FILES_DB5)
db5 = client5[DATABASE_NAME]
instance5 = Instance.from_db(db5)

@instance1.register
class Media1(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

@instance2.register
class Media2(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Metaa:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

@instance3.register
class Media3(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Metaa:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

@instance4.register
class Media4(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Metaa:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

@instance5.register
class Media5(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Metaa:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

async def check_file(media):
    """Check if file is present in the database"""

    # TODO: Find better way to get same file_id for same media to avoid duplicates
    file_id, file_ref = unpack_new_file_id(media.file_id)
    
    existing_file1 = await Media1.collection.find_one({"_id": file_id})
    existing_file2 = await Media2.collection.find_one({"_id": file_id})
    existing_file3 = await Media3.collection.find_one({"_id": file_id})
    existing_file4 = await Media4.collection.find_one({"_id": file_id})
    existing_file5 = await Media5.collection.find_one({"_id": file_id})
    if existing_file1:
        pass
    elif existing_file2:
        pass
    elif existing_file3:
        pass
    elif existing_file4:
        pass
    elif existing_file5:
        pass
    else:
        okda = "okda"
        return okda

async def save_file1(media):
    """Save file in DB 1"""

    # TODO: Find better way to get same file_id for same media to avoid duplicates
    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"(_|\+\s|\-|\.|\+|\[MM\]\s|\[MM\]_|\@TvSeriesBay|\@Cinema\sCompany|\@Cinema_Company|\@CC_|\@CC|\@MM_New|\@MM_Linkz|\@MOVIEHUNT|\@CL|\@FBM|\@CKMSERIES|www_DVDWap_Com_|MLM|\@WMR|\[CF\]\s|\[CF\]|\@IndianMoviez|\@tamil_mm|\@infotainmentmedia|\@trolldcompany|\@Rarefilms|\@yamandanmovies|\[YM\]|\@Mallu_Movies|\@YTSLT|\@DailyMovieZhunt|\@I_M_D_B|\@CC_All|\@PM_Old|Dvdworld|\[KMH\]|\@FBM_HW|\@Film_Kottaka|\@CC_X265|\@CelluloidCineClub|\@cinemaheist|\@telugu_moviez|\@CR_Rockers|\@CCineClub|KC_|\[KC\])", " ", str(media.file_name))
    try:
        file = Media1(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            caption=media.caption.html if media.caption else None
        )
    except ValidationError:
        logger.exception('Error occurred while saving file in DB 1')
        return False, 2
    else:
        try:
            await file.commit()
        except DuplicateKeyError:      
            logger.warning(
                f'{getattr(media, "file_name", "NO_FILE")} is already saved in DB 1'
            )
            return False, 0
        else:
            logger.info(f'{getattr(media, "file_name", "NO_FILE")} is saved to DB 1')
            return True, 1

async def save_file2(media):
    """Save file in DB 2"""

    # TODO: Find better way to get same file_id for same media to avoid duplicates
    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"(_|\+\s|\-|\.|\+|\[MM\]\s|\[MM\]_|\@TvSeriesBay|\@Cinema\sCompany|\@Cinema_Company|\@CC_|\@CC|\@MM_New|\@MM_Linkz|\@MOVIEHUNT|\@CL|\@FBM|\@CKMSERIES|www_DVDWap_Com_|MLM|\@WMR|\[CF\]\s|\[CF\]|\@IndianMoviez|\@tamil_mm|\@infotainmentmedia|\@trolldcompany|\@Rarefilms|\@yamandanmovies|\[YM\]|\@Mallu_Movies|\@YTSLT|\@DailyMovieZhunt|\@I_M_D_B|\@CC_All|\@PM_Old|Dvdworld|\[KMH\]|\@FBM_HW|\@Film_Kottaka|\@CC_X265|\@CelluloidCineClub|\@cinemaheist|\@telugu_moviez|\@CR_Rockers|\@CCineClub|KC_|\[KC\])", " ", str(media.file_name))
    try:
        file = Media2(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            caption=media.caption.html if media.caption else None
        )
    except ValidationError:
        logger.exception('Error occurred while saving file in DB 2')
        return False, 2
    else:
        try:
            await file.commit()
        except DuplicateKeyError:      
            logger.warning(
                f'{getattr(media, "file_name", "NO_FILE")} is already saved in DB 2'
            )
            return False, 0
        else:
            logger.info(f'{getattr(media, "file_name", "NO_FILE")} is saved to DB 2')
            return True, 1

async def save_file3(media):
    """Save file in DB 3"""

    # TODO: Find better way to get same file_id for same media to avoid duplicates
    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"(_|\+\s|\-|\.|\+|\[MM\]\s|\[MM\]_|\@TvSeriesBay|\@Cinema\sCompany|\@Cinema_Company|\@CC_|\@CC|\@MM_New|\@MM_Linkz|\@MOVIEHUNT|\@CL|\@FBM|\@CKMSERIES|www_DVDWap_Com_|MLM|\@WMR|\[CF\]\s|\[CF\]|\@IndianMoviez|\@tamil_mm|\@infotainmentmedia|\@trolldcompany|\@Rarefilms|\@yamandanmovies|\[YM\]|\@Mallu_Movies|\@YTSLT|\@DailyMovieZhunt|\@I_M_D_B|\@CC_All|\@PM_Old|Dvdworld|\[KMH\]|\@FBM_HW|\@Film_Kottaka|\@CC_X265|\@CelluloidCineClub|\@cinemaheist|\@telugu_moviez|\@CR_Rockers|\@CCineClub|KC_|\[KC\])", " ", str(media.file_name))
    try:
        file = Media3(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            caption=media.caption.html if media.caption else None
        )
    except ValidationError:
        logger.exception('Error occurred while saving file in DB 3')
        return False, 2
    else:
        try:
            await file.commit()
        except DuplicateKeyError:      
            logger.warning(
                f'{getattr(media, "file_name", "NO_FILE")} is already saved in DB 3'
            )
            return False, 0
        else:
            logger.info(f'{getattr(media, "file_name", "NO_FILE")} is saved to DB 3')
            return True, 1

async def save_file4(media):
    """Save file in DB 4"""

    # TODO: Find better way to get same file_id for same media to avoid duplicates
    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"(_|\+\s|\-|\.|\+|\[MM\]\s|\[MM\]_|\@TvSeriesBay|\@Cinema\sCompany|\@Cinema_Company|\@CC_|\@CC|\@MM_New|\@MM_Linkz|\@MOVIEHUNT|\@CL|\@FBM|\@CKMSERIES|www_DVDWap_Com_|MLM|\@WMR|\[CF\]\s|\[CF\]|\@IndianMoviez|\@tamil_mm|\@infotainmentmedia|\@trolldcompany|\@Rarefilms|\@yamandanmovies|\[YM\]|\@Mallu_Movies|\@YTSLT|\@DailyMovieZhunt|\@I_M_D_B|\@CC_All|\@PM_Old|Dvdworld|\[KMH\]|\@FBM_HW|\@Film_Kottaka|\@CC_X265|\@CelluloidCineClub|\@cinemaheist|\@telugu_moviez|\@CR_Rockers|\@CCineClub|KC_|\[KC\])", " ", str(media.file_name))
    try:
        file = Media4(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            caption=media.caption.html if media.caption else None
        )
    except ValidationError:
        logger.exception('Error occurred while saving file in DB 4')
        return False, 2
    else:
        try:
            await file.commit()
        except DuplicateKeyError:      
            logger.warning(
                f'{getattr(media, "file_name", "NO_FILE")} is already saved in DB 4'
            )
            return False, 0
        else:
            logger.info(f'{getattr(media, "file_name", "NO_FILE")} is saved to DB 4')
            return True, 1

async def save_file5(media):
    """Save file in DB 5"""

    # TODO: Find better way to get same file_id for same media to avoid duplicates
    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"(_|\+\s|\-|\.|\+|\[MM\]\s|\[MM\]_|\@TvSeriesBay|\@Cinema\sCompany|\@Cinema_Company|\@CC_|\@CC|\@MM_New|\@MM_Linkz|\@MOVIEHUNT|\@CL|\@FBM|\@CKMSERIES|www_DVDWap_Com_|MLM|\@WMR|\[CF\]\s|\[CF\]|\@IndianMoviez|\@tamil_mm|\@infotainmentmedia|\@trolldcompany|\@Rarefilms|\@yamandanmovies|\[YM\]|\@Mallu_Movies|\@YTSLT|\@DailyMovieZhunt|\@I_M_D_B|\@CC_All|\@PM_Old|Dvdworld|\[KMH\]|\@FBM_HW|\@Film_Kottaka|\@CC_X265|\@CelluloidCineClub|\@cinemaheist|\@telugu_moviez|\@CR_Rockers|\@CCineClub|KC_|\[KC\])", " ", str(media.file_name))
    try:
        file = Media5(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            caption=media.caption.html if media.caption else None
        )
    except ValidationError:
        logger.exception('Error occurred while saving file in DB 5')
        return False, 2
    else:
        try:
            await file.commit()
        except DuplicateKeyError:      
            logger.warning(
                f'{getattr(media, "file_name", "NO_FILE")} is already saved in DB 5'
            )
            return False, 0
        else:
            logger.info(f'{getattr(media, "file_name", "NO_FILE")} is saved to DB 5')
            return True, 1

async def get_search_results(query, file_type=None, max_results=10, offset=0, filter=False):
    """For given query return (results, next_offset)"""

    query = query.strip()
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(\b|[\.\+\-_:]|\s|&)' + query + r'(\b|[\.\+\-_:]|\s|&)'
    else:
        raw_pattern = query.replace(' ', r'.*[&\s\.\+\-_()\[\]:]')
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return [], '', 0

    if USE_CAPTION_FILTER:
        filter = {'$or': [{'file_name': regex}, {'caption': regex}]}
    else:
        filter = {'file_name': regex}

    if file_type:
        filter['file_type'] = file_type
    # Query both collections
    cursor_media1 = Media1.find(filter).sort('$natural', -1)
    cursor_media2 = Media2.find(filter).sort('$natural', -1)
    cursor_media3 = Media3.find(filter).sort('$natural', -1)
    cursor_media4 = Media4.find(filter).sort('$natural', -1)
    cursor_media5 = Media5.find(filter).sort('$natural', -1)

    # Ensure offset is non-negative
    if offset < 0:
        offset = 0

    # Fetch files from both collections
    files_media1 = await cursor_media1.to_list(length=35)
    files_media2 = await cursor_media2.to_list(length=35)
    files_media3 = await cursor_media3.to_list(length=35)
    files_media4 = await cursor_media4.to_list(length=35)
    files_media5 = await cursor_media5.to_list(length=35)

    total_results = len(files_media1) + len(files_media2) + len(files_media3) + len(files_media4)
    interleaved_files = []
    index_media1 = index_media2 = index_media3 = index_media4 = index_media5 = 0
    while index_media1 < len(files_media1) or index_media2 < len(files_media2) or index_media3 < len(files_media3) or index_media4 < len(files_media4) or index_media5 < len(files_media5):
        if index_media1 < len(files_media1):
            interleaved_files.append(files_media1[index_media1])
            index_media1 += 1
        if index_media2 < len(files_media2):
            interleaved_files.append(files_media2[index_media2])
            index_media2 += 1
        if index_media3 < len(files_media3):
            interleaved_files.append(files_media3[index_media3])
            index_media3 += 1
        if index_media4 < len(files_media4):
            interleaved_files.append(files_media4[index_media4])
            index_media4 += 1
        if index_media5 < len(files_media5):
            interleaved_files.append(files_media5[index_media5])
            index_media5 += 1

    # Slice the interleaved files based on the offset and max_results
    files = interleaved_files[offset:offset + max_results]
    next_offset = offset + len(files)

    # If there are more results, return the next_offset; otherwise, set it to ''
    if next_offset < total_results:
        return files, next_offset, total_results
    else:
        return files, '', total_results

async def get_file_details(query):
    filter = {'file_id': query}
    cursor_media1 = Media1.find(filter)
    filedetails_media1 = await cursor_media1.to_list(length=1)
    if filedetails_media1:
        return filedetails_media1
    cursor_media2 = Media2.find(filter)
    filedetails_media2 = await cursor_media2.to_list(length=1)
    if filedetails_media2:
        return filedetails_media2
    cursor_media3 = Media3.find(filter)
    filedetails_media3 = await cursor_media3.to_list(length=1)
    if filedetails_media3:
        return filedetails_media3
    cursor_media4 = Media4.find(filter)
    filedetails_media4 = await cursor_media4.to_list(length=1)
    if filedetails_media4:
        return filedetails_media4
    cursor_media5 = Media5.find(filter)
    filedetails_media5 = await cursor_media5.to_list(length=1)
    if filedetails_media5:
        return filedetails_media5

def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0
    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0
            r += bytes([i])
    return base64.urlsafe_b64encode(r).decode().rstrip("=")

def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")

def unpack_new_file_id(new_file_id):
    """Return file_id, file_ref"""
    decoded = FileId.decode(new_file_id)
    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )
    file_ref = encode_file_ref(decoded.file_reference)
    return file_id, file_ref

def get_readable_time(seconds) -> str:
    """
    Return a human-readable time format
    """
    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f"{days}d"
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f"{hours}h"
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f"{minutes}m"
    seconds = int(seconds)
    result += f"{seconds}s"
    return result

import re

async def get_latest_movies():
    languages = ["Malayalam", "Tamil", "Telugu", "Kannada", "Hindi", "English", "Chinese", "Japanese", "Korean"]
    latest_movies = {lang: [] for lang in languages}
    latest_movies["Multi"] = []  # Multi-language category
    latest_series = []  # Store series with language tags

    # Fetch latest 20 movies from multiple databases
    movies1 = await Media1.collection.find().sort("$natural", -1).limit(20).to_list(None)
    movies2 = await Media2.collection.find().sort("$natural", -1).limit(20).to_list(None)
    movies3 = await Media3.collection.find().sort("$natural", -1).limit(20).to_list(None)
    movies4 = await Media4.collection.find().sort("$natural", -1).limit(20).to_list(None)4
    all_movies = movies1 + movies2 + movies3 + movies4

    for movie in all_movies:
        file_name = movie.get("file_name", "")
        caption = str(movie.get("caption", ""))  # Ensure caption is always a string

        # Extract movie name and check if it's a series
        match = re.search(r"(.+?)(\d{4})", file_name)
        movie_name = f"{match.group(1).strip()} {match.group(2)}" if match else file_name

        # Detect if it's a series (SXXEYY format)
        series_match = re.search(r"(S\d{2})", file_name, re.IGNORECASE)
        if series_match:
            series_name = re.sub(r"(S\d{2}E\d{2}).*", r"\1", file_name)  # Keep series name + season/episode
            detected_languages = set()

            for lang in languages:
                if re.search(rf"\b{lang}\b", caption, re.IGNORECASE):  # Match full language names
                    detected_languages.add(lang)

            # If multiple languages are found, mark as Multi
            if len(detected_languages) > 1:
                detected_languages = {"Multi"}

            # Format series title with language tags
            language_tags = " ".join(f"#{lang}" for lang in detected_languages) if detected_languages else "#Unknown"
            series_title = f"{series_name} {language_tags}"

            if series_title not in latest_series:
                latest_series.append(series_title)
            continue  # Skip adding to movies

        # Identify and store the movie in multiple language categories
        added_to_languages = set()
        for lang in languages:
            if re.search(rf"\b{lang}\b", caption, re.IGNORECASE):  # Ensure full-word match
                if movie_name not in latest_movies[lang]:  # Avoid duplicates
                    latest_movies[lang].append(movie_name)
                    added_to_languages.add(lang)

        # If a movie belongs to multiple languages, add it to "Multi"
        if len(added_to_languages) > 1:
            if movie_name not in latest_movies["Multi"]:
                latest_movies["Multi"].append(movie_name)

    # ✅ Return structured results with series having language tags
    results = [{"language": lang, "movies": latest_movies[lang][:8]} for lang in latest_movies if latest_movies[lang]]
    if latest_series:
        results.append({"category": "Series", "movies": latest_series[:10]})  # Add Series separately

    return results
