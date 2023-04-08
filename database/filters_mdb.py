import pymongo
from info import DATABASE_URI, DATABASE_NAME
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]


async def add_filter(grp_id, text, reply_text, btn, file, alert):
    mycol = mydb[str(grp_id)]

    data = {
        'text': str(text),
        'reply': str(reply_text),
        'btn': str(btn),
        'file': str(file),
        'alert': str(alert)
    }

    try:
        mycol.update_one({'text': str(text)}, {"$set": data}, upsert=True)
    except pymongo.errors.PyMongoError:
        logger.exception('Some error occurred!', exc_info=True)


async def find_filter(group_id, name):
    mycol = mydb[str(group_id)]

    query = mycol.find({"text": name})

    for file in query:
        reply_text = file['reply']
        btn = file['btn']
        fileid = file['file']
        try:
            alert = file['alert']
        except KeyError:
            alert = None
        return reply_text, btn, alert, fileid

    return None, None, None, None


async def get_filters(group_id):
    mycol = mydb[str(group_id)]

    query = mycol.find()

    texts = [file['text'] for file in query]

    return texts


async def delete_filter(message, text, group_id):
    mycol = mydb[str(group_id)]

    myquery = {'text': text}
    query = mycol.count_documents(myquery)
    if query == 1:
        result = mycol.delete_one(myquery)
        if result.deleted_count == 1:
            await message.reply_text(
                f"'`{text}`' deleted. I'll not respond to that filter anymore.",
                quote=True,
                parse_mode='markdown'
            )
    else:
        await message.reply_text("Couldn't find that filter!", quote=True)


async def del_all(message, group_id, title):
    if str(group_id) not in mydb
